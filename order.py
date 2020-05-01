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

    def getCheckout(self,oid):
        sql = '''SELECT halukijl_lineItems . * ,  `halukijl_orders`.`orderprice` AS orderprice
        FROM  `halukijl_lineItems` 
        LEFT JOIN halukijl_orders ON halukijl_lineItems.oid = halukijl_orders.oid
        WHERE halukijl_lineItems.oid =%s'''
        tokens = (oid)
        self.connect()
        print(sql,tokens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tokens)
        self.data = []
        for row in cur:
            self.data.append(row)










