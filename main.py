from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from customer import customerList
from admin import adminList
from product import productList
from user import userList
from order import orderList
from lineItem import lineItemList
from datetime import datetime
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
            o = orderList()
            o.getLast(session['user']['id'])
            if len(o.data) > 0: 
                session['orderid'] = o.data[0]['oid']
            else:
                now = datetime.now()
                o.set('createtime',str(now))
                o.set('status','shopping')
                o.set('userid',session['user']['id'])
                o.add()
                o.insert()
                session['orderid'] = o.data[0]['oid']
            print('oid',session['orderid'])
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
        a = adminList()
        if a.tryLogin(request.form.get('email'),request.form.get('password')):
            session['user'] = a.data[0]
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
    return render_template('login.html', title='Login', msg='Welcome!')

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

    print(p.data)
    return render_template('Cproducts.html', title='Our Products', products=p.data)

@app.route('/users')
def users():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    u.getAll()

    print(u.data)
    return render_template('users.html', title='User List', users=u.data)

@app.route('/admins')
def admins():
    if checkSession() == False:
        return redirect('login')
    a = adminList()
    a.getAll()

    print(a.data)
    return render_template('admins.html', title='Admin List', admins=a.data)

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
        p.set('description', '')
        p.add()
        return render_template('newProduct.html', title='New Product', product=p.data[0])
    else:
        p = productList()
        p.set('sku',request.form.get('sku'))
        p.set('name',request.form.get('name'))
        p.set('price',request.form.get('price'))
        p.set('description',request.form.get('description'))
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
    p.set('description',request.form.get('description'))
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

@app.route('/Cproduct')
def Cproduct():
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
     return render_template('Cproduct.html', title='Product', product=p.data[0])
     
@app.route('/user')
def user():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    if request.args.get(u.pk) is None:
        return render_template('error.html', msg='No user id given.')

    u.getById(request.args.get(u.pk))
    
    if len(u.data) <= 0:
        return render_template('error.html', msg='User not found.')

    print(u.data)
    #return''
    return render_template('user.html', title='User', user=u.data[0])

@app.route('/admin')
def admin():
    if checkSession() == False:
        return redirect('login')
    a = adminList()
    if request.args.get(a.pk) is None:
        return render_template('error.html', msg='No admin id given.')

    a.getById(request.args.get(a.pk))
    
    if len(a.data) <= 0:
        return render_template('error.html', msg='Admin not found.')

    print(a.data)
    #return''
    return render_template('admin.html', title='Admin', admin=a.data[0])

@app.route('/newuser', methods = ['GET', 'POST'])
def newuser():
    if checkSession() == False:
        return redirect('login')
    if request.form.get('fname') is None:
        u = userList()
        u.set('fname', '')
        u.set('lname', '')
        u.set('email', '')
        u.set('password', '')
        u.set('subscribed', '')
        u.add()
        return render_template('newUser.html', title='New User', user=u.data[0])
    else:
        u = userList()
        u.set('fname',request.form.get('fname'))
        u.set('lname',request.form.get('lname'))
        u.set('email',request.form.get('email'))
        u.set('password',request.form.get('password'))
        u.set('subscribed',request.form.get('subscribed'))
        u.add()
        if u.verifyNew():
            u.insert()
            print(u.data)
            return render_template('saveduser.html', title='User Saved', user=u.data[0])
        else:
            return render_template('newuser.html', title='User Not Saved', user=u.data[0], msg=u.errorList)

@app.route('/newadmin', methods = ['GET', 'POST'])
def newadmin():
    if checkSession() == False:
        return redirect('login')
    if request.form.get('fname') is None:
        a = adminList()
        a.set('fname', '')
        a.set('lname', '')
        a.set('email', '')
        a.set('password', '')
        a.set('subscribed', '')
        a.add()
        return render_template('newadmin.html', title='New Admin', admin=a.data[0])
    else:
        a = adminList()
        a.set('fname',request.form.get('fname'))
        a.set('lname',request.form.get('lname'))
        a.set('email',request.form.get('email'))
        a.set('password',request.form.get('password'))
        a.set('subscribed',request.form.get('subscribed'))
        a.add()
        if a.verifyNew():
            a.insert()
            print(a.data)
            return render_template('savedadmin.html', title='Admin Saved', admin=a.data[0])
        else:
            return render_template('newadmin.html', title='Admin Not Saved', admin=a.data[0], msg=a.errorList)

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

@app.route('/saveuser', methods = ['GET', 'POST'])
def saveuser():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    u.set('id',request.form.get('id'))
    u.set('fname',request.form.get('fname'))
    u.set('lname',request.form.get('lname'))
    u.set('email',request.form.get('email'))
    u.set('password',request.form.get('password'))
    u.set('subscribed',request.form.get('subscribed'))
    u.add()
    u.update()
    print(u.data)
    #return ''
    return render_template('saveduser.html', title='User Saved', user=u.data[0])

