import json

import requests

def serverchan_push(token, content, title='Bilibili助手提醒', channel=9):
    url = f'https://sctapi.ftqq.com/{token}.send'
    data = {
        "title": title,
        "desp": content,
        "channel": channel
    }
    # body = json.dumps(data).encode(encoding='utf-8')
    # headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data)
    print(response.content.decode('utf-8'))
    if response.status_code == 200:
        return 1
    return 0


def pushplus_push(token, content, title='Bilibili助手提醒', template='markdown'):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=body, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return 1
    return 0
