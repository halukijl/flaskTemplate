import pymysql

from baseObject import baseObject

class lineItemList(baseObject):
    def __init__(self):
        self.setupObject('halukijl_lineItems')

    def getCart(self,oid):
        sql = '''SELECT halukijl_lineItems . * ,  `halukijl_products`.`name` AS productname
        FROM  `halukijl_lineItems` 
        LEFT JOIN halukijl_products ON halukijl_lineItems.pid = halukijl_products.pid
        WHERE halukijl_lineItems.oid =%s'''
        tokens = (oid)
        self.connect()
        print(sql,tokens)
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
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
