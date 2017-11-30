#_*_ coding: UTF-8 _*_
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))

from ..log.logger import Logger
from ..log.logger import LoggerFactory
from bs4 import BeautifulSoup
import datetime


class ParserFactory:

    logger = None
    __instance = None

    #do singleton
    def __new__(clz):
        if not Parser.__instance:
            Parser.__instance = object.__new__(clz)        
        return Parser.__instance

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)


    def getParser(self, url):
        return None

class StkHistoryQuoteParser:

    '''
    parse 證券歷史報價資訊， http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=19960701&stockNo=2330
    @date 起始日期 yyyyMMdd
    @stkNo 證券代碼
    '''
    def doParser(self, stkId, date, data):
        self.logger.debug("parse data: {}", data)
        result = []
        if "data" in data:
            list = data["data"]
            if list is not None and len(list) > 0:
                for obj in list:
                    pd = str(obj[0]).split("/")
                    year = int(pd[0]) + 1911
                    date = datetime.date(year, int(pd[1]), int(pd[2]))
                    distance = obj[7].replace("+", "")
                    quantity = obj[8].replace(",", "")
                    open_price = obj[3]
                    high_price = obj[4]
                    low_price = obj[5]
                    close_price = obj[6]
                    result.append({
                        "stk_id": stkId,
                        "quote_date": date,
                        "open_price": open_price,
                        "high_price": high_price,
                        "low_price": low_price,
                        "close_price": close_price,
                        "quote_date": str(date),
                        "quantity": quantity,
                        "distance": distance
                    })
        return result

class CompInfoParser:
    '''
    parse 上市公司基本資料, http://dts.twse.com.tw/opendata/t187ap03_L.csv
    '''
    def doParser(self, csv):
        #TODO
        self.logger.trace("START. parse comp info csv")
        for row in csv:
            self.logger("row: {}", row)



class CompSeasonFinanceReport:
    '''
    parse 上市公司季報, http://mops.twse.com.tw/mops/web/ajax_t05st30_c?TYPEK=all&step=1&firstin=1&off=1&queryName=co_id&t05st29_c_ifrs=N&t05st30_c_ifrs=N&isnew=false&co_id=2330&year=95
    '''
    def doParser(self, stkId, year):
        return  None