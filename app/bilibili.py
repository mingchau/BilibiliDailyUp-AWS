import random
import time

import requests as requests

import api
import config
import data
import push
import utools


class Bilibili:
    def __init__(self):
        self.log = ''
        self.session = requests.Session()

    @staticmethod
    def exchange_cookie(cookies) -> dict:
        return dict([cookie.split("=", 1) for cookie in cookies.split("; ")])

    def get_code(self, cookies) -> int:
        cookies = Bilibili.exchange_cookie(cookies)
        response = self.session.get(url=api.coin_url, cookies=cookies).json()
        flag = response['code']
        if flag == 0:
            return 1
        return 0

    def get_money(self, cookies) -> int:
        cookies = Bilibili.exchange_cookie(cookies)
        response = self.session.get(url=api.coin_url, headers=data.headers, cookies=cookies).json()
        money = response['data']['money']
        if money is None:
            return 0
        else:
            return money

    @staticmethod
    def get_csrf(cookies: str) -> str:
        cookies = Bilibili.exchange_cookie(cookies)
        bili_jct = cookies['bili_jct']
        return bili_jct

    def log_message(self, message: str) -> None:
        formatted_message = f'{message}</br>'
        self.log = f'{self.log}{formatted_message}'

    def get_info(self, cookies: str) -> tuple:
        cookies = Bilibili.exchange_cookie(cookies)
        response = self.session.get(url=api.inquire_url,
                                    cookies=cookies).json()
        login = response['data']['login']
        watch = response['data']['watch']
        coins = response['data']['coins']
        share = response['data']['share']
        email = response['data']['email']
        tel = response['data']['tel']
        safe_question = response['data']['safe_question']
        identify_card = response['data']['identify_card']
        info1 = [login, watch, coins, share]
        info2 = [email, tel, safe_question, identify_card]
        return info1, info2

    def log_head(self, cookies: str) -> None:
        cookies = Bilibili.exchange_cookie(cookies)
        response = self.session.get(url=api.info_url,
                                    cookies=cookies).json()
        mid = response['data']['mid']
        name = response['data']['name']
        level = response['data']['level']
        current_exp = response['data']['level_exp']['current_exp']
        next_exp = response['data']['level_exp']['next_exp']
        diff_exp = next_exp - current_exp
        days = int(diff_exp / 65)
        coins = response['data']['coins']
        vip_status = response['data']['vip']['status']
        vip_due_date = response['data']['vip']['due_date']
        vip_due_date = utools.formate_time(vip_due_date)
        if vip_status:
            message = f"用户{name},uid为{mid}您是大会员,大会员到期时间为{vip_due_date},你目前的等级是{level}级,目前的经验{current_exp},离下个等级还差{diff_exp}经验,需要{days}天剩余硬币还有{coins}个"
            self.log_message(
                f"用户名:{name}</br>uid:{mid}</br>VIP:大会员</br>到期时间:{vip_due_date}</br>目前的等级:{level}级</br>目前的经验:{current_exp}</br>离下个等级:{diff_exp}经验<br>距升级还差:{days}天</br>剩余硬币数:{coins}个")
            utools.formate_print(message)
        else:
            message = f"用户{name},uid为{mid}您的大会员已过期,过期时间为{vip_due_date},你目前的等级是{level}级,目前的经验{current_exp},离下个等级还差{diff_exp}经验,需要{days}天,剩余硬币还有{coins}个"
            self.log_message(
                f"用户名:{name}</br>uid:{mid}</br>VIP:非大会员</br>过期时间:{vip_due_date}</br>目前的等级:{level}级</br>目前的经验:{current_exp}</br>离下个等级:{diff_exp}经验<br>距升级还差:{days}天</br>剩余硬币数:{coins}个")
            utools.formate_print(message)

    def get_video_list(self, cookies) -> list:
        uid_list = config.UID_LIST
        video_list_headers = data.video_list_headers
        video_list_headers['cookie'] = cookies
        response = self.session.get(url=api.get_video_list_url.format(random.choice(uid_list)),
                                    headers=video_list_headers).json()
        video_list = response['data']['list']['vlist']
        return video_list

    def watch_video(self, bvid: str, cookies: str) -> None:
        random_play_time = random.randint(30, 60)
        data.watch_video_data['bvid'] = bvid
        data.watch_video_data['played_time'] = str(random_play_time)
        data.watch_video_data['csrf'] = Bilibili.get_csrf(cookies)
        cookies = Bilibili.exchange_cookie(cookies)
        response = self.session.post(url=api.watch_video_url,
                                     data=data.watch_video_data,
                                     cookies=cookies).json()
        code = response['code']
        if code == 0:
            utools.formate_print('看视频完成')
        else:
            utools.formate_print('看视频失败')

    def share_video(self, bvid: str, cookies: str) -> None:
        data.share_video_data['bvid'] = bvid
        data.share_video_data['csrf'] = Bilibili.get_csrf(cookies)
        cookies = Bilibili.exchange_cookie(cookies)
        response = self.session.post(url=api.share_video_url,
                                     data=data.share_video_data,
                                     cookies=cookies,
                                     headers=data.headers).json()
        code = response['code']
        if code == 0:
            utools.formate_print('分享视频成功')
        else:
            utools.formate_print('分享视频失败')

    def coin_video(self, aid: str, cookies: str) -> int:
        cookies_dict = Bilibili.exchange_cookie(cookies)
        insert_coin_data = data.insert_coin_data
        insert_coin_headers = data.insert_coin_headers
        insert_coin_data['aid'] = aid
        insert_coin_data['csrf'] = Bilibili.get_csrf(cookies)
        insert_coin_headers['cookie'] = cookies
        response = self.session.post(url=api.insert_coins_url,
                                     headers=data.insert_coin_headers,
                                     data=insert_coin_data,
                                     cookies=cookies_dict).json()
        like = response['data']['like']
        if like:
            utools.formate_print('投币成功')
            return 1
        else:
            utools.formate_print('投币失败')
            return 0

    @staticmethod
    def random_video_para(video_list: list) -> tuple:
        random_index = random.randint(0, len(video_list) - 1)
        bvid = video_list[random_index]['bvid']
        title = video_list[random_index]['title']
        author = video_list[random_index]['author']
        aid = video_list[random_index]['aid']
        return bvid, title, author, aid

    def random_coin_video(self, cookies: str) -> int:
        video_list = self.get_video_list(cookies)
        bvid, title, author, aid = Bilibili.random_video_para(video_list)
        utools.formate_print(f'开始向{author}的视频{title}投币……')
        coin_video_flag = self.coin_video(aid, cookies)
        return coin_video_flag

    def live_sign(self, cookies: str) -> None:
        response = self.session.get(url=api.live_sign_url,
                                    cookies=Bilibili.exchange_cookie(cookies)).json()
        if response['code'] == 0:
            text = response['data']['text']
            had_sign_days = response['data']['hadSignDays']
            self.log_message(
                '直播签到:签到成功,签到天数为{}'.format(had_sign_days))
            utools.formate_print(f'签到奖励:{text},连续签到{had_sign_days}天')
            self.log_message(
                f'签到奖励:{text},连续签到{had_sign_days}天')
        else:
            utools.formate_print('直播签到:当天已签到~')
            self.log_message('直播签到:当天已签到')

    def get_silver(self, cookies: str) -> bool:
        response = self.session.get(url=api.live_info_url, cookies=Bilibili.exchange_cookie(
            cookies)).json()
        self.log_message(f'银瓜子数量:{response["data"]["silver"]}')
        utools.formate_print(f'银瓜子数量:{response["data"]["silver"]}')
        if response['data']['silver'] > 700:
            return True
        return False

    def silver_to_coin(self, cookies: str) -> None:
        silver2coin_data = data.silver2coin_data
        silver2coin_data['csrf'] = Bilibili.get_csrf(cookies)
        silver2coin_data['csrf_token'] = Bilibili.get_csrf(cookies)
        response = self.session.post(url=api.silver2coin_url,
                                     cookies=Bilibili.exchange_cookie(cookies),
                                     data=silver2coin_data).json()
        if response['code'] == 0:
            silver = response['data']['silver']
            utools.formate_print('银瓜子兑换:成功!')
            utools.formate_print(f'银瓜子剩余:{silver}个')
            self.log_message('银瓜子兑换:成功!')
            self.log_message(f'银瓜子剩余:{silver}个')
        else:
            utools.formate_print('银瓜子兑换:当天已兑换!')
            self.log_message('银瓜子兑换:当天已兑换!')

    def start_tasks(self, cookies: str) -> None:
        code = self.get_code(cookies)
        if code:
            money = self.get_money(cookies)
            utools.formate_print('cookie有效即将开始查询任务……')
            utools.formate_print('=========以下是任务信息=========')
            self.log_message('=========以下是任务信息=========')
            info = self.get_info(cookies)
            info_1, info_2 = info
            for k, j in enumerate(info_1):
                if k == 0:
                    utools.formate_print('登录任务已完成') if j else utools.formate_print(
                        '登录任务未完成')
                    self.log_message('每日登录:已完成~获得5点经验值')
                elif k == 1:
                    if j:
                        utools.formate_print('观看视频任务已完成')
                        self.log_message('观看视频:已完成~获得5点经验值')
                    else:
                        utools.formate_print('观看视频任务未完成,即将开始观看视频任务……')
                        vlist = self.get_video_list(cookies)
                        bvid, title, author, aid = Bilibili.random_video_para(vlist)
                        utools.formate_print(f'开始观看作者{author}的视频{title}……')
                        self.watch_video(bvid, cookies)
                        utools.formate_print('观看视频任务已完成，即将开始下一个任务……')
                        self.log_message('观看视频:完成~获得5点经验值')
                elif k == 2:
                    if config.COIN_OR_NOT and money >= 5:
                        if j == 50:
                            utools.formate_print('投币任务已完成')
                            self.log_message('每日投币:已完成~获得50点经验值')
                        else:
                            utools.formate_print('投币任务未完成,即将开始投币任务')
                            num = int((50 - j) / 10)
                            for i in range(0, num):
                                temp = 0
                                if config.STRICT_MODE:
                                    while 1:
                                        coin_flag = self.random_coin_video(
                                            cookies)
                                        temp += 1
                                        if coin_flag or temp == 5:
                                            break
                                        time.sleep(2)
                                else:
                                    self.random_coin_video(cookies)
                                    time.sleep(2)
                                time.sleep(1)
                            utools.formate_print('投币任务已完成，即将开始下一个任务……')
                            self.log_message('每日投币:完成~获得50点经验值')
                    else:
                        utools.formate_print('投币任务已跳过')
                        self.log_message('每日投币:跳过~')
                else:
                    if j:
                        utools.formate_print('分享任务已完成')
                        self.log_message('每日分享:已完成~获得5点经验值')
                    else:
                        utools.formate_print('分享任务未完成,即将开始分享任务……')
                        vlist = self.get_video_list(cookies)
                        bvid, title, author, aid = Bilibili.random_video_para(
                            vlist)
                        utools.formate_print(f'开始分享{author}的视频{title}……')
                        self.share_video(bvid, cookies)
                        utools.formate_print('分享任务已完成,日常任务已全部完成!即将查询额外任务……')
                        self.log_message('每日分享:完成~获得5点经验值')
                        time.sleep(1)
            utools.formate_print('==========以下是额外任务==============')
            self.log_message('=========以下是额外任务=========')
            for k, j in enumerate(info_2):
                if k == 0:
                    if j:
                        utools.formate_print('绑定邮箱任务已完成')
                        self.log_message('绑定邮箱:已完成')
                    else:
                        utools.formate_print('绑定邮箱任务未完成,完成可以获得20点经验值~')
                        self.log_message('绑定邮箱:未完成~完成可获得20点经验')
                elif k == 1:
                    if j:
                        utools.formate_print('绑定手机任务已完成')
                        self.log_message('绑定手机:已完成')
                    else:
                        utools.formate_print('绑定手机任务未完成,完成可以获得100点经验值~')
                        self.log_message('绑定手机:未完成~完成可获得20点经验')
                elif k == 2:
                    if j:
                        utools.formate_print('设置密保任务已完成')
                        self.log_message('密保任务:已完成')
                    else:
                        utools.formate_print('设置密保任务未完成,完成可以获得30点经验值~')
                        self.log_message('密保任务:未完成~完成可获得30点经验')
                else:
                    if j:
                        utools.formate_print('实名认证任务已完成')
                        self.log_message('实名认证:已完成')
                    else:
                        utools.formate_print('实名认证任务未完成,完成可以获得50点经验值~')
                        self.log_message('实名认证:未完成~完成可获得50点经验')
            utools.formate_print('==========以下是直播任务==============')
            self.log_message('=========以下是直播任务=========')
            self.live_sign(cookies)
            if config.SILVER2COIN_OR_NOT and self.get_silver(cookies):
                self.silver_to_coin(cookies)
            else:
                self.log_message('银瓜子转换币:跳过~')
                utools.formate_print('银瓜子兑换:跳过~')
            self.log_message('=========以下是个人信息=========')
            utools.formate_print('=========以下是个人信息=========')
            self.log_head(cookies)
        else:
            utools.formate_print('cookie已失效,任务停止,请更换新的cookie!')
            self.log_message('cookie已失效,任务停止,请更换新的cookie!')
        utools.formate_print('==========分割线==============')

    def go(self) -> None:
        if len(config.COOKIE_LIST[0]) == 0:
            utools.formate_print('未添加cookie')
            return
        utools.formate_print(f'成功添加{len(config.COOKIE_LIST)}个cookie,开始任务……')
        for j, k in enumerate(config.COOKIE_LIST):
            self.log_message(f'=========这是第{j + 1}个账号=========')
            utools.formate_print(f'正在签到第{j + 1}个账号……')
            self.start_tasks(k)
            time.sleep(1)
        if config.SERVERCHAN_PUSH_OR_NOT:
            push.serverchan_push(config.SERVERCHAN_TOKEN, self.log)
        if config.PUSHPLUS_PUSH_OR_NOT:
            push.pushplus_push(config.PUSHPLUS_TOKEN, self.log)
