import gc
import os
from tkinter import messagebox
from Search import *
from Items import *

import MySQLdb
from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
from jinja2 import Environment
from requests import Session
from wtforms import Form, TextField, validators, PasswordField, BooleanField, StringField, form
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart, connection
from functools import wraps
import ctypes
__author__ = 'ibininja'


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = "supershop"
mysql = MySQL(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])



# User Register
# Register Form Class
class RegisterForm(Form):

    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('User Name', [validators.Length(min=1, max=50)])

    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    mobileno = StringField('Mobile No.', [validators.Length(min=1, max=50)])

@app.route('/upload/<filename>')
def send_image1(filename):
    return send_from_directory("images", filename)
@app.route('/Drinks/<filename>')
def send_image3(filename):
    return send_from_directory("images", filename)
@app.route('/search_result/<filename>')
def send_image4(filename):
    return send_from_directory("images", filename)


@app.route('/',methods=['GET', 'POST'])
def home():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mobileno = form.mobileno.data
        print(name)

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute(
            "INSERT INTO registration_table( name, username, email, password, mobile_no) VALUES(%s, %s, %s, %s, %s)",
            (name, username, email, password, mobileno))

        cur.execute(
            "SELECT username FROM registration_table where (username)=(%s)", [username])
        data = cur.fetchall()
        print(data[0][0])
        Id = str(data[0][0]) + ".jpg"
        print(Id)
        target = os.path.join(APP_ROOT, 'images/')
        # target = os.path.join(APP_ROOT, 'static/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print("Couldn't create upload directory: {}".format(target))
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename

            # Id = request.form['Id']
            # Id = Id + ".jpg"
            destination = "/".join([target, Id])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect("http://127.0.0.1:5000/")
    return render_template("index.html")




# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('logintransparent'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect("http://127.0.0.1:5000/")


@app.route('/registertran', methods=['GET', 'POST'])
def registertrans():


    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mobileno = form.mobileno.data


        curs = mysql.connection.cursor()

        curs.execute(
            "SELECT username FROM registration_table where (username)=(%s)", [username])
        datax = curs.fetchall()
        y=len(datax)
        mysql.connection.commit()

        # Close connection
        curs.close()
        if y==0:

            # Create cursor
            cur = mysql.connection.cursor()



            # Execute query
            cur.execute("INSERT INTO registration_table( name, username, email, password, mobile_no) VALUES(%s, %s, %s, %s, %s)", (name,  username, email, password, mobileno))

            cur.execute(
                "SELECT username FROM registration_table where (username)=(%s)",[username])
            data = cur.fetchall()
            print(data[0][0])
            Id = str(data[0][0]) + ".jpg"
            print(Id)
            target = os.path.join(APP_ROOT, 'images/')
            # target = os.path.join(APP_ROOT, 'static/')
            print(target)
            if not os.path.isdir(target):
                os.mkdir(target)
            else:
                print("Couldn't create upload directory: {}".format(target))
            print(request.files.getlist("file"))
            for upload in request.files.getlist("file"):
                print(upload)
                print("{} is the file name".format(upload.filename))
                filename = upload.filename

                # Id = request.form['Id']
                # Id = Id + ".jpg"
                destination = "/".join([target, Id])
                print("Accept incoming file:", filename)
                print("Save it to:", destination)
                upload.save(destination)
            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash('You are now registered and can log in', 'success')

            return redirect("http://127.0.0.1:5000/")
        else:
            flash('Username exist', 'failure')

    return render_template('registertran.html', form=form)



@app.route('/cart',methods=['GET'])
def cart():
    return render_template("cart.html")

# User loginmain
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM registration_table WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data[3]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect("http://127.0.0.1:5000/")
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')




@app.route('/Drinks', methods = ['GET'])
def Drinks():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from drinks_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Drinks.html", data = data, li = li,img = img ,l = l)





@app.route('/Baby_Food', methods = ['GET'])
def Baby_Food():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from baby_food_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Baby_Food.html", data = data, li = li,img = img ,l = l)



@app.route('/Biscuits', methods = ['GET'])
def Biscuits():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from biscuits_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Biscuits.html", data = data, li = li,img = img ,l = l)


@app.route('/Breads', methods = ['GET'])
def Breads():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from breads_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Breads.html", data = data, li = li,img = img ,l = l)



@app.route('/Life_Style', methods = ['GET'])
def Life_Style():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from life_style_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Life_Style.html", data = data, li = li,img = img ,l = l)

@app.route('/Meat', methods = ['GET'])
def Meat():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from meat_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Meat.html", data = data, li = li,img = img ,l = l)


@app.route('/Vegetables', methods = ['GET'])
def Vegetables():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from vegetables_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Vegetables.html", data = data, li = li,img = img ,l = l)


