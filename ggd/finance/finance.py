import os
import sys
import csv
from ggd.log.logger import LoggerFactory
from ggd.net.httpUtil import HttpUtil

class Finance:
    
    logger = None
    __instance = None

    #do singleton
    def __new__(clz):
        if not Finance.__instance:
            Finance.__instance = object.__new__(clz)        
        return Finance.__instance

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)


    #取得籌碼吉尼係數
    def getChipsGini(self, csvPath, encoding = "big5"):
        
        #將分點資料排序後，累進百分比
        def sortAndTransToPercent(collection):
            sortC = sorted([v for k, v in collection.items()])
            total = sum(sortC)
            result = []
            for i in range(len(sortC)):
                result.append(sortC[i] if i == 0 else sortC[i] + result[i-1])
            resultP = [round(p/total, 4) for p in result]
            self.logger.debug("{}", resultP)
            return resultP

        #計算一組數列在y=f(x)下的面積
        def calculateArea(collection):
            result = 0
            #for i in range(len(collection)-1):
            #    area = (collection[i] + collection[i+1]) * 1 / 2
            #    result += area
            cLen = len(collection)
            r1 = collection[0: cLen-1]
            r2 = collection[1: cLen]
            for i in range(cLen - 1):
                area = (r1[i] + r2[i]) * 1 / 2
                result += area
            return result
        
        #計算吉尼係數
        def getGiniCoefficient(bs, ss):
            f = lambda x: (len(x) * 1 / 2 - calculateArea(sortAndTransToPercent(x))) / len(x) * 1 / 2
            return f(bs) - f(ss)


        with open(csvPath, encoding="big5") as csvFile:
            csvr = csv.reader(csvFile)
            each_pt_buy_qty = {}
            each_pt_sell_qty = {}
            for row in csvr:
                pt1 = row[0].strip()
                pt2 = row[3].strip()
                bq1 = 0 if row[1].strip() == "" else int(row[1])
                sq1 = 0 if row[2].strip() == "" else int(row[2])
                bq2 = 0 if row[4].strip() == "" else int(row[4])
                sq2 = 0 if row[5].strip() == "" else int(row[5])        
                if len(pt1) != 0:
                    each_pt_buy_qty[pt1] = bq1 if pt1 not in each_pt_buy_qty.keys() else each_pt_buy_qty[pt1] + bq1
                    each_pt_sell_qty[pt1] = sq1 if pt1 not in each_pt_sell_qty.keys() else each_pt_sell_qty[pt1] + sq1
                if len(pt2) != 0:
                    each_pt_buy_qty[pt2] = bq2 if pt2 not in each_pt_buy_qty.keys() else each_pt_buy_qty[pt2] + bq2
                    each_pt_sell_qty[pt2] = sq2 if pt2 not in each_pt_sell_qty.keys() else each_pt_sell_qty[pt2] + sq2
        
        return getGiniCoefficient(each_pt_buy_qty, each_pt_sell_qty)



f = Finance()
print(f.getChipsGini("C:/Users/admin/Desktop/3031.csv"))
