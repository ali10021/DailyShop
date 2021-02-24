
# import wala saman
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash ,jsonify
from werkzeug.utils import secure_filename
from random import random, randint
import os
from flask_mail import Mail, Message
import json
from DBHandler import web_project
import smtplib

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '\\Users\\hp\\PycharmProjects\\shop\\static\\images'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def app_create():
    app = Flask(__name__)

    app.config.from_object('config')
    app.secret_key = app.config["SECRET_KEY"]
    # app.secret_key = "gfsjhfg-87t678564786"

    mail = Mail(app)

    app.config['MAIL_SERVER'] ='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ahmed345amjad@gmail.com'
    app.config['MAIL_PASSWORD'] = 'bitf18a002'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    return app
otp = randint(000000, 999999)
app=app_create()

@app.route('/')
def hello_world():
    # session.clear()
    # session.pop("admin-email", None)
    # session.pop("admin-username", None)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    men = db.CATAGERY('Men')
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    women = db.CATAGERY('Women')
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    sports = db.CATAGERY('Sports')
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    kids = db.CATAGERY('Kids')
    cartlist = db.getCarthower(session.get("email"))
    return render_template("index.html", product=men, wproduct=women, kproduct=kids, sproduct=sports, cartList=cartlist)


@app.route('/logOut')
def logOut():
    session.pop("email", None)
    session.pop("username", None)
    return redirect('/')


@app.route('/adminlogin')
def adminlogin():
    return render_template("adminLogin.html")


@app.route('/chart')
def chart():
    return render_template("chart.html")


@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/table')
def table():
    if session.get('admin-email'):
        return render_template("table.html")
    else:
        return redirect("/adminlogin")


@app.route('/ui')
def ui():
    return render_template("ui.html")


@app.route('/tab-panel')
def tabpanel():
    return render_template("tab-panel.html")


@app.route('/blank')
def blank():
    return render_template("blank.html")


@app.route('/account')
def Account():
    return render_template("account.html")


@app.route('/addProduct')
def addProduct():
    if session.get('admin-email'):
        return render_template("addProductByAdmin.html")
    else:
        return redirect("/adminlogin")


@app.route('/addToCart', methods=['POST'])
def addToCart():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    pid = int(key1[1])
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.addToCart(session["email"], pid)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/showmen')
def showmen():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.CATAGERY('Men')
    return render_template("product.html", product=dd)


@app.route('/showwomen')
def showwomen():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.CATAGERY('Women')
    return render_template("product.html", product=dd)


@app.route('/showkid')
def showkid():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.CATAGERY('Kids')
    return render_template("product.html", product=dd)


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.form["email"]
    username = request.form["uname"]
    password = request.form["pass"]
    role = request.form["rad"]

    web_projectobj = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                                 app.config["DATABASE"])
    if web_projectobj.register_user(username, email, password, role):
        return render_template("index.html", status=True)
    else:
        return render_template("account.html", status="This user email Already Exists")


@app.route('/loginn')
def loginn():
    return render_template("account.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    print("login")
    email = request.form["email"]
    passw = request.form["pass"]
    print("login1")
    obj = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                      app.config["DATABASE"])
    user_dic = obj.login(email, passw)
    print("login 2")
    print(user_dic)
    if user_dic:
        session["email"] = email
        session["username"] = user_dic["username"]
        if user_dic["role"] == "BuyerAccount":
            return redirect('/')
        else:
            return render_template("SellerDashboard.html", email=email, password=passw, role=user_dic["role"],
                                   username=user_dic["username"])
    else:
        return render_template("account.html")