@app.route('/Snacks_&_Instants', methods = ['GET'])
def Snacks():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from snacks_table")
    data = cursor.fetchall()
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][1]) + ".jpg"
        print(data[d][1])
        img.append(b)

    # for c in img:
    #     print(c)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("Snacks_&_Instants.html", data = data, li = li,img = img ,l = l)


#
# @app.route('/Home_Care', methods = ['GET'])
# def Home_Care():
#     cursor = mysql.connection.cursor()
#     cursor.execute(
#         "SELECT id,Item_Name,Category,price from home_care_table")
#     data = cursor.fetchall()
#     x = len(data)
#     if x > 6:
#         l = x - 6
#     else:
#         l = 0
#     print(l)
#     if x > 6:
#         li = range(x - 6, x)
#         li = [*li]
#         li.reverse()
#     else:
#         li = range(0, x)
#         li = [*li]
#         li.reverse()
#
#     img = []
#
#     print(li)
#     for d in li:
#         b = str(data[d][1]) + ".jpg"
#         print(data[d][1])
#         img.append(b)
#
#     # for c in img:
#     #     print(c)
#
#     img = [*img]
#     img.reverse()
#     print(img)
#     return render_template("Home_Care.html", data = data, li = li,img = img ,l = l)

#
#
# @app.route('/Fish', methods = ['GET'])
# def Fish():
#     cursor = mysql.connection.cursor()
#     cursor.execute(
#         "SELECT id,Item_Name,Category,price from fish_table")
#     data = cursor.fetchall()
#     x = len(data)
#     if x > 6:
#         l = x - 6
#     else:
#         l = 0
#     print(l)
#     if x > 6:
#         li = range(x - 6, x)
#         li = [*li]
#         li.reverse()
#     else:
#         li = range(0, x)
#         li = [*li]
#         li.reverse()
#
#     img = []
#
#     print(li)
#     for d in li:
#         b = str(data[d][1]) + ".jpg"
#         print(data[d][1])
#         img.append(b)
#
#     # for c in img:
#     #     print(c)
#
#     img = [*img]
#     img.reverse()
#     print(img)
#     return render_template("Fish.html", data = data, li = li,img = img ,l = l)



#Trying Facade
#
#
#Trying Facade


@app.route('/Home_Care', methods = ['GET'])
def newHomeCare():
    facade= Facade()
    list=facade.home_care()
    return render_template("Home_Care.html", data=list['data'], li=list['li'], img=list['img'], l=list['l'])


@app.route('/Fish', methods = ['GET'])
def newFish():
    facade= Facade()
    list=facade.fish()
    return render_template("Fish.html", data=list['data'], li=list['li'], img=list['img'], l=list['l'])



@app.route('/Chocolate_&_Candies', methods = ['GET'])
def newChocolate():
    facade= Facade()
    list=facade.chocolate()
    return render_template("Chocolate_&_Candies.html", data=list['data'], li=list['li'], img=list['img'], l=list['l'])


@app.route('/Fruits', methods = ['GET'])
def newFruit():
    facade= Facade()
    list=facade.fruits()
    return render_template("Fruits.html", data=list['data'], li=list['li'], img=list['img'], l=list['l'])




#Trying Facade
#
#
#Trying Facade



# @app.route('/Fruits', methods = ['GET'])
# def Fruits():
#     cursor = mysql.connection.cursor()
#     cursor.execute(
#         "SELECT id,Item_Name,Category,price from fruits_table")
#     data = cursor.fetchall()
#     x = len(data)
#     if x > 6:
#         l = x - 6
#     else:
#         l = 0
#     print(l)
#     if x > 6:
#         li = range(x - 6, x)
#         li = [*li]
#         li.reverse()
#     else:
#         li = range(0, x)
#         li = [*li]
#         li.reverse()
#
#     img = []
#
#     print(li)
#     for d in li:
#         b = str(data[d][1]) + ".jpg"
#         print(data[d][1])
#         img.append(b)
#
#     # for c in img:
#     #     print(c)
#
#     img = [*img]
#     img.reverse()
#     print(img)
#     return render_template("Fruits.html", data = data, li = li,img = img ,l = l)


#Trying Proxy









# @app.route('/Chocolate_&_Candies', methods = ['GET'])
# def Chocolate():
#     cursor = mysql.connection.cursor()
#     cursor.execute(
#         "SELECT id,Item_Name,Category,price from chocolate_table")
#     data = cursor.fetchall()
#     x = len(data)
#     if x > 6:
#         l = x - 6
#     else:
#         l = 0
#     print(l)
#     if x > 6:
#         li = range(x - 6, x)
#         li = [*li]
#         li.reverse()
#     else:
#         li = range(0, x)
#         li = [*li]
#         li.reverse()
#
#     img = []
#
#     print(li)
#     for d in li:
#         b = str(data[d][1]) + ".jpg"
#         print(data[d][1])
#         img.append(b)
#
#     # for c in img:
#     #     print(c)
#
#     img = [*img]
#     img.reverse()
#     print(img)
#     return render_template("Chocolate_&_Candies.html", data = data, li = li,img = img ,l = l)



