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





class SingleTone():
    __instance = None
    @staticmethod
    def getIns(self):
      if self.__instance is None:
        self.__instance = SubjectConcrete()
      return self.__instance

class Observer:
    def update(self):
        pass

class Subject:

    def registerObserver(self):
        pass
    def removeObserver(self,observer):
        pass
    def notifyObserver(self):
        pass

class SubjectConcrete(Subject):
    observer_list= []
    def __init__(self):
        pass
    def registerObserver(self,obser):
        self.observer_list.append(obser)

    # def setNotification(self, notification):
    #     self.notification = notification

    def removeObserver(self,obser):
        self.observer_list.remove(obser)
        curs = mysql.connection.cursor()
        curs.execute(
            "DELETE FROM registration_table WHERE username=%s",
            (obser.username))
        mysql.connection.commit()
        curs.close()

    def notifyObserver(self,notification):
        self.notification = notification
        for d in self.observer_list:
            d.update(self.notification)




# global_subject = SubjectConcrete()

class ObserverConcrete(Observer):
    def __init__(self,username):
        self.username = username

    def get_username(self):
        return self.username

    def update(self,notification):
        self.notification=notification
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO notification_table(username, notification) VALUES(%s, %s)",
            (self.username,self.notification))
        mysql.connection.commit()
        cur.close()

