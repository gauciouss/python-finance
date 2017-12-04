# -*- encoding: utf8-*-
from ggd.log.logger import *
from ggd.net.httpUtil import *
from bs4 import BeautifulSoup

class StkQuoteCollector:

    logger = None
    httpUtil = None
    url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={}&stockNo={}"

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)
        self.httpUtil = HttpUtil()

    def getData(self, *args):

        return None

    def doParser(self, html):
        return None
