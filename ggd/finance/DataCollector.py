# -*- encoding: utf-8 -*-
from ggd.net.httpUtil import *
import abc
from bs4 import BeautifulSoup

class Collector(abc.ABC):

    logger = None
    httpUtil = None

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)
        self.httpUtil = HttpUtil()

    def collect(self, args):
        self.logger.trace("args: {}", args)
        payload = self.httpUtil.getRemote(args)
        vos = self.parse(payload)
        self.save2db(vos)

    @abc.abstractclassmethod
    def parse(self, payload):
        return NotImplemented

    @abc.abstractclassmethod
    def save2db(self, vos):
        return NotImplemented


class PublicCompanyCollector(Collector):

    def parse(self, payload):
        result = {}
        soup = BeautifulSoup(payload, "html.parser")
        trs = soup.select("table.h4 > tr")

        for i in range(3, len(trs)):
            td = trs[i].select("td:nth-of-type(1)")
            text = td[0].get_text()
            rs = text.split("　")
            if len(rs) == 2:
                result[rs[0]] = rs[1]

        return result

    def save2db(self, vos):
        return ""