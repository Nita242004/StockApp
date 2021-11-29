import tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.font as tkFont
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Style
from functools import partial
import db_conn
import db_config
import webbrowser
from Selenium import selenium

import scraping
from googletrans import Translator
#to translate thai to english (display english term)
trans = Translator()

from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def stockInfo(symbol):
    sql = "SELECT stock_name FROM tbl_stock WHERE stock_symbol='" + symbol + "'"
    # count(*)= check through all rows
    conn = db_conn.mysqlconnect()
    cur = conn.cursor()
    cur.execute(sql)  # execute sql query
    result = cur.fetchone()

    record = []
    for row in result:
        record.append(row)
    return record


class SpecificStock:
    def __init__(self, root1, industry, symbol, username):
        print(symbol)
        print(username)
        self.industry = industry
        self.style = Toplevel(root1)
        self.root = self.style

        # self.style.configure('info.TButton', font=("Helvetica", 12))
        # self.style.configure('TNotebook.Tab', tabposition='n', font=('Helvetica', 16))

        self.root.title("Stock")
        self.root.geometry("1000x750")

#menu bar CHANGE GRID AND CONTENT AND ADD FUNCTIONS!!!!!!
    # menu section:
        # menu
        self.mb = ttk.Menubutton(self.root, style='primary.TMenubutton')
        # create menu
        self.menu = tk.Menu(self.mb)
        # add options
        self.option_var = tk.StringVar()
        self.menu.add_radiobutton(label="Industries", value=0, variable=self.option_var, command=self.gotoindustries)
        self.menu.add_radiobutton(label="General Stocks", value=1, variable=self.option_var, command=self.gotogeneralstocks)
        self.menu.add_radiobutton(label="Bookmarks", value=2, variable=self.option_var, command=self.gotobookmark)
        self.menu.add_radiobutton(label="Profile", value=4, variable=self.option_var, command=self.gotoprofile)
        self.menu.add_radiobutton(label="Logout", value=5, variable=self.option_var, command=self.gotologin)
        # associate menu with menubutton
        self.mb['menu'] = self.menu
        self.mb.grid(row=0, column=0, sticky=W)

        #Title
        self.StockTitle = ttk.Label(self.root, text=symbol, font=("Helvetica", 30,'bold'), style='TLabel')
        self.StockTitle.grid(row=0, column=0,padx=30, pady=30)

        # self.load = Image.open("Images/bookmark.png")
        # self.render = ImageTk.PhotoImage(self.load)
        # self.img = Label(self.root,image=self.render)
        # self.img.image = self.render
        # self.img.grid(row=0, column=1, sticky=W)
        self.btn_bookmark = ttk.Button(self.root, text="bookmark", command = lambda:self.addbookmark(username, symbol))
        self.btn_bookmark.grid(row=0, column=1, sticky=W)

        # search bar
        self.entry_search = ttk.Entry(self.root, style='info.TEntry', width=45, font=("Helvetica", 18, 'bold'))
        self.entry_search.grid(row=0, column=2, columnspan=2, sticky=W)
        # search button
        self.btn_search = ttk.Button(self.root, text='Search', style='info.TButton',command=lambda: self.search(self.entry_search.get()))
        self.btn_search.grid(row=0, column=4, padx=10, sticky=W, ipadx=20)


        #Tab
        self.tabControl = ttk.Notebook(self.root, width=930, height=520, style='TNotebook')
        self.tabControl.grid(row=1, column=0,columnspan=5,padx=30)

        #create tabs
        self.summarytab = ttk.Frame(self.root)
        self.profiletab = ttk.Frame(self.root)
        self.shareholderstab = ttk.Frame(self.root)
        self.financialsttab = ttk.Frame(self.root)
        self.financialrattab = ttk.Frame(self.root)
        self.socialmedtab = ttk.Frame(self.root)

        #adding tabs
        self.tabControl.add(self.summarytab, text="Summary")
        self.tabControl.add(self.profiletab, text="Profile")
        self.tabControl.add(self.shareholderstab, text="Shareholder")
        self.tabControl.add(self.financialsttab, text="Financial Statement")
        self.tabControl.add(self.financialrattab, text="Financial Ratio Analysis")
        self.tabControl.add(self.socialmedtab, text="Social Media")


        #social media tab ---------------------------------------
        # Titles
        self.newsTitle = ttk.Label(self.socialmedtab, text='Recent News:', style="TLabel",
                                   font=("Helvetica", 18, 'bold'))
        self.newsTitle.grid(row=0, column=0, columnspan=2, padx=14, pady=20, sticky="W")

        ##recent news tbl
        self.treev = ttk.Treeview(self.socialmedtab, selectmode='browse', height=19)
        self.treev.grid(row=1, column=0, padx=15, rowspan=5, columnspan=2, sticky='nw')

        ##scrollbar
        self.verscrlbar = ttk.Scrollbar(self.socialmedtab, orient="vertical", command=self.treev.yview)

        self.treev["columns"] = ("1", "2", "3")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=60, anchor='c')
        self.treev.column("2", width=200, anchor='c')
        self.treev.column("3", width=270, anchor='w')

        self.treev.heading("1", text="Time")
        self.treev.heading("2", text="Source")
        self.treev.heading("3", text="Headline")

        self.pageScrape = scraping.scrapearticle(symbol)
        self.links = self.pageScrape.getlink()
        self.times = self.pageScrape.gettime()
        self.sources = self.pageScrape.getsource()
        self.titles = self.pageScrape.gettitle()
        for i in (self.links):
            print("links " + i)

        counter = 1
        for i in range(0,6):
            self.treev.insert("", index=i, text=self.links[i],
                              values=(self.times[i], self.sources[i], self.titles[i]))
            counter = counter + 1

        self.treev.bind('<ButtonRelease-1>', self.item_selected)

