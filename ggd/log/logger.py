#_*_ coding: UTF-8 _*_
from datetime import datetime

class Logger:

    appenders = []
    clz = None
    levels = {
        "ALL": 0,
        "TRACE": 1,
        "DEBUG": 2,
        "INFO": 3,
        "ERROR": 4,
        "FATEL": 5
    }

    level = "ALL"

    

    def __init__(self, clz, *appenders):        
        if len(self.appenders) == 0:
            for appender in appenders:
                self.appenders.append(appender)
        self.clz = clz        

    def trace(self, msg, *args):
        if self.levels.get(self.level) <= 1:
            self.doLog("TRACE", msg, *args)

    def debug(self, msg, *args):                
        if self.levels.get(self.level) <= 2:
            self.doLog("DEBUG", msg, *args) 

    def info(self, msg, *args):
        if self.levels.get(self.level) <= 3:
            self.doLog("INFO", msg, *args)

    

    def error(self, msg, *args):
        if self.levels.get(self.level) >= 4:
            self.doLog("ERROR", msg, *args)

    def fatel(self, msg, *args):
        if self.levels.get(self.level) is 5:
            self.doLog("FATEL", msg, *args)


    def doLog(self, level, msg, *args):
        target = self.clz.__class__.__name__
        m = "[{}][{}]: {}".format(level, target, msg.format(*args))
        for appender in self.appenders:
            appender.doLog(m)



class FileAppender:

    logFile = None

    def __init__(self):
        print("*******[INFO] FileAppender init *******")
        self.logFile = open("C:/Users/admin/Desktop/mypython.log", "a+")

    def doLog(self, msg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logFile.writelines("[{}]{}".format(now, msg + "\n"))

    def __del__(self):
        if self.logFile is not None:
            self.logFile.close()



class ConsoleAppender:

    def __init__(self):
        print("*******[INFO] ConsoleAppender init *******")

    def doLog(self, msg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("[{}]{}".format(now, msg))


class LoggerFactory:

    loggers = None
    fileAppender = None
    consoleAppender = None

    @staticmethod
    def getLogger(clz):

        if LoggerFactory.fileAppender is None:
            LoggerFactory.fileAppender = FileAppender()
        if LoggerFactory.consoleAppender is None:
            LoggerFactory.consoleAppender = ConsoleAppender()
        if LoggerFactory.loggers is None:
            LoggerFactory.loggers = {}

        name = clz.__class__.__name__
        if clz.__class__.__name__ not in LoggerFactory.loggers:
            logger = Logger(clz, LoggerFactory.consoleAppender, LoggerFactory.fileAppender)
            LoggerFactory.loggers[name] = logger
        return LoggerFactory.loggers[name]

'''
class Test1:

    logger = None

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)

    def test(self):
        self.logger.debug("{}", "aaa")



class Test2:

    logger = None

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)

    def test(self):
        self.logger.debug("{}", "bbb")


t1 = Test1()
t2 = Test2()
t1.test()
t2.test()
'''