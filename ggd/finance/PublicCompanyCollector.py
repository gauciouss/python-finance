# -*- encoding: utf8-*-
from ggd.log.logger import *
from ggd.net.httpUtil import *
from bs4 import BeautifulSoup


'''
取得上市公司列表
'''
class PublicCompanyCollector:

    logger = None
    httpUtil = None
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)
        self.httpUtil = HttpUtil()

    def getData(self):
        result = self.httpUtil.getRemote(req = {"action": "get"}, resp={"format": "html", "encoding": "cp950"}, url=self.url, payload="", parser=self.parse)

    def parse(self, html):
        #self.logger.debug("{}", html)
        soup = BeautifulSoup(html, "html.parser")
        trs = soup.select("table.h4 > tr")

        for i in range(3, len(trs)):
            td = trs[i].select("td:nth-of-type(1)")
            text = td[0].get_text()
            rs = text.split("　");
            if len(rs) == 2:
                print("stk no: " + rs[0])
                print("stk name: " + rs[1])








collector = PublicCompanyCollector();
collector.getData()
