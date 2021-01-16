import pymysql
import itertools
from datetime import datetime
class web_project:
    def __init__(self, host , user, password, database):
        self.host = host
        self.port=3306
        self.user = user
        self.password = password
        self.database = database

    def isUser(self,user):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from  users where email=%s"
            arg = (user)
            mydbcursor.execute(sql, arg)
            res=mydbcursor.fetchall()
            if(res):
                return True #user exists

            else:
                return False

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def register_user(self,user,email,pas,typ):
        if(self.isUser(email)):
            return False
        else:
            mydb=None
            try:
                mydb=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
                mydbcursor=mydb.cursor()
                sql="insert into users(email,username,password,role) values(%s,%s,%s,%s)"
                arg=(email,user,pas,typ)
                if mydbcursor.execute(sql,arg)>0:

                    mydb.commit()
                    return True
                else:
                    print("not inserted")
            except Exception as e:
                print(str(e))
            finally:
                if mydb!=None:
                    mydb.close()

    def login(self, user, pas):
        mydb=None
        list=[]
        try:
            mydb=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mydbcursor=mydb.cursor()
            sql="select email,username, password,role from web_project.users where email=%s  and password=%s"
            arg=(user,pas)
            mydbcursor.execute(sql,arg)
            result=mydbcursor.fetchall()
            print("in db")
            if result:
                for i in result:
                    dic={}
                    dic["email"]=i[0]
                    dic["username"] = i[1]
                    dic["password"] = i[2]
                    dic["role"] = i[3]
                    print(dic)
                    list.append(dic)
                    return dic
            else:
                print("user not exists")
                return False

        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb!=None:
                mydb.close()

    def FEEDBACK(self,name,email,msg):
        mydb=None
        try:
            mydb=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mydbcursor=mydb.cursor()
            sql="insert into FEEDBACK1(NAME,EMAIL,MESSAGE,DATE) values(%s,%s,%s,now())"
            arg=(name,email,msg)
            mydbcursor.execute(sql,arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
        finally:
            if mydb!=None:
                mydb.close()
    def CATAGERY(self, cat):
        mylist=[]
        mydb=None
        try:
            print("in catagory")
            mydb=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mydbcursor=mydb.cursor()
            sql="select * from web_project.garmentsproduct where Catagory=%s"
            arg=(cat)
            mydbcursor.execute(sql,arg)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                ll = [x[0],x[1], x[2], x[3], x[4], x[5],x[6],x[7]]
                mylist.append(ll)

            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb!=None:
                mydb.close()

    def ShowProducts(self):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select id,name,price,catagory,subCatagory,filepath,stock,sold,email from garmentsproduct where email='ds@gmail.com'"

            mydbcursor.execute(sql)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                dic={}
                dic["id"]=x[0]
                dic["name"] = x[1]
                dic["price"] = x[2]
                dic["cat"] = x[3]
                dic["subcat"] = x[4]
                dic["path"] = x[5]
                dic["stock"]=x[6]
                dic["sold"]=x[7]
                dic["owner"]=x[8]
                mylist.append(dic)
            for x in mylist:
                print(x["price"])
            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
    def Approved3partyProducts(self,email):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select id,name,price,catagory,subCatagory,filepath,stock,sold,email from web_project.garmentsproduct where email = %s"
            arg=(email)
            mydbcursor.execute(sql,arg)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                dic={}
                dic["id"]=x[0]
                dic["name"] = x[1]
                dic["price"] = x[2]
                dic["cat"] = x[3]
                dic["subcat"] = x[4]
                dic["path"] = x[5]
                dic["stock"]=x[6]
                dic["sold"]=x[7]
                dic["owner"]=x[8]
                mylist.append(dic)
            for x in mylist:
                print(x["price"])
            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()



    def SEARCH(self, sch):
        mylist=[]
        mydb=None
        try:
            mydb=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mydbcursor=mydb.cursor()
            sql="select NAME,PRICE,DESCRIPTION from web_project.garmentsproduct where CATAGERY like(%s)"

            arg=("%"+sch+"%")

            mydbcursor.execute(sql,arg)

            result=mydbcursor.fetchall()

            if result:
                for r in result:
                    mylist.append({'NAME': r[0], 'PRICE': r[1], 'DESCRIPTION': r[2]})
                return mylist

                return True
            else:

                return False

        except Exception as e:
            print(str(e))
        finally:
            if mydb!=None:
                mydb.close()
    def addproduct(self,name,disc,price,cat,subcat,path,stock):
        mydb=None
        try:
            mydb=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mydbcursor=mydb.cursor()
            sql="insert into garmentsproduct(NAME,DESCRIPTION,PRICE,Catagory,subCatagory,filepath,stock) values(%s,%s,%s,%s,%s,%s,%s)"
            arg=(name,disc,price,cat,subcat,path,stock)
            mydbcursor.execute(sql,arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
        finally:
            if mydb!=None:
                mydb.close()
    def delproduct(self,name):
        mydb=None
        try:
            mydb=pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mydbcursor=mydb.cursor()
            sql="delete from garmentsproduct where NAME LIKE(%s)"
            arg=(name)
            mydbcursor.execute(sql,arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
        finally:
            if mydb!=None:
                mydb.close()

    def validateAdmin(self,name,pas):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select email,username, password from admin where email=%s  and password=%s"
            arg = (name, pas)
            mydbcursor.execute(sql, arg)
            result = mydbcursor.fetchall()
            if result:
                for i in result:
                    dic = {}
                    dic["email"] = i[0]
                    dic["username"] = i[1]
                    dic["password"] = i[2]
                    return dic
            else:
                print("admin not exists")
                return False

        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def delproductbyId(self, id):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "delete from garmentsproduct where ID=%s"
            arg = (id)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def approve(self, id):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from productBySaler where ID=%s"
            args = (id)
            mydbcursor.execute(sql, args)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                ll = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],x[9]]
                dd = self.approvedProduct(x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],x[9])
                if dd:
                    print("product approved and added")
                    dc = self.deleteFromSaler(id)
                    if dc:
                        print("SuccessFully Deleted From pending")

            return True

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def approvedProduct(self, name, sname, semail, disc, price, cat, subcat, path,stock):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "insert into productBySalerApproved(NAME,SALERNAME,SALEREMAIL,DESCRIPTION,PRICE,Catagory,subCatagory,filepath,stock) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            arg = (name, sname, semail, disc, price, cat, subcat, path,stock)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            self.approvetomain(name, sname, semail, disc, price, cat, subcat, path,stock)
            return True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
    def approvetomain(self, name, sname, semail, disc, price, cat, subcat, path,stock):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "insert into garmentsproduct(NAME,DESCRIPTION,PRICE,Catagory,subCatagory,filepath,stock,email) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            arg = (name, disc,price,cat, subcat,path,stock,semail)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()


    def deleteFromSaler(self, id):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "delete from productBySaler where ID= %s"
            arg = (id)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def addproductBySaler(self, name, sname, semail, disc, price, cat, subcat, path,stock):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "insert into productBySaler(NAME,SALERNAME,SALEREMAIL,DESCRIPTION,PRICE,Catagory,subCatagory,filepath,stock) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            arg = (name, sname, semail, disc, price, cat, subcat, path,stock)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def sellershowpending(self,email):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from web_project.productbysaler where SALEREMAIL=%s"
            arg=(email)
            mydbcursor.execute(sql,arg)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                ll = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],x[9]]
                mylist.append(ll)

            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def showpending(self):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from productBySaler"
            mydbcursor.execute(sql)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                ll = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]]
                mylist.append(ll)

            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()


    def getProductPrice(self,pid):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select PRICE from garmentsproduct where ID=%s"

            arg = (pid)

            mydbcursor.execute(sql, arg)

            result = mydbcursor.fetchall()

            if result:
                for i in result:
                    price=i[0]
                    print(price)
                return price
            else:

                return False

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def addToCart(self,email,PID):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            if self.ispresentinCart(email,PID):
                return False
            else:
                price = self.getProductPrice(PID)
                sql = "insert into addcart (ID,email,PRICE) values (%s,%s,%s)"
                arg = (PID, email, price)
                if mydbcursor.execute(sql, arg) > 0:
                    mydb.commit()
                    return True
                else:
                    return False


        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def ispresentinCart(self, email, id):

        mydb = None
        try:
            print("ispesentincatr",email,id)
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()

            sql = "select *  from addcart where ID=%s and email=%s"
            arg = (id, email)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            print("in isprsntincart",myresult)
            if myresult:
                return True
            return False

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def ispresentinWishlist(self, email, id):

        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select *  from web_project.wishlist where ID=%s and email=%s"
            arg = (id, email)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            if myresult:
                return True
            return False

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
    def getCart(self,email):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select p.price,p.filepath,p.NAME,p.ID ,p.stock,a.quantity,a.PRICE from addcart a ,garmentsproduct p where a.ID=p.ID and a.email = %s"
            arg = (email)
            mydbcursor.execute(sql, arg)
            res=mydbcursor.fetchall()
            for i in res:
                dic={}
                dic["path"]=i[1]
                dic["name"]=i[2]
                dic["price"]=i[0]
                dic["id"]=i[3]
                dic["stock"]=i[4]
                dic["c-quantity"]=i[5]
                dic["c-price"]=i[6]
                list.append(dic)


        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
                print(list)
                return list
    def getCartforCheckout(self,email):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select  a.PRICE,a.quantity,p.NAME,p.ID from addcart a ,garmentsproduct p where a.ID=p.ID and a.email = %s"
            arg = (email)
            mydbcursor.execute(sql, arg)
            res=mydbcursor.fetchall()
            for i in res:
                dic={}
                dic["price"]=i[0]
                dic["quantity"]=i[1]
                dic["name"]=i[2]
                dic["ID"]=i[3]

                list.append(dic)


        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
                print(list)
                return list

    def delproductbyIdFromCart(self, id):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "delete from addcart where ID=%s"
            arg = (id)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def updateInventory(self, id, quan):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            prevQuan = self.getQuan(id)
            quan = quan + prevQuan
            sql = "UPDATE garmentsproduct SET stock = %s WHERE ID=%s;"
            arg = (quan, id)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def getQuan(self, id):
        mylist = 0
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select stock from garmentsproduct where ID=%s"
            arg = (id)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                mylist = x[0]
            print("Inside getQUan",mylist)
            return mylist


        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
    def getWishlist(self,email):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select p.price,p.filepath,p.NAME,p.ID ,p.stock from wishlist a ,garmentsproduct p where a.ID=p.ID and a.email = %s"
            arg = (email)
            mydbcursor.execute(sql, arg)
            res=mydbcursor.fetchall()
            for i in res:
                dic={}
                dic["path"]=i[1]
                dic["name"]=i[2]
                dic["price"]=i[0]
                dic["id"]=i[3]
                if(i[4]>0):
                    dic["stock"]="Available"
                else:
                    dic["stock"]="Out of Stock"
                list.append(dic)


        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
                print(list)
                return list

    def addToWishlist(self,email,id):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            if self.ispresentinWishlist(email,id):
                return False
            else:
                sql = "insert into wishlist (ID,email) values (%s,%s)"
                arg = (id, email)
                if mydbcursor.execute(sql, arg) > 0:
                    mydb.commit()
                    return True
                else:
                    return False


        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
    def deleteFromWishlist(self,id):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "delete from wishlist where ID=%s"
            arg = (id)
            mydbcursor.execute(sql, arg)
            mydbcursor.fetchall()
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
    def updateCart(self,id,price,quan):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "Update addcart set PRICE=%s ,quantity=%s where id=%s"
            arg = (price,quan,id)
            if mydbcursor.execute(sql, arg)>0:
                mydb.commit()
                return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
    def placeOrder(self,email,total,cell,adres):
        mydb = None
        list = []
        try:
            if(total >0):
                mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
                mydbcursor = mydb.cursor()
                sql = "insert into web_project.order (EMAIL,TOTAL) values (%s,%s)"
                arg = (email,total)

                mydbcursor.execute(sql, arg)
                mydb.commit()
                dd = self.address(cell, adres)
                dd = self.orderProduct(email)
                if dd:
                    return True
                else:
                    return False
            else:
                return False




        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def orderProduct(self, email):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            dic=self.getCartforCheckout(email)
            print("inside orderproduct")
            print(dic)
            oid = self.getOID()
            for i in dic:
                print("Inside FOr loop",i)
                name=i["name"]
                quantity=i["quantity"]
                id=i["ID"]
                price = i["price"]
                print("before update")
                tt=self.updateQuantity(id,quantity)

                if tt:
                    print("In tt")
                    sql = "insert into orderitem (OID,NAME,QUANTITY,PRICE) values (%s,%s,%s,%s)"
                    arg = (oid,name,quantity,price)
                    if mydbcursor.execute(sql, arg) > 0:
                        mydb.commit()
                    print("before deletecart")
                    self.delproductbyIdFromCartByEmail(email)
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
    def updateQuantity(self,id,quan):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            quantity=self.getQuan(id)
            quantity=quantity-quan
            print("In update quan",quantity)
            soldpro=self.getsoldProducts(id)
            print("after print")
            soldpro=int(soldpro)
            soldpro=soldpro+quan
            sql = "Update garmentsproduct set stock=%s,sold=%s  where ID=%s"
            arg = (quantity,soldpro,id)
            if mydbcursor.execute(sql, arg)>0:
                mydb.commit()
                return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
    def getsoldProducts(self,id):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select sold from garmentsproduct where ID=%s"
            arg = (id)
            mydbcursor.execute(sql, arg)
            res=mydbcursor.fetchall()
            if res:
                for i in res:
                    sold=i[0]
                    print(sold)
                    return sold
            else:
                return False
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()


    def delproductbyIdFromCartByEmail(self,email):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "delete from addcart where email=%s"
            arg = (email)
            mydbcursor.execute(sql, arg)

            mydb.commit()

        except Exception as e:
            print(str(e))

        finally:
            if mydb != None:
                mydb.close()
    def getOID(self):
        mylist = 0
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select MAX(OID) from web_project.order"

            mydbcursor.execute(sql)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                mylist = x[0]
            print(mylist)
            return mylist
        except Exception as e:
            print(str(e))

        finally:
            if mydb != None:
                mydb.close()
    def address(self,phone,address):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            id=self.getOID()
            id=id
            print("id before adres insert",id)
            sql = "insert into adress (ID,PHONE,ADDRESS) values (%s,%s,%s)"
            arg = (id,phone,address)

            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True

        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
    def showOrder(self):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select OID,EMAIL,TOTAL,STATUS from web_project.order"

            mydbcursor.execute(sql)
            myresult = mydbcursor.fetchall()
            for i in myresult:
                dic = {}

                dic["ID"] = i[0]
                dic["EMAIL"] = i[1]
                dic["Total"] = i[2]
                dic["status"]=i[3]
                mylist.append(dic)
            print(mylist)
            return mylist
        except Exception as e:
            print(str(e))

        finally:
            if mydb != None:
                mydb.close()
    def detail(self,oid):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select NAME,QUANTITY,PRICE from web_project.orderitem WHERE OID=%s"
            arg=(oid)
            mydbcursor.execute(sql,arg)
            myresult = mydbcursor.fetchall()
            for i in myresult:
                dic = {}

                dic["NAME"] = i[0]
                dic["QUANTITY"] = i[1]
                dic["PRICE"] = i[2]

                mylist.append(dic)
            print(mylist)
            return mylist
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
    def getAddress(self,oid):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select ADDRESS,COUNTRY,PCODE,SPNOTE from web_project.adress WHERE ID=%s"
            arg=(oid)
            mydbcursor.execute(sql,arg)
            myresult = mydbcursor.fetchall()
            for i in myresult:
                dic = {}

                dic["ADDRESS"] = i[0]
                dic["COUNTRY"] = i[1]
                dic["PCODE"] = i[2]
                dic["SPNOTE"]=i[3]

                mylist.append(dic)
            print(mylist)
            return mylist
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
    def updateStatus(self,oid):
        mydb = None
        try:
            print("in status")
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "update web_project.order set status='Delivered' where OID=%s"

            arg = (oid)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            print("out status")
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()



    def getusers(self):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password,database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select email from users"
            mydbcursor.execute(sql)
            myresult = mydbcursor.fetchall()

            myresult = list(myresult)
            #itertools will convert list of tupples to list
            out = list(itertools.chain(*myresult))

            return out

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def getpassword(self, email):

        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password,database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select password from users where email=%s"
            arg = (email)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()

            myresult = list(myresult)

            out = list(itertools.chain(*myresult))

            return out

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def getproductbyid(self, cat):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from garmentsproduct where ID=%s"
            arg = (cat)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                ll = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]]
                mylist.append(ll)

            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def getreview(self, cat):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from review where ID=%s"
            arg = (cat)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                print(x[1])
                name = self.getUserName(x[1])
                print(name)
                ll = [x[0], name[0], x[4]]

                mylist.append(ll)

            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def getUserName(self, id):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select USERNAME from users where email=%s"
            arg = (id)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            print("username", myresult)
            for x in myresult:
                ll = x[0]
                mylist.append(ll)

            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def setreview(self, id, email, rev):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            now = datetime.now()
            now = now.strftime('%Y-%m-%d')

            sql = "insert into review (REVIEW,EMAIL,ID,DATE) values (%s,%s,%s,%s)"
            arg = (rev, email, id, now)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True

        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def totalFromCart(self, email):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select sum(PRICE) from addcart where email=%s"
            arg = (email)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            print("username", myresult)

            for x in myresult:
                ll = {}
                ll["TOTAL"] = str(x[0])
                mylist.append(ll)
            print("total price from cart", mylist)
            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def orderitem(self, oid):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from web_project.orderitem where OID=%s"
            arg = (oid)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            print("orderitem", myresult)
            for x in myresult:
                ll = {}
                ll["name"] = x[1]
                ll["quantity"] = x[2]
                ll["price"] = x[3]
                mylist.append(ll)
            print("orderitem", mylist)
            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def orderadress(self, oid):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select PHONE,ADDRESS from web_project.adress where ID=%s"
            arg = (oid)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()
            print("orderitem", myresult)
            for x in myresult:
                ll = {}
                ll["phone"] = x[0]
                ll["address"] = x[1]

                mylist.append(ll)
            print("address", mylist)
            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def orderstatus(self, oid):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select STATUS from web_project.order where OID=%s"
            arg = (oid)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchone()
            print("orderitem", myresult)
            status=myresult[0]
            print(status)
            return status

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
    def feedback(self, name,email,subject,message):
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "insert into feedback1 (NAME,EMAIL,SUBJECT,MESSAGE) values (%s,%s,%s,%s)"
            arg = (name, email, subject, message)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True

        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def getfeedback(self):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select * from web_project.feedback1"
            mydbcursor.execute(sql)
            myresult = mydbcursor.fetchall()
            print(myresult)
            for i in myresult:
                dic={}
                dic["name"]=i[0]
                dic["email"]=i[1]
                dic["message"]=i[2]
                dic["subject"]=i[3]
                mylist.append(dic)

            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def Approved3partyProductsAdmin(self):
        mylist = []
        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select id,name,price,catagory,subCatagory,filepath,stock,sold,email from web_project.garmentsproduct where email !='ds@gmail.com'"

            mydbcursor.execute(sql)
            myresult = mydbcursor.fetchall()
            for x in myresult:
                dic = {}
                dic["id"] = x[0]
                dic["name"] = x[1]
                dic["price"] = x[2]
                dic["cat"] = x[3]
                dic["subcat"] = x[4]
                dic["path"] = x[5]
                dic["stock"] = x[6]
                dic["sold"] = x[7]
                dic["owner"] = x[8]
                mylist.append(dic)
            for x in mylist:
                print(x["price"])
            return mylist

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def getCarthower(self, email):
        mydb = None
        list = []
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            print("in carthower")
            sql = "select p.price,p.filepath,p.NAME,p.ID ,p.stock,a.quantity,a.PRICE from web_project.addcart a ,web_project.garmentsproduct p where a.ID=p.ID and a.email = %s"
            arg = (email)
            print("out carthower")
            mydbcursor.execute(sql, arg)
            res = mydbcursor.fetchall()
            for i in res:
                dic = {}
                dic["path"] = i[1]
                dic["name"] = i[2]
                dic["price"] = i[0]
                dic["id"] = i[3]
                dic["stock"] = i[4]
                dic["quantity"] = i[5]
                dic["total"] = i[6]
                list.append(dic)


        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
                print(list)
                return list

    def getpassword(self, email):

        mydb = None
        try:
            mydb = pymysql.connect(host=self.host,  user=self.user, password=self.password, database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select password from web_project.users where email=%s"
            arg = (email)
            mydbcursor.execute(sql, arg)
            myresult = mydbcursor.fetchall()

            myresult = list(myresult)

            out = list(itertools.chain(*myresult))

            return out

        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def changepass(self, email, passw):

        mydb = None
        try:
            mydb = pymysql.connect(host=self.host,  user=self.user, password=self.password,
                                   database=self.database)
            mydbcursor = mydb.cursor()
            sql = "update web_project.users set password=%s where email=%s"
            arg = (passw, email)
            mydbcursor.execute(sql, arg)
            mydb.commit()
            return True


        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()

    def isexist(self, email):

        mydb = None
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                   database=self.database)
            mydbcursor = mydb.cursor()
            sql = "select email from web_project.users where email=%s"
            arg = (email)
            result = mydbcursor.execute(sql, arg)
            if result:

                mydb.commit()
                return True
            else:
                return False
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
web_projecto=web_project("localhost","root","PakarmyForce8790","web_project")
