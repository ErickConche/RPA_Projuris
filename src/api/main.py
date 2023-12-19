import requests
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

class Api:
    def __init__(self,
                 sessionid) -> None:
        self.proxy = {
            'http': 'http://lum-customer-hl_768b21eb-zone-static' +
            f'-country-br-session-{sessionid}:o631cm60v9v1@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_768b21eb-zone-static' +
            f'-country-br-session-{sessionid}:o631cm60v9v1@zproxy.lum-superproxy.io:22225'
        }
        self.session = requests.Session()
        self.ctx = create_urllib3_context()
        self.ctx.load_default_certs()
        self.ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT
        
    def sendRequestWithPool(self,
                            url,
                            method):
        with urllib3.PoolManager(ssl_context=self.ctx) as http:
            response = http.request(method=method, 
                                    url=url)
            return response
        
    def sendRequestJson(self,
                        url,
                        method,
                        json,
                        headers,
                        cookies,
                        usingProxy):
        if method == 'POST':
            response = requests.post(url=url,
                                     proxies=self.proxy if usingProxy else {},
                                     json=json,
                                     headers=headers,
                                     cookies=cookies)
        return response
        
    def sendRequestNotSession(self,
                              url,
                              method,
                              data,
                              headers,
                              cookies,
                              usingProxy):
        if method == 'GET':
            try:
                response = requests.get(url=url,
                                        headers=headers,
                                        cookies=cookies, 
                                        timeout=20)
            except Exception as error:
                print("Precisou usar proxy, url= "+str(url))
                response = requests.get(url=url,
                                        proxies=self.proxy if usingProxy else {},
                                        headers=headers,
                                        cookies=cookies, 
                                        timeout=20)
        elif method == 'POST':
            try:
                response = requests.post(url=url,
                                         data=data,
                                         headers=headers,
                                         cookies=cookies, 
                                         timeout=20)
            except Exception as error:
                print("Precisou usar proxy, url= "+str(url))
                response = requests.post(url=url,
                                         proxies=self.proxy if usingProxy else {},
                                         data=data,
                                         headers=headers,
                                         cookies=cookies, 
                                         timeout=20)
        return response
        
    def sendRequest(self,
                    url,
                    method,
                    data,
                    headers,
                    cookies,
                    usingProxy):
        if method == 'GET':
            try:
                response = self.session.get(url=url,
                                            headers=headers,
                                            cookies=cookies, 
                                            timeout=20)
            except Exception as error:
                print("Precisou usar proxy, url= "+str(url))
                response = self.session.get(url=url,
                                            proxies=self.proxy if usingProxy else {},
                                            headers=headers,
                                            cookies=cookies, 
                                            timeout=20)
        elif method == 'POST':
            try:
                response = self.session.post(url=url,
                                            data=data,
                                            headers=headers,
                                            cookies=cookies, 
                                            timeout=20)
            except Exception as error:
                print("Precisou usar proxy, url= "+str(url))
                response = self.session.post(url=url,
                                            proxies=self.proxy if usingProxy else {},
                                            data=data,
                                            headers=headers,
                                            cookies=cookies, 
                                            timeout=20)
        return response