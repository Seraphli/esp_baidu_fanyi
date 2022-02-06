import requests
import random
import json
from hashlib import md5

HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
ENDPOINT = "http://api.fanyi.baidu.com"
PATH = "/api/trans/vip/translate"
URL = ENDPOINT + PATH


def make_md5(s, encoding="utf-8"):
    return md5(s.encode(encoding)).hexdigest()


class BaiduFanyi(object):
    def __init__(self, appid, appkey) -> None:
        self.appid = appid
        self.appkey = appkey

    def translate(self, query, from_lang="auto", to_lang="zh"):
        salt = random.randint(32768, 65536)
        sign = make_md5(self.appid + query + str(salt) + self.appkey)
        payload = {
            "appid": self.appid,
            "q": query,
            "from": from_lang,
            "to": to_lang,
            "salt": salt,
            "sign": sign,
        }
        r = requests.post(URL, params=payload, headers=HEADERS)
        result = r.json()
        return result

    def form_result(self, result):
        r = "\n".join([i["dst"] for i in result["trans_result"]])
        return r
