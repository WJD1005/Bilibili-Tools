import requests
import time

# 查询天选api
url = 'https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/getLotteryInfoWeb'

# 房间信息api
room_info_url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom'
# 监测房间号
room = [22637261]

# 请求周期，单位：秒
period = 60

while True:
    # 计数器
    num = 0
    update_time = time.strftime('%H:%M:%S', time.localtime())
    for room_id in room:
        response = requests.get(url + '?roomid=' + str(room_id)).json()
        if response['code'] == 0:
            info = response['data']['anchor']
            # 判断有无天选
            if info != None:
                num += 1
                room_info = requests.get(room_info_url + '?room_id=' + str(room_id)).json()
                if room_info['code'] == 0:
                    print('%s[%d]的房间开天选啦~' % (room_info['data']['anchor_info']['base_info']['uname'], room_id))
                else:
                    print('[%d]房间开天选啦~' % room_id)
                print('礼品：%s' % info['award_name'])
                print('份数：%s' % info['award_num'])
                print('弹幕：%s' % info['danmu'])
                print('要求：%s' % info['require_text'])

        else:
            print('%d房间请求失败！' % room_id)
            print('状态码：%d' % response['code'])
            print('返回消息：%s' % response['message'])

    if num == 0:
        print('目前暂无天选')

    print('更新时间 %s' % update_time)

    time.sleep(period)
