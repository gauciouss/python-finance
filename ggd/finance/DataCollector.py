from ..log.logger import Logger
from ..log.logger import LoggerFactory
class CollectorFactory:

    logger = None
    __instance = None

    # do singleton
    def __new__(clz):
        if not CollectorFactory.__instance:
            CollectorFactory.__instance = object.__new__(clz)
        return CollectorFactory.__instance

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)


    
