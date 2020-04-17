import pymysql

from baseObject import baseObject

class productList(baseObject):
    def __init__(self):
        self.setupObject('halukijl_products')

    def verifyNew(self, n=0):
        self.errorList = []
        p = None

        if len(self.data[n]['sku']) == 0:
            self.errorList.append("SKU cannot be blank.")
        if len(self.data[n]['name']) == 0:
            self.errorList.append("Name cannot be blank.")
        try:
            p = float(self.data[n]['price'])
        except:
            self.errorList.append("Price must be entered as a float")
        if p is not None:
            if p > 0:
                self.data[n]['price'] = p
        else:
            self.errorList.append("Price cannot be blank.")
        if len(self.errorList) > 0:
            return False
        else:
            return True