@app.route('/addProductByAdmin', methods=['POST', 'GET'])
def addProductByAdmin():
    print("ADMIN")
    name = request.form['name']
    print(name)
    desc = request.form['description']
    print(desc)
    price = request.form['price']
    print(price)
    cate = request.form['cate']
    print(cate)
    subcate = request.form['subcate']
    print(subcate)
    stock = request.form["stock"]

    target = os.path.join(APP_ROOT, r'\Users\hp\PycharmProjects\shop\static\images')
    print(target)
    file = None
    for file in request.files.getlist("image"):
        filename = file.filename
        print("here21212")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print(destination)

    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    obj = db.ShowProducts()
    print("AfterShow")
    if db.addproduct(name, desc, price, cate, subcate, file.filename, stock):
        print("innerIf")
        file.save(destination)
        return render_template("addProductByAdmin.html", status=True)
    else:
        return render_template("addProductByAdmin.html", status=False)
    # dbb = db.signup(name, file.filename)
    # if dbb:
    #  return 'OK Hai'


# else:
# return 'Garbar hai'


@app.route('/404')
def four04():
    return render_template("404.html")


@app.route('/blogarchive2')
def ba2():
    return render_template("blog-archive-2.html")


@app.route('/blogsingle')
def blogSingle():
    return render_template("blog-single.html")


@app.route('/blogarchive')
def blogArchive():
    return render_template("blog-archive.html")


@app.route('/cart')
def cart():
    if session.get("email") != None:

        obj = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                          app.config["DATABASE"])
        print(session["email"])
        cartdic = obj.getCart(session["email"])
        print(cartdic)
        return render_template("cart.html", cartList=cartdic)
    else:
        return render_template("index.html")


@app.route('/seller')
def sellerDashboard():
    return render_template("SellerDashboard.html")


@app.route('/checkout')
def checkout():
    if session.get("email") != None:
        db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"])
        cartlist = db.getCartforCheckout(session.get("email"))
        return render_template("checkout.html", summaryList=cartlist)
    else:
        return render_template("index.html")


@app.route('/userApproved')
def userApproved():
    if session.get("admin-email") is not None:
        db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"])
        obj = db.Approved3partyProductsAdmin()
        return render_template("UserApproved.html", listOfProducts=obj, adminName=session.get("admin-username"))

    else:
        return render_template("adminLogin.html")


@app.route('/sellerApproved')
def sellerApproved():
    if session.get("email") is not None:
        db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"])
        obj = db.Approved3partyProducts(session["email"])
        return render_template("SellerApproved.html", listOfProducts=obj, adminName=session.get("admin-username"))

    else:
        return render_template("adminLogin.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/product')
def product():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.CATAGERY('Men')
    print(dd)
    return render_template("product.html", product=dd)


@app.route('/wishlist')
def wishlist():
    if session.get("email") != None:

        obj = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                          app.config["DATABASE"])
        print(session["email"])
        wishdic = obj.getWishlist(session["email"])
        print(wishdic)
        return render_template("wishlist.html", wishList=wishdic)
    else:
        return render_template("index.html")


@app.route('/admin-login')
def adminLogin():
    return render_template("adminLogin.html")


@app.route('/adminMain')
def adminMain():
    if session.get("admin-email") is not None:
        db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"])
        obj = db.ShowProducts()
        return render_template("table.html", listOfProducts=obj, adminName=session.get("admin-username"))

    else:
        return render_template("adminLogin.html")


@app.route('/admin-portal', methods=['GET', 'POST'])
def admin():
    print("admin Portal")
    email = request.form["email"]
    password = request.form["pass"]
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dict = db.validateAdmin(email, password)
    if dict:
        obj = db.ShowProducts()
        session["admin-email"] = email
        session["admin-username"] = dict["username"]
        print()
        return render_template("table.html", listOfProducts=obj, adminName=dict["username"])
    else:
        return render_template("adminLogin.html", error=True)


@app.route('/admin-logout')
def adminLogout():
    session.pop("admin-email", None)
    session.pop("admin-username", None)
    session.pop("oid", None)
    return render_template("index.html")


@app.route('/addTowishlist', methods=['POST'])
def addToWishList():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    id = int(key1[1])

    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.addToWishlist(session.get("email"), id)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/deleteFromWishlist', methods=['POST'])
def deleteFromWishlist():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    id = int(key1[1])

    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.deleteFromWishlist(id)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/deleteByAdmin', methods=['POST'])
