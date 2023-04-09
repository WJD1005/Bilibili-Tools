import requests
import prettytable
import time
import os

# 粉丝勋章查询api
url = 'https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall'

# 用户id
my_id = 13205905

# 登录状态cookies
my_cookies = {
    'Cookie': ''
}
# 在B站脚本文件夹中cookies.txt文件中获取cookies
with open('../cookies.txt', 'r') as f:
    # 避免文件末尾不小心出现空行，所以只读取一行
    my_cookies['Cookie'] = f.readline()

# 勋章数据表格
table = prettytable.PrettyTable(['序号', '昵称', '粉丝勋章', '等级', '总亲密度', '今日亲密度', '直播状态'])

while True:
    update_time = time.strftime('%H:%M:%S', time.localtime())  # 更新时间
    num = 1  # 序号
    wearing_medal = {'wearing_status': 0, 'target_name': '', 'medal_name': '', 'medal_level': 0}       # 正在佩戴的勋章
    # 请求获取勋章墙数据
    response = requests.get(url + '?target_id=' + str(my_id), cookies=my_cookies).json()
    # 判断请求是否有效
    if response['code'] == 0:
        # 清空表格
        table.clear_rows()
        # 获得勋章总数
        count = response['data']['count']
        # 获得正在佩戴的勋章（检查勋章墙第一个）
        first_info = response['data']['list'][0]
        if first_info['medal_info']['wearing_status'] == 1:
            wearing_medal['wearing_status'] = 1
            wearing_medal['target_name'] = first_info['target_name']
            wearing_medal['medal_name'] = first_info['medal_info']['medal_name']
            wearing_medal['medal_level'] = first_info['medal_info']['level']
        # 遍历勋章
        for info in response['data']['list']:
            medal_info = info['medal_info']
            # 直播状态
            if info['live_status'] == 1:
                live_status = '正在直播'
            else:
                live_status = ''
            # 写入表格
            table.add_row(
                [num, info['target_name'], medal_info['medal_name'], medal_info['level'],
                 str(medal_info['intimacy']) + '/' + str(medal_info['next_intimacy']),
                 str(medal_info['today_feed']) + '/' + str(medal_info['day_limit']), live_status])
            num += 1

        # 输出数据
        os.system('cls')
        print('目前共拥有粉丝勋章数：%d' % count)
        if wearing_medal['wearing_status'] == 1:
            print('目前正在佩戴的粉丝勋章：【' + wearing_medal['medal_name'] + str(wearing_medal['medal_level']) + '】 - ' + wearing_medal['target_name'])
        else:
            print('目前无佩戴粉丝勋章')
        print(table)

    else:
        print('请求失败！')
        print('状态码：%d' % response['code'])
        print('返回信息：%s' % response['message'])

    print('更新时间 %s' % update_time)

    run = input()
    if run != '':
        break
    else:
        print('更新中...')
