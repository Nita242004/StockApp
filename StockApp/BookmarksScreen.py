import tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from ttkbootstrap import Style
from functools import partial
import db_conn
import db_config
import datetime
from datetime import *
import SpecificStock

class bookmarks:
    def __init__(self, username):
        print('bookmark')
        print(username)
        self.style = Style()
        self.root = self.style.master
        self.style.configure('info.TButton',font=("Helvetica", 12))
        self.style.configure('TNotebook.Tab', tabposition='n', font=('Helvetica', 16))

        self.root.title("Bookmarks")
        self.root.geometry("1000x750")

    # menu section:
        # menu
        self.mb = ttk.Menubutton(self.root, style='primary.TMenubutton')
        # create menu
        self.menu = tk.Menu(self.mb)
        # add options
        self.option_var = tk.StringVar()
        self.menu.add_radiobutton(label="Industries", value=0, variable=self.option_var, command=self.gotoindutries)
        self.menu.add_radiobutton(label="Bookmarks", value=1, variable=self.option_var, command=self.gotobookmark)
        self.menu.add_radiobutton(label="Profile", value=2, variable=self.option_var, command=self.gotoprofile)
        self.menu.add_radiobutton(label="Logout", value=3, variable=self.option_var, command=self.gotologin)
        # associate menu with menubutton
        self.mb['menu'] = self.menu
        self.mb.grid(row=0, column=0, sticky=W)

        #Title
        self.Title = ttk.Label(self.root, text="Bookmarks", font=("Helvetica", 30,'bold'), style='TLabel')
        self.Title.grid(row=0, column=0,padx=30, pady=10, sticky=E)

    # search bar
        self.entry_search = ttk.Entry(self.root, style='info.TEntry', width=45, font=("Helvetica", 18, 'bold'))
        self.entry_search.grid(row=0, column=2, columnspan=2, sticky=W)
        # search button
        self.btn_search = ttk.Button(self.root, text='Search', style='info.TButton',command=lambda: self.search(self.entry_search.get()))
        self.btn_search.grid(row=0, column=4, padx=10, sticky=W, ipadx=20)

        self.dateLabel = ttk.Label(self.root, text="Date/Time:   "+str(datetime.date(datetime.now())) + "   " + str(datetime.now().strftime("%X")),style='secondary.TLabel', font=("Helvetica", 14))
        self.dateLabel.grid(row=1, column=0,columnspan = 3, padx=30,sticky=W,ipadx=20)
        self.btn_deleteall = ttk.Button(self.root, text='Delete All', style='info.TButton')
        self.btn_deleteall.grid(row=1, column=3,sticky=E,ipadx=20)
        self.btn_delete = ttk.Button(self.root, text='Delete', style='info.TButton')
        self.btn_delete.grid(row=1, column=4,padx=10,sticky=W,ipadx=20)

        #bookmarks frame + scroll bar
        self.bookmarkframe1=ttk.Frame(self.root, height=970, width=550)
        self.bookmarkframe1['padding'] = (5,10,5,10)
        self.bookmarkframe1.grid(row=2, column=0, columnspan=6, sticky=NSEW)


        self.treev = ttk.Treeview(self.bookmarkframe1, selectmode='browse', height = 25)
        self.treev.grid(row=0, column=0, padx=25, pady=10, rowspan= 5, columnspan=6, sticky='w')
        ##scrollbar
        self.verscrlbar = ttk.Scrollbar(self.root,
                                   orient="vertical",
                                   command=self.treev.yview)
        self.treev["columns"] = ("1", "2", "3", "4", "5", "6","7","8","9")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=60, anchor='c')
        self.treev.heading("1", text="Index")
        self.treev.column("2", width=110, anchor='c')
        self.treev.heading("2", text="Industry")
        self.treev.column("3", width=109, anchor='c')
        self.treev.heading("3", text="Symbol")
        self.treev.column("4", width=110, anchor='c')
        self.treev.heading("4", text="Available Volume")
        self.treev.column("5", width=110, anchor='c')
        self.treev.heading("5", text="Market Price")
        self.treev.column("6", width=110, anchor='c')
        self.treev.heading("6", text="High")
        self.treev.column("7", width=110, anchor='c')
        self.treev.heading("7", text="Low")
        self.treev.column("8", width=110, anchor='c')
        self.treev.heading("8", text="Selling")
        self.treev.column("9", width=110, anchor='c')
        self.treev.heading("9", text="Floor")


        self.root.mainloop()

    def item_selected(self, event):
        symbol=self.treev.selection()[0]
        item = self.treev.item(symbol)['text']

    def gotobookmark(self):
        self.root.withdraw()
        import bookmarks as bookmarks
        self.bookmarks = bookmarks.bookmark(self.root, self.username)

    def gotoindutries(self):
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

    def item_selected(self, event):
        symbol=self.treev.selection()[0]
        item = self.treev.item(symbol)['text']
        # self.root.destroy()
        #goes to spec stock screen + sends specific parameters
        import SpecificStock
        SpecifcStockScreen = SpecificStock.SpecificStock(self.root, self.industryname, item, self.username)

    def search(self, search):
        sql = "SELECT stock_symbol, stock_name, industry_name FROM tbl_stock WHERE stock_name like '%" + search + "%' or stock_symbol like '%" + search + "%'"
        # count(*)= check through all rows
        conn = db_conn.mysqlconnect()
        cur = conn.cursor()
        cur.execute(sql)  # execute sql query
        result = cur.fetchall()

        record = []
        for row in result:
            record.append(row)

        # destroys old treeview
        self.treev.destroy()
        # Using treeview widget
        self.treev = ttk.Treeview(self.root, selectmode='browse', height=22)
        self.treev.grid(row=1, column=0, padx=30, rowspan=10, columnspan=6, sticky='w')

        # Constructing vertical scrollbar
        # with treeview
        self.verscrlbar = ttk.Scrollbar(self.root,orient="vertical",command=self.treev.yview)

        # Defining number of columns
        self.treev["columns"] = ("1", "2", "3")

        # Defining heading
        self.treev['show'] = 'headings'

        # Assigning the width and anchor to  the
        # respective columns
        self.treev.column("1", width=30, anchor='c')
        self.treev.column("2", width=300, anchor='c')
        self.treev.column("3", width=600, anchor='w')

        # Assigning the heading names to the
        # respective columns
        self.treev.heading("1", text="")
        self.treev.heading("2", text="Symbol")
        self.treev.heading("3", text="Stock Name")

        # new list
        self.stockList = record
        counter = 1
        for i in range(len(self.stockList)):
            self.treev.insert("", index=i, text=self.stockList[i][0],
                              values=(counter, self.stockList[i][0], self.stockList[i][1]))
            counter = counter + 1

        self.treev.bind('<ButtonRelease-1>', self.item_selected)

A = bookmarks("nita")


        # self.root.destroy()
        # # goes to spec stock screen + sends specific parameters
        # SpecifcStockScreen = SpecificStock.SpecificStock(self.root, item, self.username)



