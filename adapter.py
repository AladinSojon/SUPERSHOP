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




class range_class:
    def __init__(self,range_item):
        self.range_item = range_item
    def getRangeItem(self):
        return self.range_item

class range_adapter:
    def __init__(self,range_cl):
        self.range_cl = range_cl
    def create_list(self):
        li =[*self.range_cl.getRangeItem()]
        return li


