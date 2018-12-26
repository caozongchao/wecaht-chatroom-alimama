# -*- coding:utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from apscheduler.schedulers.background import BackgroundScheduler
from sender import Sender
from crawler import Crawler
import common

if __name__ == '__main__':

    #提前执行一次，因为apscheduler不会立即执行
    crawlerInstance = Crawler()
    crawlerInstance.flushRedis()
    crawlerInstance.reqHaoquan()

    senderInstance = Sender()
    senderInstance.sendToChatroom()

    #定时器
    scheduler = BlockingScheduler()
    #定时爬取品牌券
    scheduler.add_job(crawlerInstance.reqPinpai,'cron',hour=common.conf['crawlerPinpaiquanHour'])
    #定时爬取好券直播
    scheduler.add_job(crawlerInstance.reqHaoquan,'cron',hour=common.conf['crawlerHaoquanHour'])
    #定时发送优惠券
    scheduler.add_job(senderInstance.sendToChatroom,'cron',hour=common.conf['senderCouponHour'],minute=common.conf['senderCouponMinute'])
    #定时发布公告
    scheduler.add_job(senderInstance.sendNotice,'cron',hour=common.conf['senderNoticeHour'],minute=common.conf['senderNoticeMinute'])
    scheduler.add_job(senderInstance.sendAlive,'cron',hour=common.conf['senderAliveHour'],minute=common.conf['senderAliveMinute'])
    scheduler.start()
