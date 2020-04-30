import pymysql

from baseObject import baseObject

class lineItemList(baseObject):
    def __init__(self):
        self.setupObject('halukijl_lineItems')