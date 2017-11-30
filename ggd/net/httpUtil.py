import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))

from ..log.logger import *
import requests
import csv

class HttpUtil:
    
    logger = None
    __instance = None

    #do singleton
    def __new__(clz):
        if not HttpUtil.__instance:
            HttpUtil.__instance = object.__new__(clz)        
        return HttpUtil.__instance

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)

    '''
    @param action: get or post
    @param resp: 回傳的資料處理方式，{"format": "csv", "encoding": "utf-8"}
    @param url: api路徑
    @param payload: 要送過去的參數，ex: a=xxx&b=ooo
    @param parser: parser object callback
    '''
    def getRemote(self, req, resp, url, payload, parser):
        self.logger.trace("do getRemote(), action: {}, resp: {}, url: {}, payload: {}", req, resp, url, payload)        
        res = None
        result = None
        with requests.Session() as s:
            if req["action"] == "get":
                res = requests.get(url, payload)
            elif req["action"] == "post":
                res = requests.post(url, payload)  

            format = resp["format"]
            if format == "csv":                
                result = parser(csv.reader(res))            
            elif format == "json":
                result = parser(res.json())        
            else:
                encoding = "utf-8" if resp["encoding"] is None else resp["encoding"]
                res.encoding = encoding
                result = parser(res.text)
        return result    

