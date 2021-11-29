from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image
from ttkbootstrap import Style
import tkinter as tk
from tkinter import ttk
import db_conn
from overlay import Window

class profile:
    def __init__(self, root1, user):
        self.username = user

        self.style = Toplevel(root1)
        self.root = self.style
        self.root.title("Profile")

        # all imported info bout profile
        self.profileinfo = []
        self.profileinfo = self.profileInformation()
        self.usern = self.profileinfo[0][0]
        self.firstn = self.profileinfo[0][1]
        self.lastn = self.profileinfo[0][2]
        self.email = self.profileinfo[0][3]

        # menu section:
        # menu
        self.mb = ttk.Menubutton(self.root, style='primary.TMenubutton')
        # create menu
        self.menu = tk.Menu(self.mb)
        # add options
        self.option_var = tk.StringVar()
        self.menu.add_radiobutton(label="Industries", value=0, variable=self.option_var, command=self.gotoindustries)
        self.menu.add_radiobutton(label="Bookmarks", value=1, variable=self.option_var, command=self.gotobookmark)
        self.menu.add_radiobutton(label="Profile", value=2, variable=self.option_var, command=self.gotoprofile)
        self.menu.add_radiobutton(label="Logout", value=3, variable=self.option_var, command=self.gotologin)
        # associate menu with menubutton
        self.mb['menu'] = self.menu
        self.mb.grid(row=0, column=0, sticky=W)

        # Title
        self.Indlabel = ttk.Label(self.root, text='Profile: ', font=("Helvetica", 30, 'bold'), style='TLabel')
        self.Indlabel.grid(row=0, column=0, padx=10, pady=15, sticky=SE)

        # name box thing
        self.nameFrame = Frame(self.root, height=140, width=354, padx=30, pady=15, background="white")
        self.nameFrame.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        self.load = Image.open("/Users/22NitaC/PycharmProjects/pawnshop/Images/profile.png")
        self.resized_image = self.load.resize((80, 80), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.resized_image)
        self.imgpfp = Label(self.nameFrame, image=self.render)
        self.imgpfp.image = self.render
        self.imgpfp.grid(row=0, column=0, rowspan=3, ipadx=20, ipady=20, padx=20, sticky=NW)

        self.name = ttk.Label(self.nameFrame, text=self.firstn + " " + self.lastn, font=('Helvetica', 18))
        self.name.grid(row=0, column=1, sticky=SW)
        self.usernametitle = ttk.Label(self.nameFrame, text="Username: " + self.usern, font=('Helvetica', 13))
        self.usernametitle.grid(row=1, column=1, sticky=W)
        self.emailtitle = ttk.Label(self.nameFrame, text="Email: " + self.email, font=('Helvetica', 13))
        self.emailtitle.grid(row=2, column=1, sticky=NW)

        self.root.mainloop()

    def profileInformation(self):
        self.sql = "SELECT username, firstname, lastname, email FROM tbl_user_profile WHERE username = '" + self.username+"'"
        print(self.sql)
        # count(*)= check through all rows
        self.conn = db_conn.mysqlconnect()
        self.cur = self.conn.cursor()
        self.cur.execute(self.sql)  # execute sql query
        self.result = self.cur.fetchall()

        self.record = []
        for row in self.result:
            self.record.append(row)
        print(self.record)
        return self.record

    def gotobookmark(self):
        self.root.withdraw()
        import bookmarks as bookmarks
        self.bookmarks = bookmarks.bookmark(self.root, self.username)

    def gotoindustries(self):
        self.root.withdraw()
        import IndustriesScreen as industriesscreen
        self.industriesscreen = industriesscreen.industry(self.root, self.username)

    def gotogeneralstocks(self, industry):
        self.root.withdraw()
        import GeneralstocksScreen2 as genstocks2
        self.genstocks2 = genstocks2.GeneralScreen(self.root, industry, self.username)

    def gotologin(self):
        self.root.withdraw()
        import login2 as login
        self.login = login.Login

    def gotoprofile(self):
        import profilePage as profilepage
        self.profilepage = profilepage.profile(self.root, self.username)