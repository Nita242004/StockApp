from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image
from ttkbootstrap import Style
from tkinter import ttk
import db_conn

class Login:
    def __init__(self):
        # customizing style, colors, fonts
        self.style = Style(theme='lumen')
        self.root = self.style.master
        # making custom style
        self.style.configure('TButton', font=("Helvetica", 16))
        self.style.configure('my.TButton', font=("Helvetica", 10))
        # style.configure('info.TButton', font=("Helvetica", 12))
        # style.configure('TNotebook.Tab', tabposition='n', font=('Helvetica', 16))
        self.style.configure("menustyle.TFrame", background="gray")

        self.root.title("Login Window")

        #textbox labels and labels
        # Tab
        self.tabControl = ttk.Notebook(self.root, style='login.TNotebook')
        self.tabControl.grid(row=1, column=0, columnspan=2, padx=30, pady=20)

        self.login = ttk.Frame(self.root)
        self.signup = ttk.Frame(self.root)

        self.tabControl.add(self.login, text="Login")
        self.tabControl.add(self.signup, text="Signup")

    #login
        #textbox labels and labels
        self.usernameLabel = ttk.Label(self.login, text="   Username: ", style='primary.TLabel')
        self.usernameLabel.grid(row=1, column=0, ipadx= 5, ipady=20, sticky=E)

        self.username = StringVar()
        self.usernameEntry = ttk.Entry(self.login, textvariable=self.username, style='info.TEntry')
        self.usernameEntry.grid(row=1, column=1, sticky=W)

        self.passwordLabel = ttk.Label(self.login, text="   Password: ", style='primary.TLabel')
        self.passwordLabel.grid(row=2, column=0, ipadx= 5, ipady=20, sticky=E)

        self.password = StringVar()
        self.passwordEntry = ttk.Entry(self.login, textvariable=self.password, style='info.TEntry')
        self.passwordEntry.grid(row=2, column=1, sticky=W)

        # hide pass checkbox
        self.var1 = IntVar()
        self.b = ttk.Checkbutton(self.login, text="Hide Password", onvalue=1, variable=self.var1, command=self.hidepass,
                            style='info.TCheckbutton')
        self.b.grid(row=2, column=4, sticky=E, padx=10)

        # login button
        self.btn_login = ttk.Button(self.login, text="Login", width=10, command = self.checkLogin, style='my.TButton').grid(row=4, column=0,columnspan=2,sticky=S)

    #signup
        # textbox labels and labels
        self.firstnameLabel2 = ttk.Label(self.signup, text="Firstname: ", ).grid(row=0, column=0)
        self.firstname2 = StringVar()
        self.firstnameEntry2 = ttk.Entry(self.signup, textvariable=self.firstname2)
        self.firstnameEntry2.grid(row=0, column=1)

        self.lastnameLabel2 = ttk.Label(self.signup, text="Lastname: ", ).grid(row=1, column=0)
        self.lastname2 = StringVar()
        self.lastnameEntry2 = ttk.Entry(self.signup, textvariable=self.lastname2)
        self.lastnameEntry2.grid(row=1, column=1)

        self.emailLabel2 = ttk.Label(self.signup, text="Email: ", ).grid(row=2, column=0)
        self. email2 = StringVar()
        self.emailEntry2 = ttk.Entry(self.signup, textvariable=self.email2)
        self.emailEntry2.grid(row=2, column=1)

        self.usernameLabel2 = ttk.Label(self.signup, text="Username: ", ).grid(row=3, column=0)
        self.username2 = StringVar()
        self.usernameEntry2 = ttk.Entry(self.signup, textvariable=self.username2)
        self.usernameEntry2.grid(row=3, column=1)

        self.passwordLabel2 = ttk.Label(self.signup, text="Password: ", ).grid(row=4, column=0)
        self.password2 = StringVar()
        self.passwordEntry2 = ttk.Entry(self.signup, textvariable=self.password2)
        self.passwordEntry2.grid(row=4, column=1)

        # signup button
        self.btn_signup = ttk.Button(self.signup, text="Signup", width=10, command=self.insertNewuser)
        self.btn_signup.grid(row=5, column=1)

        self.root.mainloop()

    def checkLogin(self):
        self.txt_username = self.username.get()
        self.txt_password = self.password.get()
        print(self.txt_username)
        print(self.txt_password)

        self.sql = "SELECT count(*) FROM tbl_user_profile  where username = '" + self.txt_username + "' and password = '" + self.txt_password + "'"
        # count(*)= check through all rows
        self.conn = db_conn.mysqlconnect()
        self.cur = self.conn.cursor()
        self.cur.execute(self.sql)  # execute sql query

        self.result = self.cur.fetchone()
        # fetchone = makes into table (only one row, but if multiple rows=fetchall)
        if self.result[0] == 1:
            self.root.withdraw()
            import IndustriesScreen as IndustriesScreen
            IndustriesScreen = IndustriesScreen.industry(self.root, self.txt_username)

            # nameoffile.nameofclass

        else:
            # messagebox.showinfo("wrong password/username")
            messagebox.showinfo("result", "wrong password or username")

                # fetchone = makes into table (only one row, but if multiple rows=fetchall)

    def insertNewuser(self):
        self.txt_username2 = self.username2.get()
        self.txt_password2 = self.password2.get()
        self.txt_firstname2 = self.firstname2.get()
        self.txt_lastname2 = self.lastname2.get()
        self.txt_email2 = self.email2.get()

        self.conn2 = db_conn.mysqlconnect()
        self.cur2 = self.conn2.cursor()

        self.sql2 = "INSERT INTO tbl_user_profile (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s)"
        self.val2 = (self.txt_firstname2, self.txt_lastname2, self.txt_email2, self.txt_username2, self.txt_password2)
        self.cur2.execute(self.sql2, self.val2)

        self.conn2.commit()
        print(self.cur2.rowcount, "record inserted.")
        messagebox.showinfo("result", "User created")

    def hidepass(self):
        if self.var1.get() == 1:
            self.passwordEntry = ttk.Entry(self.login, textvariable=self.password, show="*", style='info.TEntry').grid(row=2, column=1, sticky=W)
        else:
            self.passwordEntry = ttk.Entry(self.login, textvariable=self.password, style='info.TEntry').grid(row=2, column=1, sticky=W)

Login()