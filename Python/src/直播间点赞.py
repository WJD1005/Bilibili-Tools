import requests


# 需要运行机器人的房间号
room_id = 1435894
# 点赞api
url = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/interact/likeInteract'
# 点赞数据
data = {
    'roomid': str(room_id),
    'csrf_token': '',
    'csrf': '',
    'visit_id': '',
}
# 登录状态cookies
my_cookies = {
    'Cookie': ''
}
# 在B站脚本文件夹中cookies.txt文件中获取cookies
with open('../cookies.txt', 'r') as f:
    # 避免文件末尾不小心出现空行，所以只读取一行
    my_cookies['Cookie'] = f.readline()

# 获取csrf
with open('../csrf.txt', 'r') as f:
    # 避免文件末尾不小心出现空行，所以只读取一行
    data['csrf'] = f.readline()
    data['csrf_token'] = data['csrf']

while True:
    requests.post(url, data=data, cookies=my_cookies)