#SENT ANALYSIS GRAPH
        ###graph
        self.graphframe1 = ttk.Frame(self.socialmedtab, height=970, width=550)
        self.graphframe1['padding'] = (0, 10, 0, 10)
        self.graphframe1.grid(row=1, column=3, columnspan=5)

        # Authentication
        self.consumerKey = "UY6aeEjwyQiaounKfBzLjB7i0"
        self.consumerSecret = "uXbMc3S0y33BF9RGKfV4uNN4Lk617EGiWXxIXhgwV2kno5G8my"
        self.accessToken = "1414996578817875972-QyoWsIKR0f05OBv562j3RmQQ3foqxI"
        self.accessTokenSecret = "K2fKbuNjOo5Pl5KRLDbToj33B3I3jViS3WnC4D0OF1Hre"
        self.auth = tweepy.OAuthHandler(self.consumerKey, self.consumerSecret)
        self.auth.set_access_token(self.accessToken, self.accessTokenSecret)
        self.api = tweepy.API(self.auth)

        # Sentiment Analysis
        self.keyword = symbol
        self.noOfTweet = 100
        self.tweets = tweepy.Cursor(self.api.search, q=self.keyword).items(self.noOfTweet)
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.polarity = 0
        self.tweet_list = []
        self.neutral_list = []
        self.negative_list = []
        self.positive_list = []

        for tweet in self.tweets:
            # print(tweet.text)
            # sorting tweets based on polarity
            self.tweet_list.append(tweet.text)
            self.analysis = TextBlob(tweet.text)
            self.score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
            self.neg = self.score['neg']
            self.neu = self.score['neu']
            self.pos = self.score['pos']
            self.comp = self.score['compound']
            self.polarity += self.analysis.sentiment.polarity

            if self.neg > self.pos:
                self.negative_list.append(tweet.text)
                self.negative += 1
            elif self.pos > self.neg:
                self.positive_list.append(tweet.text)
                self.positive += 1

            elif self.pos == self.neg:
                self.neutral_list.append(tweet.text)
                self.neutral += 1

        # Finding percentage
        self.positive = self.percentage(self.positive, self.noOfTweet)
        self.negative = self.percentage(self.negative, self.noOfTweet)
        self.neutral = self.percentage(self.neutral, self.noOfTweet)
        self.polarity = self.percentage(self.polarity, self.noOfTweet)
        self.positive = format(self.positive, '.1f')
        self.negative = format(self.negative, '.1f')
        self.neutral = format(self.neutral, '.1f')

        # Number of Tweets (Total, Positive, Negative, Neutral)
        self.tweet_list = pd.DataFrame(self.tweet_list)
        self.neutral_list = pd.DataFrame(self.neutral_list)
        self.negative_list = pd.DataFrame(self.negative_list)
        self.positive_list = pd.DataFrame(self.positive_list)
        print("total number: ", len(self.tweet_list))
        print("positive number: ", len(self.positive_list))
        print("negative number: ", len(self.negative_list))
        print("neutral number: ", len(self.neutral_list))

        # Bar chart
        # Bringing raw data.
        self.frequencies = [len(self.positive_list), len(self.negative_list), len(self.neutral_list)]
        self.freq_series = pd.Series(self.frequencies)

        self.x_labels = ['Positive', 'Negative', 'Neutral']
    #creating graph
        self.figure = plt.figure(figsize=(3, 4))
        # self.ax1 = self.figure.add_subplot()
        self.line1 = FigureCanvasTkAgg(self.figure, self.graphframe1)
        self.line1.get_tk_widget().grid(row=0, column=0, sticky = NSEW)

        self.ax = self.freq_series.plot(kind="bar")
        self.ax.set_title("Sentiment Analysis Result for keyword " + self.keyword + "")
        self.ax.set_xlabel("Polarity")
        self.ax.set_ylabel("Number of Tweets")
        self.ax.set_xticklabels(self.x_labels, rotation=0, ha='center')

        self.rects = self.ax.patches

        # Make some labels.
        self.labels = self.frequencies
        # placement for labels
        for rect, label in zip(self.rects, self.labels):
            print(label)
            self.height = rect.get_height()
            self.ax.text(rect.get_x() + rect.get_width() / 2, self.height, label, ha="center", va="bottom")

        # plt.show()


    # financial ratio analysis TAB ---------------------------------------
        self.fin_labelframe = ttk.Label(self.financialrattab, text=symbol +": "+ str(stockInfo(symbol)[0]),
                                        style="success.TLabel", font=("Helvetica", 18, 'bold'))
        self.fin_labelframe.grid(row=0, column=0, columnspan=2, padx=14, pady=20, sticky="W")

        self.ratframe1 = ttk.Frame(self.financialrattab, height=970, width=550)
        self.ratframe1['padding'] = (5, 10, 5, 10)
        self.ratframe1.grid(row=1, column=0, columnspan=10, sticky=NW)

        # self.rat_label = ttk.Label(self.ratframe1, text='Score (0-2): ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=2, column=2, padx=10, sticky=W)

        # pageScrape = scraping.scrape2(symbol)
        # data_dict = pageScrape.getTextinTbl2()
        # print(data_dict.get(''))

        # self.ratioinfo('Earnings Per Share (EPS): ',stat, score, 3)
        # self.ratioinfo('Price to Earning (PE): ', 5)
        # self.ratioinfo('Price to Break (PBV): ', 7)
        # self.ratioinfo('Debt to Equity (DE): ', 9)
        # self.ratioinfo('Return on Equity (ROE): ', 11)
        # self.ratioinfo('Price to Sales (P/S): ', 13)
        # self.ratioinfo('Current Ratio: ', 15)
        # self.ratioinfo('Dividend Yield: ', 15)

        # self.rat_label = ttk.Label(self.ratframe1, text='Total Score: ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=19, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=19, column=2, padx=20, sticky=E)

        # self.space = ttk.Label(self.ratframe1, text="")
        # self.space.grid(row=3, column=4, columnspan=4, rowspan=10)

        # self.rat_label = ttk.Label(self.ratframe1, text='Meter: ', style="secondary.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=2, column=8)
        #
        # self.score = 12
        # if self.score >= 50:
        #     self.style = 'warning.Vertical.TProgressbar'
        # elif self.score >= 70:
        #     self.style = 'success.Vertical.TProgressbar'
        # elif self.score < 50:
        #     self.style = 'danger.Vertical.TProgressbar'

        # self.meter = ttk.Progressbar(self.ratframe1, value=self.score, orient='vertical', style=self.style, length=300)
        # self.meter.grid(row=3, column=8, rowspan=18, padx=100, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='100%', style="secondary.TLabel", font=("Helvetica", 10))
        # self.rat_label.grid(row=3, column=9, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='0%', style="secondary.TLabel", font=("Helvetica", 10))
        # self.rat_label.grid(row=20, column=9, sticky=W)

        self.s = selenium()
        self.finstate = self.s.finstate(symbol)
        self.fin_col_title = ["Return on assets (ROA)(%):", "Price to Sales (ROE)(%):", "Net Profit Margin(%):", "Last Price(Baht):", "Market Cap:",
                                   "F/S Period (As of date):", "Price to Earning (P/E):", "Price to Break (P/BV):", "Book Value per share (Baht):", "Dividend Yield(%):"]

        ##financial stm table
        self.treev1 = ttk.Treeview(self.ratframe1, selectmode='browse', height=7)
        self.treev1.grid(row=2, column=0, padx=15, rowspan=10, columnspan=6, sticky='w')

        self.treev1["columns"] = ("1", "2", "3", "4", "5", "6")
        self.treev1['show'] = 'headings'
        self.treev1.column("1", width=200, anchor='w')
        self.treev1.column("2", width=130, anchor='c')
        self.treev1.column("3", width=130, anchor='c')
        self.treev1.column("4", width=130, anchor='c')
        self.treev1.column("5", width=130, anchor='c')
        self.treev1.column("6", width=130, anchor='c')

        self.treev1.heading("1", text="")
        self.treev1.heading("2", text="2017")
        self.treev1.heading("3", text="2018")
        self.treev1.heading("4", text="2019")
        self.treev1.heading("5", text="2020")
        self.treev1.heading("6", text="2021")

        for i in range(6,16):
            self.treev1.insert("", index=i-5, iid=i-5, text="", values=(self.fin_col_title[i-6], self.finstate[i][0], self.finstate[i][1], self.finstate[i][2], self.finstate[i][3], self.finstate[i][4]))

        # self.rat_label = ttk.Label(self.ratframe1, text='Earnings Per Share (EPS): ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=3, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=3, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=3, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=4, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Price to Earning (PE): ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=5, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=5, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=5, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=6, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Price to Break (PBV): ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=7, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=7, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=7, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=8, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Debt to Equity (DE): ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=9, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=9, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=9, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=10, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Return on Equity (ROE): ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=11, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=11, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=11, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=12, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Price to Sales (P/S): ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=13, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=13, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=13, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=14, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Current Ratio: ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=15, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=15, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=15, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=16, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Dividend Yield: ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=17, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="success.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=17, column=1, padx=20, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=17, column=2, padx=20, sticky=E)
        # self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        # self.separator.grid(sticky=EW, row=18, columnspan=4, padx=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Total Score: ', style="secondary.TLabel",
        #                            font=("Helvetica", 14))
        # self.rat_label.grid(row=19, column=0, padx=10, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='---', style="info.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=19, column=2, padx=20, sticky=E)
        #
        # self.space = ttk.Label(self.ratframe1, text="")
        # self.space.grid(row=3, column=4, columnspan=4, rowspan=10)
        #
        # self.rat_label = ttk.Label(self.ratframe1, text='Meter: ', style="secondary.TLabel", font=("Helvetica", 14))
        # self.rat_label.grid(row=2, column=8)

        # self.score = 12
        # if self.score >= 50:
        #     self.style = 'warning.Vertical.TProgressbar'
        # elif self.score >= 70:
        #     self.style = 'success.Vertical.TProgressbar'
        # elif self.score < 50:
        #     self.style = 'danger.Vertical.TProgressbar'
        #
        # self.meter = ttk.Progressbar(self.ratframe1, value = self.score, orient='vertical', style = self.style, length=300)
        # self.meter.grid(row=3, column=8, rowspan=18, padx=100, sticky=E)
        # self.rat_label = ttk.Label(self.ratframe1, text='100%', style="secondary.TLabel", font=("Helvetica", 10))
        # self.rat_label.grid(row=3, column=9, sticky=W)
        # self.rat_label = ttk.Label(self.ratframe1, text='0%', style="secondary.TLabel", font=("Helvetica", 10))
        # self.rat_label.grid(row=20, column=9, sticky=W)
        #
        #
        #financial statement TAB ---------------------------------------
        self.fin_labelframe = ttk.Label(self.financialsttab, text=symbol +": "+ str(stockInfo(symbol)[0]),style="success.TLabel",font=("Helvetica", 18,'bold'))
        self.fin_labelframe.grid(row=0,column=0,columnspan=2,padx=14, pady=20, sticky="W")

        ##financial stm table
        self.treev = ttk.Treeview(self.financialsttab, selectmode='browse', height = 7)
        self.treev.grid(row=2, column=0, padx=15, rowspan= 10, columnspan=6, sticky='w')

        self.treev["columns"] = ("1", "2", "3", "4", "5", "6")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=200, anchor='w')
        self.treev.column("2", width=130, anchor='c')
        self.treev.column("3", width=130, anchor='c')
        self.treev.column("4", width=130, anchor='c')
        self.treev.column("5", width=130, anchor='c')
        self.treev.column("6", width=130, anchor='c')

        self.treev.heading("1", text="")
        self.treev.heading("2", text="2017")
        self.treev.heading("3", text="2018")
        self.treev.heading("4", text="2019")
        self.treev.heading("5", text="2020")
        self.treev.heading("6", text="2021")

        # pageScrape = scraping.scrape(symbol)
        # data_dict = pageScrape.getTextinTbl2()
        # print(data_dict.get(''))

        print(self.finstate)
        self.finstate_col_title = ["Total Assets:", "Total Liabilities:", "Equity:", "Paid-up Capital:", "Revenue:", "Net Profit:"]

        for i in range(0,5):
            self.treev.insert("", index=i, iid=i, text="", values=(self.finstate_col_title[i], self.finstate[i][0], self.finstate[i][1], self.finstate[i][2], self.finstate[i][3], self.finstate[i][4]))


        # stakeholdersTAB ---------------------------------------
        self.share_labelframe = ttk.Label(self.shareholderstab, text= symbol +": "+ str(stockInfo(symbol)[0]),style="success.TLabel",font=("Helvetica", 18,'bold'))
        self.share_labelframe.grid(row=0,column=0,columnspan=2,padx=14, pady=20, sticky="W")

        self.pageScrape = scraping.scrape(symbol, '05_stock_majorshareholder')
        self.shareholder = self.pageScrape.getshareholders('table table-info')
        print("=====================")
        print(self.shareholder)
        self.totalno = self.pageScrape.gettotalshareholders()

        self.share_label = ttk.Label(self.shareholderstab, text='Total Shareholders: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.share_label.grid(row=1,column=0,padx=15,sticky=W)
        self.share_label = ttk.Label(self.shareholderstab, text= self.totalno, style="success.TLabel",font=("Helvetica", 14))
        self.share_label.grid(row=1,column=1,padx=12,sticky=W)

        ##shareholder tbl
        self.treev = ttk.Treeview(self.shareholderstab, selectmode='browse', height = 18)
        self.treev.grid(row=3, column=0, padx=15, pady=10, rowspan= 10, columnspan=6, sticky='w')

        ##scrollbar
        self.verscrlbar = ttk.Scrollbar(self.shareholderstab, orient="vertical", command=self.treev.yview)

        self.treev["columns"] = ("1", "2", "3")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=420, anchor='w')
        self.treev.column("2", width=320, anchor='c')
        self.treev.column("3", width=100, anchor='c')

        self.treev.heading("1", text="Major Shareholders")
        self.treev.heading("2", text="Number of Shares")
        self.treev.heading("3", text="Shares (%)")

        print(self.shareholder[i][0])

        #fill the tree view rows with the scraped data (by looping)
        for i in range(1, int(len(self.shareholder))-1):
            #trans = translates the thai to english
            self.stakeinfo(trans.translate(self.shareholder[i][0]), self.shareholder[i][1], self.shareholder[i][2], i+1, i)



        #profileTAB ---------------------------------------
        self.prof_labelframe = ttk.Label(self.profiletab, text=symbol +": "+ str(stockInfo(symbol)[0]),style="success.TLabel",font=("Helvetica", 18,'bold'))
        self.prof_labelframe.grid(row=0,column=0, padx=13,pady=20)

        self.profframe1=ttk.Frame(self.profiletab, height=970, width=550)
        self.profframe1['padding'] = (5,10,5,10)
        self.profframe1.grid(row=1, column=0, columnspan=10,sticky=NW)

        self.s = selenium()
        self.profinfo = self.s.compinfo(symbol)
        print(self.profinfo)

        self.prof_label = ttk.Label(self.profframe1, text='Website: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=1,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=self.profinfo[0],style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=1,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=2, columnspan = 2, padx=10, pady=10)

        self.prof_label = ttk.Label(self.profframe1, text='Address: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=3,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=trans.translate(self.profinfo[1]),style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=3,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=4, columnspan = 2, padx=10, pady=10)

        self.prof_label = ttk.Label(self.profframe1, text='Telephone: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=5,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=self.profinfo[2],style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=5,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=6, columnspan = 6, padx=10, pady=10)

        self.prof_label = ttk.Label(self.profframe1, text='Sector: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=7,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=trans.translate(self.profinfo[3]),style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=7,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=8, columnspan = 6, padx=10, pady=10)

        self.prof_label = ttk.Label(self.profframe1, text='Industry: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=9,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=trans.translate(self.profinfo[4]),style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=9,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=10, columnspan = 6, padx=10, pady=10)

        self.prof_label = ttk.Label(self.profframe1, text='Establish Date: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=11,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=trans.translate(self.profinfo[5]),style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=11,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=12, columnspan = 6, padx=10, pady=10)

        self.prof_label = ttk.Label(self.profframe1, text='Foreign Available: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=13,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=trans.translate(self.profinfo[6]),style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=13,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=14, columnspan = 6, padx=10, pady=10)

        self.prof_label = ttk.Label(self.profframe1, text='Par Value: ',style="secondary.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=15,column=0,padx=10,sticky=W)
        self.prof_label = ttk.Label(self.profframe1, text=trans.translate(self.profinfo[7]),style="success.TLabel",font=("Helvetica", 14))
        self.prof_label.grid(row=15,column=1,padx=12,sticky=E)
        self.separator = ttk.Separator(self.profframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky = EW, row=16, columnspan = 6, padx=10, pady=10)


        #summaryTAB ---------------------------------------

        # self.summary_labelframe = ttk.Label(self.summarytab, text=symbol,
        #                                     style="success.TLabel", font=("Helvetica", 18, 'bold'))
        # self.summary_labelframe.grid(row=1, column=0, padx=13, pady=20)

        self.sumframe1 = ttk.Frame(self.summarytab, height=970, width=690)
        self.sumframe1['padding'] = (30, 1, 1, 1)
        self.sumframe1.grid(row=2, column=0, columnspan=24, sticky=NW)

        self.labelframe = ttk.Label(self.summarytab, text= symbol +": "+ str(stockInfo(symbol)[0]),
                                            style="primary.TLabel", font=("Helvetica", 30, 'bold'))
        self.labelframe.grid(row=0, column=0, columnspan=2, sticky=NW, padx=13, pady=20)

        self.pageScrape = scraping.scrape(symbol, '01_stock_quote')
        self.data_dict = self.pageScrape.getchangerate()
        data_dict2 = self.pageScrape.getTextinTbl('table table-info', 0)
        data_dict3 = self.pageScrape.getTextinTbl('table table-info', 1)
        data_dict4 = self.pageScrape.getTextinTbl('table table-info', 2)
        # print("Dictionary 1 " + str(data_dict3))
        # print(data_dict3.get('ปริมาณซื้อขาย (หุ้น)'))



        self.summaryinfo(self.sumframe1, 'Last Trade: ', self.data_dict.get(1), 1, 0, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Change: ', self.data_dict.get(2), 3, 0, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, '%Change: ', self.data_dict.get(3), 5, 0, 'primary.Horizontal.TSeparator')

        # self.sumframe = ttk.Frame(self.summarytab, height=970, width=550)
        # self.sumframe['padding'] = (5, 10, 5, 10)
        # self.sumframe.grid(row=2, column=2, columnspan=20)

        self.summaryinfo(self.sumframe1, 'Prior: ', data_dict2.get('ราคาปิดก่อนหน้า'), 1, 2,'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Open: ', data_dict2.get('ราคาเปิด'), 3, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'High: ', data_dict2.get('ราคาสูงสุด'), 5, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Low: ', data_dict2.get("ราคาต่ำสุด"), 7, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Average Price: ', data_dict2.get("ราคาเฉลี่ย"),9, 2, 'primary.Horizontal.TSeparator')

        self.space1 = ttk.Label(self.sumframe1, text="")
        self.space1.grid(row=11, column=2, columnspan=2)

        self.summaryinfo(self.sumframe1, 'Volume(Shares): ', (data_dict3.get('ปริมาณซื้อขาย (หุ้น)')), 12, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, "Value('000 Baht): ", (data_dict3.get("มูลค่าซื้อขาย ('000 บาท)")), 14, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Par Value (Baht): ', (data_dict3.get('ราคาพาร์ (บาท)')), 16, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Ceiling: ', (data_dict3.get('ราคา Ceiling')), 18, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Floor: ', (data_dict3.get('ราคา Floor')), 20, 2, 'primary.Horizontal.TSeparator')

        self.space2 = ttk.Label(self.sumframe1, text="")
        self.space2.grid(row=22, column=2, columnspan=2)

        self.summaryinfo(self.sumframe1, 'Bid / Volume Bid: ', data_dict4.get('ราคาเสนอซื้อ / ปริมาณเสนอซื้อ'), 23, 2, 'secondary.Horizontal.TSeparator')
        self.summaryinfo(self.sumframe1, 'Offer / Volume Offer: ', data_dict4.get('ราคาเสนอขาย / ปริมาณเสนอขาย'), 25, 2, 'primary.Horizontal.TSeparator')

        self.root.mainloop()

    def summaryinfo(self, location, label, number, row, column, style):
        self.summary_labelframe = ttk.Label(location, text=label, style="secondary.TLabel", font=("Helvetica", 14))
        self.summary_labelframe.grid(row=row, column=column, padx=10, sticky=W)
        self.summary_labelframe = ttk.Label(location, text=number, style="success.TLabel", font=("Helvetica", 14))
        self.summary_labelframe.grid(row=row, column=column + 1, padx=12, sticky=E)
        self.separator = ttk.Separator(location, orient='horizontal', style=style)
        self.separator.grid(sticky=EW, row=row + 1, column=column, columnspan=2, padx=10)


    def stakeinfo(self, name, quantity, percent, index, id):
        self.treev.insert("", index=index, iid=id, text="", values=(name, quantity, percent))

    def ratioinfo(self, label, stat, score, row):
        self.rat_label = ttk.Label(self.ratframe1, text=label, style="secondary.TLabel",
                                   font=("Helvetica", 14))
        self.rat_label.grid(row=row, column=0, padx=10, sticky=W)
        self.rat_label = ttk.Label(self.ratframe1, text= stat, style="success.TLabel", font=("Helvetica", 14))
        self.rat_label.grid(row=row, column=1, padx=20, sticky=E)
        self.rat_label = ttk.Label(self.ratframe1, text= score, style="info.TLabel", font=("Helvetica", 14))
        self.rat_label.grid(row=row, column=2, padx=20, sticky=E)
        self.separator = ttk.Separator(self.ratframe1, orient='horizontal', style='secondary.Horizontal.TSeparator')
        self.separator.grid(sticky=EW, row=row+1, columnspan=4, padx=10)

    def item_selected(self, event):
        symbol = self.treev.selection()[0]
        print(symbol)
        item = self.treev.item(symbol)['text']
        print(item)

        webbrowser.open_new(item)

    def addbookmark(self, username, symbol):
        conn = db_conn.mysqlconnect()
        cur = conn.cursor()

        sqlcheck = "Select * from tbl_bookmarks where username = '"+ username +"' and stocksymbol = '"+ symbol +"'"
        cur.execute(sqlcheck)  # execute sql query
        result = cur.fetchone()

        if result is not None:
            messagebox.showinfo("result", "Stock Already Added")

        else:
            sql = "INSERT INTO tbl_bookmarks (username, stocksymbol) VALUES (%s, %s)"
            val = (username, symbol)
            print(sql)
            cur.execute(sql, val)

            conn.commit()
            messagebox.showinfo("result", "Stock added")

    def finstateinfo(self, index, text, y1, y2, y3, y4):
        return self.treev.insert("", index=index, iid=index, text="", values=(text, y1, y2, y3, y4))

    def percentage(self, part, whole):
        return 100 * float(part) / float(whole)

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
