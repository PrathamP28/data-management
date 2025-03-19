import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, END
import configparser
import mysql.connector
import random
import pandas as pd
import os 
import sys

inAction = False

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
login_user= config["login"]["user"]
login_password= config["login"]["password"]

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor()

def fetch_data():
    try:
        mycursor.execute("SELECT * FROM database1")
        rows = mycursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return []
    
def displayTree():
    for items in treeview1.get_children():
        treeview1.delete(items)

    data = fetch_data()
    for row in data:
        treeview1.insert("",END,text=row[0],values=row[1:])

def selectItem():
    global selectedItem,index
    selectedItem = treeview1.selection()
    index = treeview1.index(selectedItem)

def generate_username(name,role):
    n = random.randint(100, 999)
    username = f"{role[0].lower()}{name.lower()}{n}"
    return username

def isDigit(string):
    string = list(string)
    for letters in string:
        if letters.isdecimal():
            return True
    return False

def checkMail(enteredMail):
    mycursor.execute("SELECT * FROM database1")
    rows = mycursor.fetchall()
    selectItem()
    for i,item in enumerate(rows):
        if (enteredMail in item) and (i != index):
            return True
    return False

def checkMail1(enteredMail):
    mycursor.execute("SELECT * FROM database1")
    rows = mycursor.fetchall()
    selectItem()
    for item in rows:
        if (enteredMail in item):
            return True
    return False

def submit():
    name = entry1.get()
    mail = entry2.get()
    role = combo.get()
    username = generate_username(name,role)
    if checkMail1(mail):
        messagebox.showerror("Email already Entered","The Email you're trying to enter already exsist")
    else:
        if isDigit(name):
            messagebox.showerror("Name not Valid","Enter a Valid Name")
        
        else:
            if name.strip() == "" or mail.strip() == "":
                messagebox.showerror("field must be entered.","field must be entered.")

            else:
                additem(name,username,mail,role)
                entry1.delete(0,END)
                entry2.delete(0,END)
                combo.set("User")
                displayTree()

def additem(name,username,mail,role):
    sql = "INSERT INTO database1 (name, username, mail, role) VALUES (%s, %s, %s, %s)"
    val = (name,username,mail,role)
    mycursor.execute(sql, val)
    mydb.commit()

def removeItem():
    data = fetch_data()
    selectItem()
    try:
        sql = f"DELETE FROM database1 WHERE username = '{data[index][1]}'"

        mycursor.execute(sql)

        mydb.commit()
        treeview1.delete(selectedItem)
    except:
        messagebox.showerror("Nothing Selected","Select an Item to Delete")

