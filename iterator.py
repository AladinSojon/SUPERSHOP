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




class Iterator:
    def hasNext(self):
        pass
    def Next(self):
        pass
class Container:
    def getIterator(self):
        pass



class Menu(Container):
    def __init__(self,li):
        self.li = li
    def getIterator(self):
        return NameIterator(self.li)


class NameIterator(Iterator):
    def __init__(self,li):
        self.index = 0
        self.li = li

    def hasNext(self):
        if self.index < len(self.li):
            return True
        else:
            return False
    def Next(self):
        item = self.li[self.index]
        self.index+=1
        return item

# class iterator_main:
#
#
#     for d in li:
#         b = str(data[d][1]) + ".jpg"
#         print(data[d][1])
#         img.append(b)

# class RoundPeg:
#     def __init__(self,lis):
#         self.lis = lis
#     def create_list(self):
#         return self.lis


