import requests
import json
import redis
import common

class Crawler():

    def __init__(self):
        self.redis = redis.Redis(host=common.conf['redisHost'],port=common.conf['redisPort'],db=0)
        self.pids = common.conf['pid'].split('_')
        self.pid3 = self.pids[3]
        self.pid2 = self.pids[2]

    def reqHaoquan(self):
        self.flushRedis()
        params = {'apkey':common.conf['key'],'adzoneid':self.pid3, 'siteid':self.pid2, 'tbname':common.conf['name'],'pagesize':common.conf['pagesize']}
        finalUrl = common.conf['haoquanUrl'] + common.parseUrl(params)
        self.doRequest(finalUrl)

    def reqPinpai(self):
        self.flushRedis()
        params = {'apkey':common.conf['key'],'adzoneid':self.pid3, 'siteid':self.pid2, 'tbname':common.conf['name'],'pagesize':common.conf['pagesize']}
        finalUrl = common.conf['pinpaiquanUrl'] + common.parseUrl(params)
        self.doRequest(finalUrl)

    def flushRedis(self):
        self.redis.flushdb()

    def doRequest(self,url):
        response = requests.get(url)
        if response.status_code == 200:
            content = response.json()
            for i in content['data']:
                self.redis.sadd('taobao',json.dumps(i))