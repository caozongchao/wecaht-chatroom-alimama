
conf = {
    #淘宝客接口相关配置
    'key':'',
    'pid':'',
    'name':'',
    'pagesize':'100',
    #好券直播
    'haoquanUrl':'',
    #品牌券
    'pinpaiquanUrl':'',
    #通过itemid获取淘口令和短链
    'couponUrl':'',

    #群聊名称
    'roomName':'淘宝天猫精选优惠券',

    #redis配置
    'redisHost':'127.0.0.1',
    'redisPort':'6379',

    #爬虫定时设置
    #品牌券
    'crawlerPinpaiquanHour':'8,16',
    #好券直播
    'crawlerHaoquanHour':'12,20',

    #群发消息定时设置
    #发送优惠券定时
    'senderCouponHour':'8-21',
    'senderCouponMinute':'*/18',
    #发送公告定时
    'senderNoticeHour':'8-21',
    'senderNoticeMinute':'15',
    #类似心跳包，避免晚上掉线
    'senderAliveHour':'22-23,0-7',
    'senderAliveMinute':'*/10',
}

#将dict解析为url参数
def parseUrl(data={}):
    item = data.items()
    urls = '?'
    for i in item:
        (key,value) = i
        temp_str = key + '=' + value
        urls = urls + temp_str+"&"
    urls = urls[:len(urls)-1]
    return urls
