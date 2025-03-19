import mysql.connector
import configparser
import os 
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(__file__)

config_path = os.path.join(BASE_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

host= config["database"]["host"]
user= config["database"]["user"]
password= config["database"]["password"]
database= config["database"]["database"]

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE database1 (name VARCHAR(255), username VARCHAR(255), mail VARCHAR(255), role VARCHAR(255))")


