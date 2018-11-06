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




class Items:

    def getChocolate(self):
        print('dkjfhelgkehf')
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id,Item_Name,Category,price from chocolate_table")

        data = cursor.fetchall()
        x = len(data)
        l=0
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
        return {'data':data, 'li':li, 'img':img, 'l':l}

    def getHomeCare(self):
        print('dkjfhelgkehf')
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id,Item_Name,Category,price from home_care_table")

        data = cursor.fetchall()
        x = len(data)
        l=0
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
        return {'data':data, 'li':li, 'img':img, 'l':l}





    def getFish(self):
        print('dkjfhelgkehf')
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id,Item_Name,Category,price from fish_table")

        data = cursor.fetchall()
        x = len(data)
        l=0
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
        return {'data':data, 'li':li, 'img':img, 'l':l}





    def getFruits(self):
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
        return {'data': data, 'li': li, 'img': img, 'l': l}


class Facade:
    def __init__(self):
        self.item = Items()



    def chocolate(self):
        return self.item.getChocolate()

    def fruits(self):
        return self.item.getFruits()

    def fish(self):
        return self.item.getFish()

    def home_care(self):
        return self.item.getHomeCare()


