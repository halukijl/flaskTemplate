import pymysql

from baseObject import baseObject

class customerList(baseObject):
    def __init__(self):
        self.setupObject('halukijl_customers')

    def verifyNew(self, n=0):
        self.errorList = []

        if len(self.data[n]['fname']) == 0:
            self.errorList.append("First name cannot be blank.")
        if len(self.data[n]['lname']) == 0:
            self.errorList.append("Last name cannot be blank.")
        if len(self.data[n]['email']) == 0:
            self.errorList.append("Email cannot be blank.")
        if '@' not in self.data[n]['email'] or '.' not in self.data[n]['email']:
            self.errorList.append("Email must contain '.' and '@'.")
        if len(self.data[n]['password']) == 0:
            self.errorList.append("Password cannot be blank.")
        elif len(self.data[n]['password']) >= 5:
            self.errorList.append("Password must be 4 or less characters.")
        if self.data[n]['subscribed'].lower() == 'true':
            self.data[n]['subscribed'] = 'true'
        elif self.data[n]['subscribed'].lower() == 'false':
            self.data[n]['subscribed'] = 'false'
        else:
            self.errorList.append("Subscription must be True or False.")
        if len(self.errorList) > 0:
            return False
        else:
            return True

    def tryLogin(self, email, pw):
        #SELECT * FROM 'halukijl_customers' WHERE 'email' = 'jennyhaluk12@gmail.com' AND 'password' = '1234'
        sql = 'SELECT * FROM `' +self.tn + '`WHERE `email` =%s AND `password` =%s;'
        tokens = (email, pw)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tokens)
        self.data = []
        n=0
        for row in cur:
            self.data.append(row)
            n+=1
        if n > 0:
            return True
        else:
            return False