def deleteByAdmin():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    score = int(key1[1])
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.delproductbyId(score)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/deleteFromCart', methods=['POST'])
def deleteFromCart():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    score = int(key1[1])
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.delproductbyIdFromCart(score)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/pending-requests')
def pendingRequest():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.showpending()
    return render_template("ShowPending.html", listOfProducts=dd)


@app.route('/sellerpending')
def sellerpendingRequest():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.sellershowpending(session["email"])
    return render_template("SellerPending.html", listOfProducts=dd)


@app.route('/approve', methods=['POST'])
def approve():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    score = int(key1[1])

    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.approve(score)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/addProductBySaler', methods=['POST', 'GET'])
def addProductBySaler():
    name = request.form['name']
    print(name)
    desc = request.form['description']
    print(desc)
    price = request.form['price']
    print(price)
    cate = request.form['cate']
    print(cate)
    subcate = request.form['subcate']
    print(subcate)
    stock = request.form["stock"]
    target = os.path.join(APP_ROOT, r'\Users\hp\PycharmProjects\shop\static\images')
    print(target)
    file = None
    for file in request.files.getlist("image"):
        filename = file.filename
        print("here21212")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print(destination)
        file.save(destination)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    db.addproductBySaler(name, session["username"], session["email"], desc, price, cate, subcate, file.filename, stock)
    return render_template("SellerDashboard.html", status=True)


@app.route('/updateInventory', methods=['POST'])
def upateStock():
    key1 = str(request.data)
    key1 = key1.split("'")
    score = key1[1]
    score = score.split(",")
    name = int(score[0])
    print(name)
    score = int(score[1])
    print(score)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.updateInventory(name, score)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/updateCart', methods=['POST'])
def upateCart():
    key1 = str(request.data)
    key1 = key1.split("'")
    score = key1[1]
    score = score.split(",")
    id = int(score[0])
    print(id)
    price = int(score[1])
    print(price)
    quan = int(score[2])
    print(quan)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.updateCart(id, price, quan)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/placeOrder', methods=['POST'])
def placeOrder():
    key1 = str(request.data)
    key1 = key1.split("'")
    score = key1[1]
    score = score.split(",")
    total = int(score[0])

    cell = int(score[1])
    address = score[2]


    print("In Place order before calling db handler")
    print(total)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.placeOrder(session.get("email"), total,cell,address)
    if dd:
        id = db.getOID()
        dd = db.orderitem(id)
        item = ""
        j = 1
        for i in dd:
            j = str(j)
            item = item + j + " Product Title:  " + i["name"] + " Quantity:   " + str(
                i["quantity"]) + " Product Price    " + str(i["price"]) + "\n"
            j = int(j)
            j = j + 1
        adress = "On Following Address\n" + " address  " + address + "  cell no. " + str(cell)
        detail = "Your order id " + str(id) + "\n" + item + adress
        message = Message("Order", sender='ahmed345amjad@gmail.com', recipients=[session["email"]])
        message.body = detail

        mail.send(message)
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/ship')
def address():
    return render_template("checkout.html", status=True)
@app.route('/showOrder')
def showorder():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.showOrder()
    df = db.detail
    return render_template("showOrder.html", listOfProducts=dd)


@app.route('/detail', methods=['POST'])
def detail():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    oid = int(key1[1])
    print("In Place order before calling db handler")
    print(oid)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.detail(oid)
    if dd:

        return jsonify(dd)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/Oadress', methods=['POST'])
def Oadress():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    oid = int(key1[1])
    print("In Place order before calling db handler")
    print(oid)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.getAddress(oid)
    if dd:

        return jsonify(dd)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/delivered', methods=['POST'])
def deliveered():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    oid = int(key1[1])
    print("In Place order before calling db handler")
    print(oid)
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.updateStatus(oid)
    if dd:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return None


@app.route("/anounce")
def annc():
    return render_template("anounce.html")


@app.route("/pasrecvry")
def pasrecvry():
    return render_template("pasrecvry.html")


