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



class Subject:
    def search_result(self):
        print()



class Proxy(Subject):
    def __init__(self, real_subject,Item_Name,Category):
        self._real_subject = real_subject
        self.Item_Name=Item_Name
        self.Category=Category
    def search_result(self):
        dict = self._real_subject.search_result(self.Category, self.Item_Name)
        if dict['data'] is None:
            dict=[]
        return  dict


class RealSubject(Subject):
    def search_result(self,Category,Item_Name):

        cur = mysql.connection.cursor()
        if Category == 'Life_Style':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM life_style_table where Item_Name = %s ",
                [Item_Name])

        elif Category == 'Drinks':
            cur.execute(
                "SELECT Item_Name, Category, price, id FROM drinks_table where Item_Name = %s ", [Item_Name])

        elif Category == 'Chocolate_&_Candies':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM chocolate_table where Item_Name = %s ",
                [Item_Name])
        elif Category == 'Meat':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM meat_table where Item_Name = %s ", [Item_Name])
        elif Category == 'Home_Care':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM home_care_table where Item_Name = %s ",
                [Item_Name])
        elif Category == 'Biscuits':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM biscuits_table where Item_Name = %s ", [Item_Name])
        elif Category == 'Breads':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM breads_table where Item_Name = %s ", [Item_Name])
        elif Category == 'Snacks_&_Instants':
            cur.execute(
                "SELECT Item_Name, Category, price, id FROM snacks_table where Item_Name = %s ", [Item_Name])
        elif Category == 'Fruits':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM fruits_table where Item_Name = %s ", [Item_Name])
        elif Category == 'Fish':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM fish_table where Item_Name = %s ", [Item_Name])
        elif Category == 'Vegetables':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM vegetables_table where Item_Name = %s ",
                [Item_Name])
        elif Category == 'Baby_Food':
            cur.execute(
                "SELECT Item_Name, Category, price, description FROM baby_fruits_table where Item_Name = %s ",
                [Item_Name])

        data = cur.fetchall()

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
            b = str(data[d][0]) + ".jpg"
            print(data[d][0])
            img.append(b)

        # for c in img:
        #     print(c)

        img = [*img]
        img.reverse()
        print(img)

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        print()

        return {'data': data, 'li': li, 'img': img, 'l': l}

