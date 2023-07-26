import requests
import time
import prettytable
import os

# 获取正在直播的关注用户数据的api，其实最后还有一个时间戳参数但实测无用
url = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/xfetter/GetWebList'

# 登录状态cookies
my_cookies = {
    'Cookie': ''
}
# 在B站脚本文件夹中cookies.txt文件中获取cookies
with open('../cookies.txt', 'r') as f:
    # 避免文件末尾不小心出现空行，所以只读取一行
    my_cookies['Cookie'] = f.readline()

# 请求参数
page_size = 10  # 一页数据量

# 脚本运行模式
# 0：手动模式
# 1：自动模式
mode = 0

# 自动模式周期
period = 0

# 输出表格
table = prettytable.PrettyTable(['序号', '昵称', '分区', '房间名', '开播时长'])

while True:
    update_time = time.strftime('%H:%M:%S', time.localtime())    # 更新时间
    page = 1    # 请求起始页数
    num = 1     # 输出序号
    # 第一次请求（第一页）
    response = requests.get(url + '?page=' + str(page) + '&page_size=' + str(page_size), cookies=my_cookies).json()
    # 判断是否有效
    if response['code'] == 0:
        # 清空表格
        table.clear_rows()
        # 获取正在直播用户数量
        count = response['data']['count']
        # 计算需要请求的页数
        times = count // page_size + 1
        # 遍历第一页数据
        for info in response['data']['rooms']:
            # 计算开播时长
            live_time_h = info['live_time'] // 60 // 60
            live_time_m = info['live_time'] // 60 % 60
            live_time_s = info['live_time'] % 60
            if live_time_h == 0:
                live_time = str(live_time_m).zfill(2) + ':' + str(live_time_s).zfill(2)
            else:
                live_time = str(live_time_h) + ':' + str(live_time_m).zfill(2) + ':' + str(live_time_s).zfill(2)
            table.add_row([num, info['uname'], info['area_v2_name'], info['title'], live_time])
            num += 1
        page += 1
        # 从第二页开始继续请求完剩下的
        for i in range(times - 1):
            response = requests.get(url + '?page=' + str(page) + '&page_size=' + str(page_size),
                                    cookies=my_cookies).json()
            # 遍历本页数据
            for info in response['data']['rooms']:
                # 计算开播时长
                live_time_h = info['live_time'] // 60 // 60
                live_time_m = info['live_time'] // 60 % 60
                live_time_s = info['live_time'] % 60
                if live_time_h == 0:
                    live_time = str(live_time_m).zfill(2) + ':' + str(live_time_s).zfill(2)
                else:
                    live_time = str(live_time_h) + ':' + str(live_time_m).zfill(2) + ':' + str(live_time_s).zfill(2)
                table.add_row([num, info['uname'], info['area_v2_name'], info['title'], live_time])
                num += 1
            page += 1
        # 输出数据
        os.system('cls')
        print('关注列表中当前正在直播人数：%d' % count)
        print(table)
    else:
        os.system('cls')
        print('请求失败！')
        print('状态码：%d' % response['code'])
        print('返回消息：' + response['message'])
    print('更新时间 %s' % update_time)

    # 手动模式
    if mode == 0:
        run = input()
        print(run)
        # 输入任意值进入自动模式，无输入则视为手动更新
        if run != '':
            mode = 1
            os.system('cls')
            print('即将进入自动模式')
            period = int(input('请输入自动更新周期（单位：秒）：'))
        else:
            print('更新中...')
    # 自动模式
    elif mode == 1:
        time.sleep(period)
