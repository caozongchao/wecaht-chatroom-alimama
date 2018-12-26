import itchat
from datetime import datetime
import redis
import json
import requests
import io
import common
import re

class Sender():

    def __init__(self):
        itchat.auto_login(hotReload=True,loginCallback=self.loginCallback,exitCallback=self.exitCallback,enableCmdQR=2)
        self.redis = redis.Redis(host=common.conf['redisHost'],port=common.conf['redisPort'],db=0)
        self.imageStorage = None

    def sendToChatroom(self):
        itchat.get_chatrooms(update=True)
        chatrooms = itchat.search_chatrooms(common.conf['roomName'])
        # print(chatrooms)
        username = ''
        for chatroom in chatrooms:
            if chatroom['NickName'] == common.conf['roomName']:
                username = chatroom['UserName']
                break
        if username:
            # sendtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg = self.getMsg()
            if msg is not None:
                msg = json.loads(msg)
                image = self.getImage(msg['pict_url'])
                itchat.send_image(self.imageStorage,toUserName=username)
                s = self.getS(msg)
                itchat.send_msg(msg=s,toUserName=username)

    def loginCallback(self):
        print("成功登陆")

    def exitCallback(self):
        print("成功推出")

    def getMsg(self):
        return self.redis.spop('taobao')

    def getImage(self,imageUrl):
        r = requests.get(imageUrl, stream=True)
        self.imageStorage = io.BytesIO()
        for block in r.iter_content(1024):
            self.imageStorage.write(block)
        self.imageStorage.seek(0)

    def getS(self,msg):
        template = """【%s】
▪%s,折后价%s
▪%s前有效
▪口令：%s
▪链接：%s
【购物流程】
1.复制口令→打开手机app→领取→下单
2.复制链接→打开浏览器→粘贴链接并打开→领取→下单
"""
        taokouling_shortUrl = self.getTaokoulingAndShortUrl(msg['item_url'])
        s = template % (msg['title'],msg['coupon_info'],msg['zk_final_price'],msg['coupon_end_time'],taokouling_shortUrl[0],taokouling_shortUrl[1])
        return s

    def getTaokoulingAndShortUrl(self,itemUrl):
        itemId = re.search(r'id=(\d*)',itemUrl)[1]
        params = {'apkey':common.conf['key'],'itemid':itemId,'pid':common.conf['pid'],'tbname':common.conf['name'],'shorturl':str(1),'tpwd':str(1)}
        finalUrl = common.conf['couponUrl'] + common.parseUrl(params)
        response = requests.get(finalUrl)
        if response.status_code == 200:
            content = response.json()
            return [content['result']['data']['tpwd'],content['result']['data']['short_url']]

    def sendNotice(self):
        itchat.get_chatrooms(update=True)
        chatrooms = itchat.search_chatrooms(common.conf['roomName'])
        # print(chatrooms)
        username = ''
        for chatroom in chatrooms:
            if chatroom['NickName'] == common.conf['roomName']:
                username = chatroom['UserName']
                break
        if username:
            image = self.getImage('https://i.loli.net/2018/12/25/5c21c9c2e2965.jpg')
            itchat.send_image(self.imageStorage,toUserName=username)
            s = '关注公众号【轻松领券(qslingquan)】，可以通过输入链接查询指定宝贝的优惠券，全网查询最方便最快捷！'
            itchat.send_msg(msg=s,toUserName=username)

    def sendAlive(self):
        users = itchat.search_friends('己')
        userName= users[0]['UserName']
        itchat.send('I am alive',toUserName=userName)