def editItem():
    global inAction,edit
    data = fetch_data()
    def editData():
        global inAction
        newName = edit_entry1.get()
        newMail = edit_entry2.get()
        newRole = edit_combo.get()
        if checkMail(newMail):
            messagebox.showerror("Email already Entered","The Email you're trying to enter already exsist")
        else:
            if isDigit(newName):
                messagebox.showerror("Name not Valid","Enter a Valid Name")
            else:
                if newName.strip() == "" or newMail.strip() == "":
                    messagebox.showerror("Nothing Entered","Field must be Entered")
                else:
                    inAction = False
                    delete = f"DELETE FROM database1 WHERE username = '{data[index][1]}'"
                    mycursor.execute(delete)

                    mydb.commit()
                    additem(newName,userName,newMail,newRole)
                    edit.destroy()
                    displayTree()

    def close():
        global inAction
        inAction = False
        edit.destroy()

    if inAction == True:
        messagebox.showerror("Action already running","Please stop the action to run")
        edit.destroy()
        inAction = False

    else:
        selectItem()
        if not selectedItem:
            messagebox.showerror("Nothing Selected","Select an item to edit it")
            inAction = False
        else:
            
            edit = tb.Toplevel(app)
            inAction = True
            p1 = tb.PhotoImage(file = 'icon.png') 
            edit.iconphoto(False, p1) 
            data = fetch_data()
            userName = data[index][1]

            style = tb.Style("darkly")

            edit.title("Edit")
            ex = int((edit.winfo_screenwidth()+925)//2)
            ey = int((edit.winfo_screenheight()-280)//2)
            edit.geometry(f"240x280+{str(ex)}+{str(ey)}")
            edit.resizable(width=False, height=False)
            labelframe = tb.LabelFrame(edit, text="Edit Data", bootstyle="light", padding=10)  
            labelframe.pack(side=LEFT, anchor="nw", padx=10, pady=10)

            edit_title1 = tb.Label(labelframe, text="Enter Your Name:")
            edit_title1.pack(anchor="w")

            edit_entry1 = tb.Entry(labelframe, width=30)
            edit_entry1.pack(pady=5, fill=X)
            edit_entry1.insert(0,data[index][0])

            edit_title2 = tb.Label(labelframe, text="Enter Your Email:")
            edit_title2.pack(anchor="w")

            edit_entry2 = tb.Entry(labelframe)
            edit_entry2.pack(pady=5, fill=X)
            edit_entry2.insert(0,data[index][2])

            edit_combo = tb.Combobox(labelframe, values=["Admin", "User", "Temp"],state="readonly")
            edit_combo.pack(pady=15, anchor="w")
            edit_combo.set(f"{data[index][3]}")

            edit_button_frame = tb.Frame(labelframe)
            edit_button_frame.pack(pady=5)

            edit_editBtn = tb.Button(edit_button_frame, text="Edit Data", bootstyle="warning-outline",command=editData)
            edit_editBtn.grid(row=0, column=1, padx=5, pady=5)

            edit_close = tb.Button(edit_button_frame,text="Close",bootstyle="secondary-outline",command=close)
            edit_close.grid(row=0,column=2, padx=5, pady=5)

            edit.mainloop()

def reset():
    mycursor.execute("DELETE FROM database1")
    mydb.commit()
    displayTree()

def excel():
    conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

    query = "SELECT * FROM database1"
    df = pd.read_sql(query, conn)

    df.to_excel("excel\\database.xlsx", index=False,engine="openpyxl")
    file_path = os.path.abspath("excel\\database.xlsx")
    folder_path = os.path.dirname(file_path)
    os.startfile(folder_path)
    conn.close()

def login():
    # username = entry_username.get()
    password = entry_password.get()
    
    # if username == login_user and password == login_password:
    if password == login_password:
        login_window.withdraw()
        open_home_page()

    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


def openFolder():
    file_path = os.path.abspath("excel\\database.xlsx")
    folder_path = os.path.dirname(file_path)
    os.startfile(folder_path)

def open_home_page():
    global entry1 ,entry2 ,combo,treeview1,app
    app = tb.Toplevel(login_window) 
    style = tb.Style("darkly")  
    p1 = tb.PhotoImage(file = 'icon.png') 
    app.iconphoto(False, p1) 

    app.title("Role Manager")
    hpx = int((app.winfo_screenwidth()-880)//2)
    hpy = int((app.winfo_screenheight()-400)//2)
    app.geometry(f"880x400+{str(hpx)}+{str(hpy)}")
    app.resizable(width=False, height=False)
    
    app.protocol("WM_DELETE_WINDOW", on_close) 

    theme_selection = tb.Frame(app, padding=(10, 10, 10, 0))
    theme_selection.pack(fill=X)

    theme_selected = tb.Label(
        master=theme_selection, 
        text="Role Manager", 
        font="-size 24 -weight bold"
    )
    theme_selected.pack(side=LEFT)

    # lbl = tb.Label(theme_selection, text="Select a Database:")
    # theme_cbo = tb.Combobox(theme_selection)
    # theme_cbo.pack(padx=10, side=RIGHT)
    # lbl.pack(side=RIGHT)
    open_file = tb.Button(theme_selection, text="Open Excel Folder", bootstyle="success-outline",command=openFolder)
    open_file.pack(padx=10, side=RIGHT)

    labelframe = tb.LabelFrame(app, text="My Data", bootstyle="light", padding=10)  
    labelframe.pack(side=LEFT, anchor="nw", padx=10, pady=10)

    title1 = tb.Label(labelframe, text="Enter Your Name:")
    title1.pack(anchor="w")

    entry1 = tb.Entry(labelframe, width=30)
    entry1.pack(pady=5, fill=X)

    title2 = tb.Label(labelframe, text="Enter Your Email:")
    title2.pack(anchor="w")

    entry2 = tb.Entry(labelframe)
    entry2.pack(pady=5, fill=X)

    combo = tb.Combobox(labelframe, values=["Admin", "User", "Temp"],state="readonly")
    combo.pack(pady=15, anchor="w")
    combo.set("User")

    button_frame = tb.Frame(labelframe)
    button_frame.pack(pady=5, fill=X)

    submitbtn = tb.Button(button_frame, text="Submit", bootstyle="success-outline",command=submit)
    submitbtn.grid(row=0, column=0, padx=5, pady=5)
    editBtn = tb.Button(button_frame, text="Edit", bootstyle="warning-outline",command=editItem)
    editBtn.grid(row=0, column=1, padx=5, pady=5)
    removeBtn = tb.Button(button_frame, text="Remove", bootstyle="danger-outline",command=removeItem)
    removeBtn.grid(row=0, column=2, padx=5, pady=5)
    tb.Button(button_frame, text="Excel", bootstyle="success-outline",command=excel).grid(row=1, column=0, padx=5, pady=5)
    tb.Button(button_frame, text="Clear all", bootstyle="primary-outline",command=reset).grid(row=1, column=1, padx=5, pady=5)
    tb.Button(button_frame, text="Close", bootstyle="secondary-outline", command=app.destroy and login_window.destroy).grid(row=1, column=2, padx=5, pady=5)

    treeFrame = tb.LabelFrame(app, text="Data Display", bootstyle="light", padding=10,width= 1000)
    treeFrame.pack(side=LEFT, anchor="n", padx=5, pady=10)

    cols = ["Username","Mail", "Role"]
    treeview1 = tb.Treeview(treeFrame, columns=cols, height=14)
    treeview1.pack(padx=5, pady=5, side=TOP, anchor="n",fill="both")

    treeview1.heading("#0", text="Name")
    treeview1.column("#0",minwidth=100,width=100)
    treeview1.heading("Username", text="Username")
    treeview1.column("Username",minwidth=100,width=100)
    treeview1.heading("Mail", text="Mail")
    treeview1.column("Mail",minwidth=250,width=250)
    treeview1.heading("Role", text="Role")
    treeview1.column("Role",minwidth=100,width=100)
    
    displayTree()

# Creating login window
login_window = tb.Window(themename="darkly")
login_window.title("Login Page")
p1 = tb.PhotoImage(file = 'icon.png') 
login_window.iconphoto(False, p1) 
x = int((login_window.winfo_screenwidth() - 250)//2)
y = int((login_window.winfo_screenheight() - 250)//2)
login_window.geometry(f"250x250+{str(x)}+{str(y)}")
login_window.resizable(width=False,height=False)

def on_close():
    login_window.destroy()

label_frame = tb.LabelFrame(login_window, text="My Data", bootstyle="light", padding=15)  
label_frame.pack(padx=10, pady=10, expand=True)

# tb.Label(label_frame, text="Username:").pack()
# entry_username = tb.Entry(label_frame)
# entry_username.pack()

tb.Label(label_frame, text="Password:").pack()
entry_password = tb.Entry(label_frame, show="*")
entry_password.pack()

tb.Button(label_frame, text="Login", bootstyle="success-outline", command=login).pack(pady=10,side="left")
tb.Button(label_frame, text="Close", bootstyle="secondary-outline", command=on_close).pack(pady=10,side="right")

login_window.mainloop()