@app.route("/announcement", methods=['POST'])
def anouncement():
    subject = request.form['sub']

    msg = request.form['message']

    obj = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                      app.config["DATABASE"])
    email = obj.getusers()
    print(email)

    for i in email:
        message = Message(subject, sender='ahmed345amjad@gmail.com', recipients=[i])
        message.body = msg

        mail.send(message)

    return render_template("anounce.html", status=True)


@app.route("/passrecovery", methods=['POST'])
def pssrcvry():
    email = request.form['email']
    obj = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                      app.config["DATABASE"])
    isuser = obj.isexist(email)
    if isuser:
        email = str(email)
        print(email)
        msg = "This is 6 digit code:" + str(otp)
        message = Message("OTP", sender='ahmed345amjad@gmail.com', recipients=[email])
        message.body = msg
        mail.send(message)
        return render_template("pasrecvry.html", status=True)
    else:
        return render_template("pasrecvry.html", warning=True)


@app.route('/setValue', methods=['POST'])
def setValue():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    oid = int(key1[1])
    print("In Place order before calling db handler")
    print(oid)
    session["pid"] = oid
    if oid:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/product_detail')
def productDetails():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.getproductbyid(session["pid"])
    review = db.getreview(session["pid"])
    print(dd)
    return render_template("product-detail.html", product=dd, review=review)


@app.route('/review', methods=['POST', 'GET'])
def review():
    print("inside review")
    rev = request.form['message']
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.setreview(session["pid"], session["email"], rev)
    if dd:
        db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                         app.config["DATABASE"])
        dd = db.getproductbyid(session["pid"])
        review = db.getreview(session["pid"])
        print(dd)
        return render_template("product-detail.html", product=dd, review=review)
    else:
        return "garbar"


@app.route('/totalFromCart', methods=['GET', 'POST'])
def totalcart():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.totalFromCart(session["email"])
    if dd is not None:
        return jsonify(dd)
    else:
        va = [{"check": "true"}]
        return jsonify(va)


@app.route('/setOID', methods=['POST'])
def setOID():
    key1 = str(request.data)
    print(key1)
    key1 = key1.split("'")
    oid = int(key1[1])
    print("In Place order before calling db handler")
    print(oid)
    session["oid"] = oid
    if oid:
        va = [{"check": "true"}]
        return jsonify(va)
    else:
        va = [{"check": "false"}]
        return jsonify(va)


@app.route('/orderdetail')
def orderdetail():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.orderitem(session["oid"])
    adres = db.orderadress(session["oid"])
    status = db.orderstatus(session["oid"])
    print(dd)
    return render_template("orderdetail.html", orderitem=dd, orderadres=adres, oid=session["oid"], status=status)


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.feedback(name, email, subject, message)
    if dd:
        return render_template("contact.html")
    else:
        return "Not added Feedback"


@app.route('/showsports')
def showsports():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.CATAGERY('Sports')
    return render_template("product.html", product=dd)


@app.route('/showdigital')
def showdigital():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.CATAGERY('Digital')
    return render_template("product.html", product=dd)


@app.route('/showfeedback')
def showfeedback():
    db = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
    dd = db.getfeedback()
    return render_template("feedback.html", feedbackList=dd)


@app.route("/otpconfirm", methods=['POST'])
def otpconfirm():
    user_otp = request.form['OTP']
    if otp != int(user_otp):
        return render_template("pasrecvry.html", recvry=False)
    else:
        return render_template("reenterpass.html")


@app.route("/reenterpass", methods=['POST'])
def reenterpass():
    email = request.form['email']
    passw = request.form['pass']
    cpass = request.form['cpass']
    if passw == cpass:
        obj = web_project(app.config["DATABASEIP"], app.config["DB_USER"], app.config["DB_PASSWORD"],
                          app.config["DATABASE"])
        result = obj.changepass(email, passw)
        if result:
            return render_template("account.html", change=True)
    else:
        return render_template("reenterpass.html", change=False)


if __name__ == '__main__':
    app.run(debug=True)
