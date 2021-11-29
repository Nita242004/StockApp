from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from PIL import ImageTk, Image
from ttkbootstrap import Style
import tkinter as tk
from tkinter import ttk
import db_conn
import SpecificStock

def stockInfo(industry):
    sql = "SELECT stock_symbol, stock_name, industry_name FROM tbl_stock WHERE industry_name='" + industry + "'"
    # count(*)= check through all rows
    conn = db_conn.mysqlconnect()
    cur = conn.cursor()
    cur.execute(sql)  # execute sql query
    result = cur.fetchall()

    record = []
    for row in result:
        record.append(row)
    return record

class GeneralScreen:
    def __init__(self, root1, industryname, username):
        print(username)
        self.username = username
        #create a window on top of all other windows
        self.style = Toplevel(root1)
        #applying parameters of style from industries screen to keep the same theme for new window
        self.root = self.style
        # root = Tk() --> cam remove since root = style.master already does this
        self.root.title("Industries")
        self.root.geometry("1000x600")
        self.industryname = industryname

    # menu section:
        # menu
        self.mb = ttk.Menubutton(self.root, style='primary.TMenubutton')
        # create menu
        self.menu = tk.Menu(self.mb)
        # add options
        self.option_var = tk.StringVar()
        self.menu.add_radiobutton(label="Industries", value=0, variable=self.option_var, command=self.gotoindustries)
        self.menu.add_radiobutton(label="General Stocks", value=1, variable=self.option_var,
                                  command=self.gotogeneralstocks)
        self.menu.add_radiobutton(label="Bookmarks", value=2, variable=self.option_var, command=self.gotobookmark)
        self.menu.add_radiobutton(label="Profile", value=4, variable=self.option_var, command=self.gotoprofile)
        self.menu.add_radiobutton(label="Logout", value=5, variable=self.option_var, command=self.gotologin)
        # associate menu with menubutton
        self.mb['menu'] = self.menu
        self.mb.grid(row=0, column=0, sticky=W)

    # Title
        self.StockTitle = ttk.Label(self.root, text=self.industryname, font=("Helvetica", 30, 'bold'), style='primary.TLabel')
        self.StockTitle.grid(row=0, column=0, padx=30, pady=15)

    # search bar
        self.entry_search = ttk.Entry(self.root, style='info.TEntry', width=45, font=("Helvetica", 18, 'bold'))
        self.entry_search.grid(row=0, column=2, columnspan=2, sticky=W)
        # search button
        self.btn_search = ttk.Button(self.root, text='Search', style='info.TButton', command = lambda:self.search(self.entry_search.get()))
        self.btn_search.grid(row=0, column=4, padx=10, sticky=W, ipadx=20)

    #bookmark button
        # bookmark img
        self.load = Image.open("Images/bookmark.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self.root, image=self.render)
        self.img.image = self.render
        # self.img.grid(row=0, column=1)
        self.bookmarkbut = Button(self.root, text="", image=self.img.image, compound=LEFT,
                                  command=lambda: self.gotobookmark(username))
        self.bookmarkbut.grid(row=0, column=1)

    # Stocks
        # Using treeview widget
        self.treev = ttk.Treeview(self.root, selectmode='browse', height=22)
        self.treev.grid(row=1, column=0, padx=30, rowspan=10, columnspan=6, sticky='w')

        # Constructing vertical scrollbar
        # with treeview
        self.verscrlbar = ttk.Scrollbar(self.root,
                                   orient="vertical",
                                   command=self.treev.yview)

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

        self.stockList = []
        self.stockList = stockInfo(self.industryname)

        counter = 1
        for i in range(len(self.stockList)):
            self.treev.insert("", index=i, text=self.stockList[i][0] , values=(counter, self.stockList[i][0], self.stockList[i][1]))
            counter = counter + 1

        self.treev.bind('<ButtonRelease-1>', self.item_selected)

        self.root.mainloop()

    def item_selected(self, event):
        symbol=self.treev.selection()[0]
        item = self.treev.item(symbol)['text']
        # self.root.destroy()
        #goes to spec stock screen + sends specific parameters
        SpecifcStockScreen = SpecificStock.SpecificStock(self.root, self.industryname, item, self.username)

    def search(self, search):
        sql = "SELECT stock_symbol, stock_name, industry_name FROM tbl_stock WHERE stock_name like '%" + search + "%' or stock_symbol like '%" + search +"%'"
        # count(*)= check through all rows
        conn = db_conn.mysqlconnect()
        cur = conn.cursor()
        cur.execute(sql)  # execute sql query
        result = cur.fetchall()

        record = []
        for row in result:
            record.append(row)

        #destroys old treeview
        self.treev.destroy()
        # Using treeview widget
        self.treev = ttk.Treeview(self.root, selectmode='browse', height=22)
        self.treev.grid(row=1, column=0, padx=30, rowspan=10, columnspan=6, sticky='w')

        # Constructing vertical scrollbar
        # with treeview
        self.verscrlbar = ttk.Scrollbar(self.root,
                                        orient="vertical",
                                        command=self.treev.yview)

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

        #new list
        self.stockList = record
        counter = 1
        for i in range(len(self.stockList)):
            self.treev.insert("", index=i, text=self.stockList[i][0], values=(counter, self.stockList[i][0], self.stockList[i][1]))
            counter = counter + 1

        self.treev.bind('<ButtonRelease-1>', self.item_selected)

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











