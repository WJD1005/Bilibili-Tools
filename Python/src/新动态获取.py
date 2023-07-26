import requests
import time


update_period = 20  # 更新周期，单位：秒

# 动态更新api（update_baseline=0）
check_update_url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all/update?type=all&update_baseline=0'
# 动态详情api（update_baseline=0）
get_dynamic_url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&update_baseline=0&page=1&features=itemOpusStyle'

# 登录状态cookies
my_cookies = {
    'Cookie': ''
}
# 在B站脚本文件夹中cookies.txt文件中获取cookies
with open('../cookies.txt', 'r') as f:
    # 避免文件末尾不小心出现空行，所以只读取一行
    my_cookies['Cookie'] = f.readline()

while True:
    # 查询是否有更新
    response = requests.get(check_update_url, cookies=my_cookies).json()
    if response['code'] == 0:
        # 请求成功
        update_num = response['data']['update_num']
        if update_num != 0:
            # 获取动态详情
            response = requests.get(get_dynamic_url, cookies=my_cookies).json()
            if response['code'] == 0:
                # 请求成功
                dynamic_info = response['data']['items']
                # 读取新动态
                for i in range(update_num):
                    new_dynamic_info = dynamic_info[i]['modules']
                    # 处理信息
                    pub_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(new_dynamic_info['module_author']['pub_ts']))  # 发布时间
                    author = new_dynamic_info['module_author']['name']  # 发布者
                    pub_action = new_dynamic_info['module_author']['pub_action']  # 发布行为（纯动态、视频、番剧、专栏）
                    if new_dynamic_info['module_dynamic']['desc']:
                        text = new_dynamic_info['module_dynamic']['desc']['text']  # 文本
                        text = f'\n{text}'  # 由于有可能为空自己带换行方便排版
                    else:
                        text = ''
                    # 纯动态
                    if pub_action == '':
                        print(f'{pub_time}\n{author}{text}\n')
                    # 视频
                    elif pub_action == '投稿了视频' or pub_action == '投稿了直播回放' or pub_action == '发布了动态视频':
                        title = new_dynamic_info['module_dynamic']['major']['archive']['title']
                        print(f'{pub_time}\n{author} {pub_action}：{title}{text}\n')
                    # 番剧
                    elif pub_action == '更新了':
                        title = new_dynamic_info['module_dynamic']['major']['pgc']['title']
                        print(f'{pub_time}\n{author} {pub_action}：{title}\n')
                    # 专栏
                    elif pub_action == '投稿了文章':
                        title = new_dynamic_info['module_dynamic']['major']['opus']['title']
                        summary_text = new_dynamic_info['module_dynamic']['major']['opus']['summary']['text']
                        print(f'{pub_time}\n{author} {pub_action}：{title}\n{summary_text}\n')
                    else:
                        print(f'{pub_time}\n{author} 不明类型动态{text}\n')
            else:
                print('详情请求失败！')
                print(f"状态码：{response['code']}")
                print(f"返回信息：{response['message']}")
    else:
        print('更新请求失败！')
        print(f"状态码：{response['code']}")
        print(f"返回信息：{response['message']}")

    time.sleep(update_period)
