from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from customer import customerList
from product import productList
from user import userList
import json, pymysql, time

from flask_session import Session

app = Flask(__name__,static_url_path='')

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'

@app.route('/get')
def get():
    return str(session['time'])

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.form.get('email') is not None and request.form.get('password') is not None:
        u = userList()
        if u.tryLogin(request.form.get('email'),request.form.get('password')):
            #print('Login Okay')
            session['user'] = u.data[0]
            session['active'] = time.time()
            '''
            o = orderList()
            o.getLast(session['user']['id'])
            if len(o.data) > 0: 
                session['orderid'] = o.data[0]['order_id']
            else:
                o.set('createtime','NOW')
                o.set('status','shopping')
                o.set('userid',session['user']['id'])
                o.add()
                o.insert()
                session['orderid'] = o.data[0]['order_id'] 
            '''
            return redirect('main')
        else:
            #print('Login Failed')
            return render_template('login.html', title='Login', 
            msg='Incorrect username or password.')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None

        return render_template('login.html', title='Login', 
        msg=m)

@app.route('/loginadmin', methods = ['GET','POST'])
def loginadmin():
    if request.form.get('email') is not None and request.form.get('password') is not None:
        u = userList()
        if u.tryLogin(request.form.get('email'),request.form.get('password')):
            session['user'] = u.data[0]
            session['active'] = time.time()

            return redirect('mainAdmin')
        else:
            return render_template('loginadmin.html', title='Login', 
            msg='Incorrect credentials.')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None

        return render_template('loginadmin.html', title='Login', 
        msg=m)

@app.route('/logout', methods = ['GET','POST'])
def logout():
    del session['user']
    del session['active']
    return render_template('login.html', title='Login', 
    msg='You have logged out.')

@app.route('/nothing')
def nothing():
    print('hi')
    return ''

@app.route('/basichttp')
def basichttp():
    if request.args.get('myvar') is not None:
        return 'your var:' + request.args.get('myvar')
    else:
        return 'myvar not set' 

@app.route('/')
def home():
    if checkSession() == False:
        return redirect('login')
    return render_template('test.html', title='Test', msg='Welcome!')

@app.route('/index')
def index():
    user = {'username': 'Jenny'}

    items = [
        {'name':'Apple','price':2.34},
        {'name':'Orange','price':4.88},
        {'name':'Grape','price':2.44}
    ]
    return render_template('index.html', title='Home', user=user, items=items)

@app.route('/Cproducts')
def Cproducts():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    p.getAll()

    return render_template('Cproducts.html', title='Our Products', products=p.data)

@app.route('/customers')
def customers():
    if checkSession() == False:
        return redirect('login')
    c = customerList()
    c.getAll()

    print(c.data)
    return render_template('customers.html', title='Customer List', customers=c.data)

@app.route('/users')
def users():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    u.getAll()

    print(u.data)
    return render_template('customers.html', title='User List', users=u.data)

@app.route('/products')
def products():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    p.getAll()

    print(p.data)
    #return''
    return render_template('products.html', title='Product List', products=p.data)

@app.route('/newProduct', methods = ['GET', 'POST'])
def newProduct():
    if checkSession() == False:
        return redirect('login')
    if request.form.get('sku') is None:
        p = productList()
        p.set('sku', '')
        p.set('name', '')
        p.set('price', '')
        p.add()
        return render_template('newProduct.html', title='New Product', product=p.data[0])
    else:
        p = productList()
        p.set('sku',request.form.get('sku'))
        p.set('name',request.form.get('name'))
        p.set('price',request.form.get('price'))
        p.add()
        if p.verifyNew():
            p.insert()
            print(p.data)
            return render_template('savedproduct.html', title='Product Saved', product=p.data[0])
        else:
            return render_template('newProduct.html', title='Product Not Saved', product=p.data[0], msg=p.errorList)

@app.route('/saveproduct', methods = ['GET', 'POST'])
def saveproduct():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    p.set('pid',request.form.get('pid'))
    p.set('sku',request.form.get('sku'))
    p.set('name',request.form.get('name'))
    p.set('price',request.form.get('price'))
    p.add()
    p.update()
    print(p.data)
    #return ''
    return render_template('savedproduct.html', title='Product Saved', product=p.data[0])

@app.route('/product')
def product():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    if request.args.get(p.pk) is None:
        return render_template('error.html', msg='No product id given.')

    p.getById(request.args.get(p.pk))
    
    if len(p.data) <= 0:
        return render_template('error.html', msg='Product not found.')

    print(p.data)
    #return''
    return render_template('product.html', title='Product', product=p.data[0])

@app.route('/customer')
def customer():
    if checkSession() == False:
        return redirect('login')
    c = customerList()
    if request.args.get(c.pk) is None:
        return render_template('error.html', msg='No customer id given.')

    c.getById(request.args.get(c.pk))
    
    if len(c.data) <= 0:
        return render_template('error.html', msg='Customer not found.')

    print(c.data)
    #return''
    return render_template('customer.html', title='Customer', customer=c.data[0])

@app.route('/newcustomer', methods = ['GET', 'POST'])
def newcustomer():
    if checkSession() == False:
        return redirect('login')
    if request.form.get('fname') is None:
        c = customerList()
        c.set('fname', '')
        c.set('lname', '')
        c.set('email', '')
        c.set('password', '')
        c.set('subscribed', '')
        c.add()
        return render_template('newCustomer.html', title='New Customer', customer=c.data[0])
    else:
        c = customerList()
        c.set('fname',request.form.get('fname'))
        c.set('lname',request.form.get('lname'))
        c.set('email',request.form.get('email'))
        c.set('password',request.form.get('password'))
        c.set('subscribed',request.form.get('subscribed'))
        c.add()
        if c.verifyNew():
            c.insert()
            print(c.data)
            return render_template('savedcustomer.html', title='Customer Saved', customer=c.data[0])
        else:
            return render_template('newcustomer.html', title='Customer Not Saved', customer=c.data[0], msg=c.errorList)

@app.route('/main')
def main():
    if checkSession() == False: #check to make sure user is logged in
        return redirect('login')
    userinfo = 'Hello, ' + session['user']['fname']
    return render_template('main.html', title='Main Menu', msg = userinfo)

@app.route('/mainAdmin')
def mainAdmin():
    if checkSession() == False:
        return redirect('loginadmin')
    userinfo = 'Hello, ' + session['user']['fname']
    return render_template('mainAdmin.html', title='Main Menu', msg = userinfo)

@app.route('/savecustomer', methods = ['GET', 'POST'])
def savecustomer():
    if checkSession() == False:
        return redirect('login')
    c = customerList()
    c.set('id',request.form.get('id'))
    c.set('fname',request.form.get('fname'))
    c.set('lname',request.form.get('lname'))
    c.set('email',request.form.get('email'))
    c.set('password',request.form.get('password'))
    c.set('subscribed',request.form.get('subscribed'))
    c.add()
    c.update()
    print(c.data)
    #return ''
    return render_template('savedcustomer.html', title='Customer Saved', customer=c.data[0])

@app.route('/deletecustomer', methods = ['GET', 'POST'])
def deletecustomer():
    if checkSession() == False:
        return redirect('login')
    c = customerList()
    c.deleteByID(request.form.get('id'))
    return render_template('deletedCustomer.html', title='Customer Deleted', msg= 'Customer deleted.')

def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 5000:
            session['msg'] = 'Your session has timed out'
            return False
        else:    
            session['active'] = time.time()
            return True

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)











