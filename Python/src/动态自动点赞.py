import random
import requests
import time


# 配置区
update_period = 30  # 更新周期，单位：秒
fixed_delay = 10  # 点赞延迟，单位：秒，过小可能会导致账号异常
max_random_delay = 3  # 最大随机延迟，单位：秒
max_try_times = 3  # 最大尝试次数
# 白名单，若不为空则只点赞白名单内的人的动态
white_list = []
# 黑名单，若不为空则不点赞黑名单内的人的动态，黑名单与白名单冲突时黑名单优先
black_list = []

# 动态更新api（update_baseline=0）
check_update_url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all/update?type=all&update_baseline=0'
# 动态详情api（update_baseline=0）
get_dynamic_url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&update_baseline=0&page=1&features=itemOpusStyle'
# 点赞api
dynamic_like_url = 'https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/thumb'

# 点赞数据
like_data = {
    'dynamic_id': '',
    'up': '1',  # 1点赞，2取消
    'csrf': '',
}
# 登录状态cookies
my_cookies = {
    'Cookie': ''
}

# 在B站脚本文件夹中cookies.txt文件中获取cookies
with open('../cookies.txt', 'r') as f:
    # 避免文件末尾不小心出现空行，所以只读取一行
    my_cookies['Cookie'] = f.readline()

# 获取csrf（暂时不需要，经测试不带csrf请求也行）
# with open('../csrf.txt', 'r') as f:
#     # 避免文件末尾不小心出现空行，所以只读取一行
#     like_data['csrf'] = f.readline()

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
                time.sleep(fixed_delay)  # 延时一下再开始点赞
                time.sleep(random.random() * max_random_delay)  # 随机延迟
                # 读取新动态
                for i in range(update_num):
                    new_dynamic_info = dynamic_info[i]
                    uid = new_dynamic_info['modules']['module_author']['mid']  # 发布者uid
                    name = new_dynamic_info['modules']['module_author']['name']  # 发布者昵称
                    # 如果白名单不为空
                    if white_list:
                        # 判断是否在白名单
                        if uid not in white_list:
                            break
                    # 如果黑名单不为空
                    if black_list:
                        # 判断是否在黑名单中
                        if uid in black_list:
                            break
                    # 满足点赞条件发送点赞请求
                    like_data['dynamic_id'] = int(new_dynamic_info['id_str'])  # 动态id
                    response = requests.post(dynamic_like_url, data=like_data, cookies=my_cookies).json()
                    if response['code'] == 0:
                        like_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        print(f'{like_time} 成功为 {name}[{uid}] 点赞')
                    else:
                        print('点赞请求失败！')
                        print(f"状态码：{response['code']}")
                        print(f"返回信息：{response['message']}")
                    # 要点赞的动态数量大于1时为了防止点赞频率过高被判定账号异常需要加延迟
                    if update_num > 1:
                        time.sleep(fixed_delay)
                        time.sleep(random.random() * max_random_delay)  # 随机延迟
            else:
                print('详情请求失败！')
                print(f"状态码：{response['code']}")
                print(f"返回信息：{response['message']}")
    else:
        print('更新请求失败！')
        print(f"状态码：{response['code']}")
        print(f"返回信息：{response['message']}")

    time.sleep(update_period)
