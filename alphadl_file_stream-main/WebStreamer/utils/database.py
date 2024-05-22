import requests
import json
from WebStreamer.vars import Var


# global proxy_all

# list = open(r'/root/scraper.acemovie/proxies.txt', 'r')
# proxy_all = list.readlines()
# proxy_all = [i.replace("\r\n", "").replace("\n", "") for i in proxy_all]
# list.close()


# def proxy():
#     import random
#     xx = random.randint(0, len(proxy_all)-1)
#     proxy = proxy_all[xx]
#     return proxy

class Database:
    def __init__(self):
        self.url = "{}base.php?key={}&&table={}&&type={}"
        self.url2 = "{}yunapi.php?title=saeed&&url={}"

        
    def check_user(self, id):
        while True:
            try:
                # http_proxy = proxy()
                # proxies = { 
                #         "http"  : http_proxy,
                #         "https" : http_proxy
                #     }
                response = requests.get(self.url.format(Var.API_URL, Var.API_KEY,'vipusers', 'get')+'&&where={}'.format(id))#,proxies=proxies,timeout=10)
                call_back = response.content
                user_id = json.loads(call_back)['from_id']
                break
            except:
                continue
        return True if bool(user_id) == True else False
    
    def check_status(self, id):
        while True:
            try:
                # http_proxy = proxy()
                # proxies = { 
                #         "http"  : http_proxy,
                #         "https" : http_proxy
                #     }
                response = requests.get(self.url.format(Var.API_URL, Var.API_KEY,'vipusers', 'get')+'&&where={}'.format(id))#,proxies=proxies,timeout=10)
                call_back = response.content
                status = json.loads(call_back)['status']
                break
            except:
                continue
        return True if status == "1" else False

    def check_dailyusage(self, id, size):
        while True:
            try:
                # http_proxy = proxy()
                # proxies = { 
                #         "http"  : http_proxy,
                #         "https" : http_proxy
                #     }
                response = requests.get(self.url.format(Var.API_URL, Var.API_KEY,'vipusers', 'get')+'&&where={}'.format(id))#,proxies=proxies,timeout=10)
                call_back = response.content
                dailyUsage = json.loads(call_back)['dailyUsage']
                break
            except:
                continue
        if float(dailyUsage) >= float(size):
            while True:
                try:
                    requests.post(self.url.format(Var.API_URL, Var.API_KEY,'vipusers', 'update')+'&&where={}&&value={}'.format(id, round(float(dailyUsage) - float(size), 2)))#,proxies=proxies,timeout=10)
                    break
                except:
                    continue
            return True
        else:
            return False

    def info(self, id):
        while True:
            try:
                # http_proxy = proxy()
                # proxies = { 
                #         "http"  : http_proxy,
                #         "https" : http_proxy
                #     }
                response = requests.get(self.url.format(Var.API_URL, Var.API_KEY,'vipusers', 'get')+'&&where={}'.format(id))#,proxies=proxies,timeout=10)
                call_back = response.content
                info = json.loads(call_back)
                break
            except:
                continue
        return info


    def set_data(self, message_id, remove_time):
        while True:
            try:
                # http_proxy = proxy()
                # proxies = { 
                #         "http"  : http_proxy,
                #         "https" : http_proxy
                #     }
                requests.get(self.url.format(Var.API_URL, Var.API_KEY,'vipLinksExpire', 'insert')+'&&messageid={}&&time={}'.format(int(message_id), remove_time))#,proxies=proxies,timeout=10)
                break
            except:
                continue
        return True
    
    def shourt_link(self, dwlink):
        while True:
            try:
                # http_proxy = proxy()
                # proxies = { 
                #         "http"  : http_proxy,
                #         "https" : http_proxy
                #     }
                Response = requests.get(self.url2.format(Var.API_URL, dwlink))#,proxies=proxies,timeout=10)
                result = json.loads(Response.content)['doc']['url']
                break
            except:
                continue
        return result



