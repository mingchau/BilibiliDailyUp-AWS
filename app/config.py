import base64
import os

COIN_OR_NOT = True
# 是否投币
# 开启后如果硬币数量小于5默认也会跳过


SILVER2COIN_OR_NOT = True
# 是否将银瓜子兑换为硬币


STRICT_MODE = False
# 是否开启严格模式，严格模式会保证至少5次成功投币，因为官方投币API存在缺陷，会有投币成功但是返回失败的情况
# 默认开启严格模式，如果关闭则只会投币5次，无论成功失败，会出现少投币的情况，因为可能失败，但是不会造成浪费硬币的情况，自行选择

UID_LIST = ['473837611', '1131457022', '433587902', '2026561407', '50329118']
# 投币UP主的ID号,如果不修改，默认将用上面这个列表里的,可以选择自己喜欢的UP主
# 获取UID的方法见README.md
# 新华网 人民日报 央视频  王冰冰 英雄联盟赛事


temp = os.getenv("BILIBILI_COOKIES_BASE64", None)
if temp:
    temp += "=" * ((4 - len(temp) % 4) % 4)
    COOKIE_LIST = base64.urlsafe_b64decode(temp).decode().split('\r\n')
else:
    COOKIE_LIST = ['']

# Bilibili的COOKIE获取的方法见README.md

# 是否推送消息
PUSHPLUS_PUSH_OR_NOT = True
PUSHPLUS_TOKEN = os.getenv('PUSHPLUS_TOKEN', None)

# PUSH PLUS的TOKEN 官网为 https://www.pushplus.plus

SERVERCHAN_PUSH_OR_NOT = False
SERVERCHAN_TOKEN = os.getenv('SERVERCHAN_TOKEN', None)