@app.route('/show_feedback', methods = ['GET'])
def show_feedback():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT name,email,phone_no,details from feedback")
    data = cursor.fetchall()
    x = len(data)
    if x > 10:
        l = x - 10
    else:
        l = 0
    print(l)
    if x > 10:
        li = range(x - 10, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    return render_template("show_feedback.html", data = data, li = li ,l = l)




@app.route('/add_item', methods=['GET', 'POST'])
def add_item():

    if request.method == 'POST':
        Item_Name = request.form['Item_Name']
        Category = request.form.get('Category')
        price = request.form['price']
        description = request.form['description']
        print(Item_Name)

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        if Category=='Life_Style':
            cur.execute(
                "INSERT INTO  life_style_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category=='Drinks':
            cur.execute(
                "INSERT INTO  drinks_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Chocolate_&_Candies':
            cur.execute(
                "INSERT INTO  chocolate_&_candies_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Meat':
            cur.execute(
                "INSERT INTO  meat_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Home_Care':
            cur.execute(
                "INSERT INTO  home_care_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Biscuits':
            cur.execute(
                "INSERT INTO  biscuits_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Breads':
            cur.execute(
                "INSERT INTO  breads_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Snacks_&_Instants':
            cur.execute(
                "INSERT INTO  snacks_&_instants_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Fruits':
            cur.execute(
                "INSERT INTO  fruits_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Fish':
            cur.execute(
                "INSERT INTO  fish_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Vegetables':
            cur.execute(
                "INSERT INTO  vegetables_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))
        elif Category == 'Baby_Food':
            cur.execute(
                "INSERT INTO  baby_food_table ( Item_name, Category, price, description) VALUES(%s, %s, %s, %s)",
                (Item_Name, Category, price, description))

       # data = cur.fetchall()
        #print(data[0][0])
        Id = str(Item_Name)+".jpg"
        print(Id)

        target = os.path.join(APP_ROOT, 'images/')
        # target = os.path.join(APP_ROOT, 'static/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print("Couldn't create upload directory: {}".format(target))
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename

            # Id = request.form['Id']
            # Id = Id + ".jpg"
            destination = "/".join([target, Id])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return redirect("http://127.0.0.1:5000/")
    return render_template("add_item.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_no = request.form['phone_no']
        details = request.form['details']

        print(name)
        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO  feedback(name,email,phone_no,details) VALUES(%s,%s,%s,%s)",(name,email,phone_no,details))



        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return redirect("http://127.0.0.1:5000/")
    return render_template("contact.html")



@app.route('/description/<string:id>', methods = ['GET'])
def description(id):
    Id = id
    # homeId = 12
    id_n = Id.split()
    print(id_n)
    cursor = mysql.connection.cursor()
    if  id_n[6] == 'Life_Style':
        cursor.execute(
            "SELECT Item_Name,Category,id,price from life_style_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Drinks":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from drinks_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Chocolate_&_Candies":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from drinks_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Meat":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from meat_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Home_Care":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from home_care_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Biscuits":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from biscuits_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Breads":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from breads_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Snacks_&_Instants":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from snacks_&_instants_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Fruits":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from fruits_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Fish":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from fish_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Vegetables":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from vegetables_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()
    elif id_n[6]=="Baby_Food":
        cursor.execute(
            "SELECT Item_Name,Category,id,price from baby_food_table WHERE id=%s", [id_n[2]])
        g_data = cursor.fetchall()

        cursor.execute(
            "SELECT description from drinks_table WHERE id=%s", [id_n[2]])
        des_data = cursor.fetchall()

    #img = Item_Name+'.jpg'
    return render_template("description.html",g_data = g_data, des_data = des_data)





#Trying Proxy
#
#
#Trying Proxy


# class Subject:
#     def search_result(self):
#         print()
#
#
#
# class Proxy(Subject):
#     def __init__(self, real_subject,Item_Name,Category):
#         self._real_subject = real_subject
#         self.Item_Name=Item_Name
#         self.Category=Category
#     def search_result(self):
#         dict = self._real_subject.search_result(self.Category, self.Item_Name)
#         if dict['data'] is None:
#             dict=[]
#         return  dict
#
#
# class RealSubject(Subject):
#     def search_result(self,Category,Item_Name):
#
#         cur = mysql.connection.cursor()
#         if Category == 'Life_Style':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM life_style_table where Item_Name = %s ",
#                 [Item_Name])
#
#         elif Category == 'Drinks':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, id FROM drinks_table where Item_Name = %s ", [Item_Name])
#
#         elif Category == 'Chocolate_&_Candies':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM chocolate_table where Item_Name = %s ",
#                 [Item_Name])
#         elif Category == 'Meat':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM meat_table where Item_Name = %s ", [Item_Name])
#         elif Category == 'Home_Care':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM home_care_table where Item_Name = %s ",
#                 [Item_Name])
#         elif Category == 'Biscuits':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM biscuits_table where Item_Name = %s ", [Item_Name])
#         elif Category == 'Breads':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM breads_table where Item_Name = %s ", [Item_Name])
#         elif Category == 'Snacks_&_Instants':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, id FROM snacks_table where Item_Name = %s ", [Item_Name])
#         elif Category == 'Fruits':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM fruits_table where Item_Name = %s ", [Item_Name])
#         elif Category == 'Fish':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM fish_table where Item_Name = %s ", [Item_Name])
#         elif Category == 'Vegetables':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM vegetables_table where Item_Name = %s ",
#                 [Item_Name])
#         elif Category == 'Baby_Food':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM baby_fruits_table where Item_Name = %s ",
#                 [Item_Name])
#
#         data = cur.fetchall()
#
#         x = len(data)
#         if x > 6:
#             l = x - 6
#         else:
#             l = 0
#         print(l)
#         if x > 6:
#             li = range(x - 6, x)
#             li = [*li]
#             li.reverse()
#         else:
#             li = range(0, x)
#             li = [*li]
#             li.reverse()
#
#         img = []
#
#         print(li)
#         for d in li:
#             b = str(data[d][0]) + ".jpg"
#             print(data[d][0])
#             img.append(b)
#
#         # for c in img:
#         #     print(c)
#
#         img = [*img]
#         img.reverse()
#         print(img)
#
#         # Commit to DB
#         mysql.connection.commit()
#
#         # Close connection
#         cur.close()
#
#         print()
#
#         return {'data': data, 'li': li, 'img': img, 'l': l}
#



@app.route('/search_result', methods=['GET', 'POST'])
def search_result():
    if request.method == 'POST':
        Item_Name = request.form['Item_Name']
        Category = request.form.get('Category')
        realObj= RealSubject()
        proxyObj=Proxy(realObj,Item_Name,Category)
        list=proxyObj.search_result()
        if len(list)==0:
            return render_template("search_result.html")
        else:
            return render_template("search_result.html",data=list['data'], li=list['li'], img=list['img'], l=list['l'])
    return render_template("search_result.html")














# @app.route('/search_result', methods=['GET', 'POST'])
# def search_result():
#     if request.method == 'POST':
#         Item_Name = request.form['Item_Name']
#         Category = request.form.get('Category')
#
#
#         cur = mysql.connection.cursor()
#
#
#         if Category=='Life_Style':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM life_style_table where Item_Name = %s ",[Item_Name])
#
#         elif Category=='Drinks':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, id FROM drinks_table where Item_Name = %s ",[Item_Name])
#
#         elif Category == 'Chocolate_&_Candies':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM chocolate_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Meat':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM meat_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Home_Care':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM home_care_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Biscuits':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM biscuits_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Breads':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM breads_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Snacks_&_Instants':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, id FROM snacks_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Fruits':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM fruits_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Fish':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM fish_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Vegetables':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM vegetables_table where Item_Name = %s ",[Item_Name])
#         elif Category == 'Baby_Food':
#             cur.execute(
#                 "SELECT Item_Name, Category, price, description FROM baby_fruits_table where Item_Name = %s ",[Item_Name])
#
#
#
#         data = cur.fetchall()
#
#         x = len(data)
#         if x > 6:
#             l = x - 6
#         else:
#             l = 0
#         print(l)
#         if x > 6:
#             li = range(x - 6, x)
#             li = [*li]
#             li.reverse()
#         else:
#             li = range(0, x)
#             li = [*li]
#             li.reverse()
#
#         img = []
#
#         print(li)
#         for d in li:
#             b = str(data[d][0]) + ".jpg"
#             print(data[d][0])
#             img.append(b)
#
#         # for c in img:
#         #     print(c)
#
#         img = [*img]
#         img.reverse()
#         print(img)
#
#         # Commit to DB
#         mysql.connection.commit()
#
#         # Close connection
#         cur.close()
#
#         return render_template("search_result.html",data=data, li=li, img=img, l=l)
#     return render_template("search_result.html")




if __name__ == '__main__':
    app.secret_key='secret123'
    app.run()
