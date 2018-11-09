import gc
import os
from tkinter import messagebox
from adapter import *
from iterator import *
from Observer import *
from Search import *




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




class Mediator:
    def __init__(self,data):
        self.data=data
        self.x=len(data)

        if self.x > 10:
            self.l = self.x - 10
        else:
            self.l = 0
        print(self.l)
        if self.x > 10:
            self.li = range(self.x - 10, self.x)
            self.li = [*self.li]
            self.li.reverse()
        else:
            self.li = range(0, self.x)
            self.li = [*self.li]
            self.li.reverse()

    def get_li(self):
        return self.li

    def get_l(self):
        return self.l




class User:
    def __init__(self,username):
        self.username=username
        cursor = mysql.connection.cursor()
        cursor.execute(
        "SELECT Item_Name,Category,price,username FROM cart_table where username = %s ",[self.username])
        self.data = cursor.fetchall()
        self.md = Mediator(self.data)

    def get_li(self):
        return self.md.get_li()

    def get_l(self):
        return self.md.get_l()

    def get_data(self):
        return self.data


