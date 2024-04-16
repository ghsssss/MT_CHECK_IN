import requests
from lxml import etree
import re
import os
import json
import notify

# MT首页地址
URL = 'https://kp.m-team.cc/api/fun/first'
# 从环境变量中获取cookie
cookie = os.environ.get('MT_COOKIE')
# 构造请求头
HEADERS = {
    'authority': 'kp.m-team.cc',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
    'Cookie': cookie,
    'Host':'kp.m-team.cc'
}

# 获取投票id
def get_voId():
    response = requests.post(URL, headers=HEADERS)
    # 判断请求是否成功
    if response.status_code == 200:
        # 获取投票id
        return response.json().get('data').get('fun').get('id')
    else:
        # 请求失败，发送通知
        notify.dingding_bot('MT投票', f"请求失败，状态码：{response.status_code}，错误信息：{response.json().get('message')}")
        return None

# 主函数


def main():
    # 获取投票id
    voId = get_voId()
    print(voId)
    # 构造投票请求
    url = "https://kp.m-team.cc/api/fun/vote"
    # 发送投票请求
    response = requests.post(url,{'Id':voId},headers=HEADERS)
    # 判断请求是否成功
    if response.status_code == 200:
        # 请求成功，发送通知
        print('本日投票成功！')
        notify.dingding_bot('MT投票', '本日投票成功！')
    else:
        print('投票失败！')
        # 请求失败，发送通知
        notify.dingding_bot('MT投票', f"请求失败，状态码：{response.status_code}，错误信息：{response.json().get('message')}")
          


if __name__ == "__main__":
    main()
