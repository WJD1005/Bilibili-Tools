import requests
import json
import time


def get_fans(uid):
    url = 'https://api.bilibili.com/x/relation/stat?vmid=' + str(uid)
    result_str = requests.get(url)
    result = json.loads(result_str.text)
    relation = result.get('data')
    fans = relation.get('follower')
    return fans


def get_time():
    now = time.localtime()
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', now)
    return now_time


while True:
    fans_past = get_fans(122879)
    time.sleep(1)
    fans_now = get_fans(122879)
    fans_add = fans_now - fans_past
    now = get_time()
    print('%s 当前粉丝数：%d 相比于上次：%d' % (now, fans_now, fans_add))
