import gc
import os
from tkinter import messagebox



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


@app.route('/Fruits', methods = ['GET'])
def Fruits():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id,Item_Name,Category,price from fruits_table")
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
    return render_template("Fruits.html", data = data, li = li,img = img ,l = l)



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





if __name__ == '__main__':
    app.secret_key='secret123'
    app.run()
