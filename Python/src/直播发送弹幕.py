import requests
import time

# 输入房间号
room_id = int(input('请输入房间号：'))

# 发送弹幕的api
url = 'https://api.live.bilibili.com/msg/send'
# 发送弹幕时的数据
msg_data = {
    'bubble': 0,
    'msg': '',                      # 弹幕内容
    'color': 65532,
    'mode': 1,
    'fontsize': 25,
    'rnd': str(int(time.time())),   # 时间戳
    'roomid': room_id,              # 房间号
    'csrf': '',
    'csrf_token': ''
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
    msg_data['csrf'] = f.readline()
    msg_data['csrf_token'] = msg_data['csrf']

while True:
    # 修改发送数据
    msg_data['msg'] = input()
    # 发送
    response = requests.post(url, data=msg_data, cookies=my_cookies)