@app.route('/saveadmin', methods = ['GET', 'POST'])
def saveadmin():
    if checkSession() == False:
        return redirect('login')
    a = adminList()
    a.set('id',request.form.get('id'))
    a.set('fname',request.form.get('fname'))
    a.set('lname',request.form.get('lname'))
    a.set('email',request.form.get('email'))
    a.set('password',request.form.get('password'))
    a.set('subscribed',request.form.get('subscribed'))
    a.add()
    a.update()
    print(a.data)
    #return ''
    return render_template('savedadmin.html', title='Admin Saved', admin=a.data[0])

@app.route('/deleteuser', methods = ['GET', 'POST'])
def deleteuser():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    u.deleteByID(request.form.get('id'))
    return render_template('deletedUser.html', title='User Deleted', msg= 'User deleted.')

@app.route('/deleteproduct', methods = ['GET', 'POST'])
def deleteproduct():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    p.deleteByID(request.form.get('pid'))
    return render_template('deletedProduct.html', title='Product Deleted', msg= 'Product deleted.')

@app.route('/deleteadmin', methods = ['GET', 'POST'])
def deleteadmin():
    if checkSession() == False:
        return redirect('login')
    a = adminList()
    a.deleteByID(request.form.get('id'))
    return render_template('deletedAdmin.html', title='Admin Deleted', msg= 'Admin deleted.')

@app.route('/cart')
def cart():
    if checkSession() == False:
        return redirect('login')
    l = lineItemList()
    l.getOrder(session['orderid'])
    ot = 0.0
    for item in l.data:
        ot += float(item['price']) * int(item['quantity'])

    l.getCart(session['orderid'])

    if len(l.data) <= 0:
        return render_template('noproduct.html', msg='Please add products')

    return render_template('cart.html', title='Cart', lineItems=l.data, ot=ot)

@app.route('/addToCart', methods = ['GET', 'POST'])
def addToCart():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    p.getById(request.form.get('pid'))
    l = lineItemList()
    l.set('price',p.data[0]['price'])
    l.set('quantity',request.form.get('quantity'))
    l.set('oid',session['orderid'])
    l.set('pid',request.form.get('pid'))
    l.add()
    l.insert()

    print(l.data)
    return render_template('itemAdded.html', title='Item Added.', msg= 'Item added.')

@app.route('/checkout', methods = ['GET','POST'])
def checkout():
    if checkSession() == False:
        return redirect('login')
    l = lineItemList()
    l.getOrder(session['orderid'])
    ot = 0.0
    for item in l.data:
        ot += float(item['price']) * int(item['quantity'])
    o = orderList()
    o.getById(session['orderid'])
    o.data[0]['status']='completed'
    o.data[0]['orderprice']=ot
    o.update()
    o = orderList()
    now = datetime.now()
    o.set('createtime',str(now))
    o.set('status','shopping')
    o.set('userid',session['user']['id'])
    o.add()
    o.insert()
    session['orderid'] = o.data[0]['oid']
    print('oid',session['orderid'])

    print(o.data)
    return render_template('checkedout.html', title='Check Out Completed')

@app.route('/deleteitem', methods = ['GET', 'POST'])
def deleteitem():
    if checkSession() == False:
        return redirect('login')
    o = orderList()
    o.deleteByID(request.form.get('id'))
    return render_template('deletedItem.html', title='Item Deleted', msg= 'Item deleted.')

@app.route('/myorders')
def myorders():
    if checkSession() == False: 
        return redirect('login')
    o = orderList()
    o.getByCustomer(session['user']['id'])
   
    print(o.data)
    #return''
    return render_template('myorders.html', title='Your Orders', orders=o.data)

@app.route('/orders')
def orders():
    if checkSession() == False:
        return redirect('login')
    o = orderList()
    o.getAll()

    print(o.data)
    return render_template('orders.html', title='Orders', orders=o.data)

@app.route('/deleteorder', methods = ['GET', 'POST'])
def deleteorder():
    if checkSession() == False:
        return redirect('login')
    o = orderList()
    o.deleteByID(request.form.get('id'))
    return render_template('deletedOrder.html', title='Order Deleted', msg= 'Order deleted.')

@app.route('/myorder')
def myorder():
    if checkSession() == False:
        return redirect('login')
    l = lineItemList()
    if request.args.get('oid') is None:
        return render_template('error.html', msg='No order id given.')

    l.getOrder(request.args.get('oid'))
    
    if len(l.data) <= 0:
        return render_template('error.html', msg='Order not found.')
    
    print(l.data)
    print(session['user']['id'])
    #return''
    return render_template('myorder.html', title='Order', lineItems=l.data)

@app.route('/order')
def order():
    if checkSession() == False:
        return redirect('login')
    l = lineItemList()
    if request.args.get('oid') is None:
        return render_template('error.html', msg='No order id given.')

    l.getOrder(request.args.get('oid'))
    
    if len(l.data) <= 0:
        return render_template('error.html', msg='No items in cart')
    
    print(l.data)
     #return''
    return render_template('order.html', title='Order', lineItems=l.data)

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











