import pymysql

from baseObject import baseObject

class orderList(baseObject):
    def __init__(self):
        self.setupObject('halukijl_orders')

    def getLast(self,uid):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `userid` = %s AND `status` = %s order by `createtime` desc;'
        tokens = (uid,'shopping')
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql,tokens)
        cur.execute(sql,tokens)
        self.data = []
        for row in cur:
            self.data.append(row)

    def getByCustomer(self,uid):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `userid` = %s AND `status` = %s order by `createtime` desc;'
        tokens = (uid,'completed')
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql,tokens)
        cur.execute(sql,tokens)
        self.data = []
        for row in cur:
            self.data.append(row)












