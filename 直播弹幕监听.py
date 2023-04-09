import requests
import time

# 每次请求仅提取最新的一条，所以弹幕速度如果快的话会遗漏
# 建议添加缓冲区对一次请求获得的10条弹幕进行重复验证来提高获取速度

url = 'http://api.live.bilibili.com/ajax/msg?roomid='
room_id = '21654925'

# 获取开始时间
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
# 创建文件：时间_房间号.txt
f = open('Record/' + current_time + '_' + room_id + '.txt', 'w')

# 最新弹幕缓存区，用于判断是否重复获取同一条，只对比uid和时间
uid_buff = ' '
time_buff = ' '

while True:
    # 获取历史弹幕（10条）
    res = requests.get(url + room_id).json()
    # 提取最后一条弹幕
    res = res['data']['room'][-1]
    # 提取弹幕信息
    text = res['text']
    uid = str(res['uid'])
    name = res['nickname']
    time = res['timeline']

    if uid_buff != uid and time_buff != time:
        # 记录弹幕
        f.write(time + '\t' + uid + '\t' + name + '\t' + text + '\n')
        print(time + ' ' + uid + ' ' + name + ' ' + text + '\n')
        # 记录缓存信息
        uid_buff = uid
        time_buff = time

        # 未解决文件退出
