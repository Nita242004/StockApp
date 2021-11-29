import pymysql
import db_config
from tkinter import *
from tkinter import messagebox

def mysqlconnect():
  #to connect MySql database
  conn = pymysql.connect(
        host = 'localhost',
        user='root',
        password='',
        db='ComsciIA')

  return conn

# def load_database_result():
#
#
#         con = pymysql.connect(host=db_config.DB_SERVER,
#                               user=db_config.DB_USER,
#                               password=db_config.DB_PASS,
#                               database=db_config.DB)
#         print(str(con))
#         # messagebox.showinfo("Connected to Database")
#         print("connected")
#
#
# load_database_result()

# import pymysql.cursors
#
# try:
#     connection = pymysql.connect(host='192.168.64.3',
#                                  user='root',
#                                  password='',
#                                  db='ComsciIA',
#                                  port=3306)
#
# except Exception as e:
#     print('connection failed')
#     print(e)
#
# import mysql.connector
#
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword")
#
# print(mydb)
