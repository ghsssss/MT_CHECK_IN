import requests
from lxml import etree
import re
import os
import json

# 常量提取
URL = 'https://kp.m-team.cc/'
cookie = os.environ.get("MT_COOKIE")
HEADERS = {
    'authority': 'kp.m-team.cc',
    'cookie': cookie,
    'dnt': '1',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55"
}


def get_element():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        # pushplus_bot('MT投票', "请求MT首页成功!")
        return etree.HTML(response.text)
    else:
        pushplus_bot('MT投票', f"请求失败，状态码：{response.status_code}")
        return None


def main():
    root = get_element()
    if root is not None:
        element = root.xpath('//*[@id="fun"]')
        if element:
            btn = etree.tostring(element[0]).decode()
            match = re.search(r'funvote\((\d+),', btn)
            if match:
                number = int(match.group(1))
                url = f"https://kp.m-team.cc/fun.php?action=vote&id={number}&yourvote=fun"
                response = requests.get(url, headers=HEADERS)
                if response.status_code == 200:
                    pushplus_bot('MT投票', '投票成功')
                else:
                    pushplus_bot('MT投票', f"请求失败，状态码：{response.status_code}")
            else:
                pushplus_bot('MT投票', '未找到相应的投票码')
        else:
            # print("已投票")
            pushplus_bot('MT投票', '已投票')


def pushplus_bot(title: str, content: str) -> None:
    """
    通过 push+ 推送消息。
    """
    if not os.environ.get("PUSH_PLUS_TOKEN"):
        print("PUSHPLUS 服务的 PUSH_PLUS_TOKEN 未设置!!\n取消推送")
        return
    print("PUSHPLUS 服务启动")

    url = "http://www.pushplus.plus/send"
    data = {
        "token": os.environ.get("PUSH_PLUS_TOKEN"),
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=body, headers=headers).json()

    if response["code"] == 200:
        print("PUSHPLUS 推送成功！")

    else:
        url_old = "http://pushplus.hxtrip.com/send"
        headers["Accept"] = "application/json"
        response = requests.post(
            url=url_old, data=body, headers=headers).json()

        if response["code"] == 200:
            print("PUSHPLUS(hxtrip) 推送成功！")

        else:
            print("PUSHPLUS 推送失败！")


if __name__ == "__main__":
    main()
