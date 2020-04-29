import pymysql

from baseObject import baseObject

class orderList(baseObject):
    def __init__(self):
        self.setupObject('halukijl_orders')