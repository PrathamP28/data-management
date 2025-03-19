import mysql.connector
import configparser
import os 
import sys

if getattr(sys, 'frozen', False):
    baseDirectory = sys._MEIPASS
else:
    baseDirectory = os.path.dirname(__file__)

config_path = os.path.join(baseDirectory, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

host= config["database"]["host"]
user= config["database"]["user"]
password= config["database"]["password"]
database= config["database"]["database"]

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE database1")

mycursor.close()

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE database1 (name VARCHAR(255), username VARCHAR(255), mail VARCHAR(255), role VARCHAR(255))")
mydb.commit()