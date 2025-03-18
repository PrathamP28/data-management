import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from configparser import ConfigParser 
  
configur = ConfigParser() 
configur.read('config.ini') 

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # if username == "a" and password == "a":
    if True == True:
        login_window.withdraw()  # Hide the login window instead of destroying it
        open_home_page()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def open_home_page():
    app = tb.Toplevel(login_window)  # Attach to main window
    style = tb.Style("darkly")  

    app.title("DM")
    app.geometry("1000x400")
    app.resizable(width=False, height=False)

    def on_close():
        app.destroy()
        login_window.deiconify()  # Show login window again when closing

    app.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close

    theme_selection = tb.Frame(app, padding=(10, 10, 10, 0))
    theme_selection.pack(fill=X)

    theme_selected = tb.Label(
        master=theme_selection, 
        text="Role Manager", 
        font="-size 24 -weight bold"
    )
    theme_selected.pack(side=LEFT)

    lbl = tb.Label(theme_selection, text="Select a Database:")
    theme_cbo = tb.Combobox(theme_selection)
    theme_cbo.pack(padx=10, side=RIGHT)
    lbl.pack(side=RIGHT)

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

    combo = tb.Combobox(labelframe, values=["Admin", "User", "Temp"])
    combo.pack(pady=15, anchor="w")
    combo.set("Select Role")

    button_frame = tb.Frame(labelframe)
    button_frame.pack(pady=5, fill=X)

    tb.Button(button_frame, text="Submit", bootstyle="success-outline").grid(row=0, column=0, padx=5, pady=5)
    tb.Button(button_frame, text="Edit", bootstyle="warning-outline").grid(row=0, column=1, padx=5, pady=5)
    tb.Button(button_frame, text="Remove", bootstyle="danger-outline").grid(row=0, column=2, padx=5, pady=5)
    tb.Button(button_frame, text="Advance", bootstyle="danger-outline").grid(row=1, column=0, padx=5, pady=5)
    tb.Button(button_frame, text="Reset", bootstyle="primary-outline").grid(row=1, column=1, padx=5, pady=5)
    tb.Button(button_frame, text="Close", bootstyle="secondary-outline", command=on_close).grid(row=1, column=2, padx=5, pady=5)

    treeFrame = tb.LabelFrame(app, text="Data Display", bootstyle="light", padding=10,width= 1000)
    treeFrame.pack(side=LEFT, anchor="n", padx=10, pady=10)

    cols = ["Mail", "Role","Username"]
    treeview1 = tb.Treeview(treeFrame, columns=cols, height=14)
    treeview1.pack(padx=5, pady=5, side=TOP, anchor="n",fill="both")

    treeview1.heading("#0", text="Name")
    treeview1.heading("Mail", text="Mail")
    treeview1.heading("Role", text="Role")
    treeview1.heading("Username", text="Username")


# Creating login window
login_window = tb.Window(themename="darkly")
login_window.title("Login Page")
login_window.geometry("250x250")
login_window.resizable(width=False,height=False)

def on_close():
    login_window.destroy()

label_frame = tb.LabelFrame(login_window, text="My Data", bootstyle="light", padding=15)  
label_frame.pack(padx=10, pady=10, expand=True)

tb.Label(label_frame, text="Username:").pack()
entry_username = tb.Entry(label_frame)
entry_username.pack()

tb.Label(label_frame, text="Password:").pack()
entry_password = tb.Entry(label_frame, show="*")
entry_password.pack()

tb.Button(label_frame, text="Login", bootstyle="success-outline", command=login).pack(pady=10,side="left")
tb.Button(label_frame, text="Close", bootstyle="secondary-outline", command=on_close).pack(pady=10,side="right")

login_window.mainloop()