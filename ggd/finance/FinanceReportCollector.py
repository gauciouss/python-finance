# -*- encoding: utf8-*-
from ggd.log.logger import *
from ggd.net.httpUtil import *
from bs4 import BeautifulSoup
import datetime

'''
財務季報收集者
'''
class FinanceSeasonReportCollector:

    logger = None
    httpUtil = None
    url = "http://mops.twse.com.tw/mops/web/ajax_t05st30_c?TYPEK=all&step=1&firstin=1&off=1&queryName=co_id&t05st29_c_ifrs=N&t05st30_c_ifrs=N&isnew=false&co_id={}&year={}"

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)
        self.httpUtil = HttpUtil()

    def getData(self, *args):
        u = self.url.format(args[0], args[1])
        req = {"action": "get"}
        resp = {"format": "", "encoding": "utf-8"}
        self.httpUtil.getRemote(req, resp, u, "", self.doParser)

    def doParser(self, html):
        sp = BeautifulSoup(html, "html.parser")
        warn = sp.select("font[color=red]")
        if len(warn) is not 0:
            return None

        tr_even = sp.select("tr.even")
        tr_odd = sp.select("tr.odd")

        trs = tr_even + tr_odd
        rangeTRS = range(0, len(trs))


        result = {
            "cost_of_goods_sold": {},
            "operating_expenses": {},
            "non_op_income": {},
            "EPS": {},
            "pre_tex_income": {},
            "net_sales": {},
            "gross_profit": {},
            "non_op_exp": {},
            "income_tex_expense": {},
            "operating_income": {}
        }

        def seasonLoop(key, tr, unit=1):
            vals = {}
            for season in range(1, 5):
                # 資料單位是1000元
                # val = float(tr.select("td")[season].text.strip().replace(",", "")) * unit
                tx = tr.select("td")[season].text.strip()
                val = tx if tx != "" else 0
                if isinstance(val, int) == False:
                    val = float(val.replace(",", ""))
                self.logger.debug("key: {}, value: {}", key, str(val))
                vals.update({"s" + str(season): val})
            result[key] = vals


        for r in rangeTRS:
            title = trs[r].find("td").text

            self.logger.debug("title:" + title)
            if title == "營業成本":
                seasonLoop("cost_of_goods_sold", trs[r])
            elif title == "營業費用" or title == "營業支出":
                seasonLoop("operating_expenses", trs[r])
            elif title == "營業外收入及利益":
                seasonLoop("non_op_income", trs[r])
            elif title == "基本每股盈餘":
                seasonLoop("EPS", trs[r], 1)
            elif title == "繼續營業單位稅前淨利(淨損)":
                seasonLoop("pre_tex_income", trs[r])
            elif title == "營業收入":
                seasonLoop("net_sales", trs[r])
            elif title == "營業毛利(毛損)":
                seasonLoop("gross_profit", trs[r])
            elif title == "營業外費用及損失":
                seasonLoop("non_op_exp", trs[r])
            elif title == "所得稅費用（利益）":
                seasonLoop("income_tex_expense", trs[r])
            elif title == "營業淨利(淨損)":
                seasonLoop("operating_income", trs[r])

        # 計算net_income
        nis = {}
        for season in range(1, 5):
            ni = int(result["pre_tex_income"]["s" + str(season)]) - int(result["income_tex_expense"]["s" + str(season)])
            nis.update({"s" + str(season): ni})
        result["net_income"] = nis
        self.logger.debug("{}", result)
        return result



#a = FinanceSeasonReportCollector()
#a.getData("1409", "95")
