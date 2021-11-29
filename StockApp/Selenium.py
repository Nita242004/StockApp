from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

class selenium:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="/Users/22NitaC/PycharmProjects/CompsciIA/chromedriver 2")
        # symbol =
        #self.url2 = "https://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol=ADVANC&ssoPageId=12&selectPage=3"


    def compinfo(self,symbol):
        self.url = "https://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol="+symbol+"&ssoPageId=12&selectPage=3"
        self.driver.get(self.url)
        time.sleep(10)
        self.elem2 = self.driver.find_element_by_class_name('col-xs-12')
        self.stock_info = str(self.elem2.text).split('\n')
        # print(self.stock_info)

        self.companyinfo = []
        self.keywords = ['เว็บไซต์บริษัท:', 'ที่อยู่:', 'โทร:', 'หมวดธุรกิจ:', 'กลุ่มอุตสาหกรรม:', 'วันที่เริ่มต้นซื้อขาย:', 'ข้อจำกัดการถือหุ้นต่างด้าว:', 'ราคาพาร์:']
        self.address_index=[]
        for i in range(len(self.keywords)):
            self.address_index.append(self.stock_info.index(self.keywords[i]))
        # print(self.address_index)

        for i in range(0, 8):
            self.companyinfo.append(self.stock_info[self.address_index[i] + 1])
            print(str(self.address_index[i]) + str(self.stock_info[self.address_index[i] + 1]))
        # print(self.companyinfo)
        return self.companyinfo
        self.driver.close()

    def finstate(self, symbol):
        self.url = "https://www.settrade.com/settrade/stock-quote/financialstatement?symbol="+symbol
        self.driver.get(self.url)
        time.sleep(10)
        # self.fininfo = []
        self.keywords = ["สินทรัพย์รวม", "หนี้สินรวม", "ส่วนของผู้ถือหุ้น", "มูลค่าหุ้นที่เรียกชำระแล้ว", "รายได้รวม", "กำไรสุทธิ",
                         "กำไรต่อหุ้น (บาท)", "ROA(%)", "ROE(%)", "อัตรากำไรสุทธิ(%)", "", "ราคาล่าสุด(บาท)",
                         "มูลค่าหลักทรัพย์ตามราคาตลาด", "P/E (เท่า)", "P/BV (เท่า)", "มูลค่าหุ้นทางบัญชีต่อหุ้น (บาท)",
                         "อัตราส่วนเงินปันผลตอบแทน(%)"]

        self.elem = self.driver.find_element_by_css_selector('table')
        self.elem_text = self.elem.get_attribute('innerHTML')

        # print(self.elem.text)

        self.a=str(self.elem.text)
        self.a = self.a.replace("\nบัญชีทางการเงินที่สำคัญ  ", "")
        self.a = self.a.replace("\nอัตราส่วนทางการเงินที่สำคัญ  ", "")
        self.a = self.a.replace("ค่าสถิติสำคัญ\nณ วันที่ 29/12/2560 28/12/2561 30/12/2562 30/12/2563 19/11/2564", "")
        self.a = self.a.replace("\nวันที่ของงบการเงินที่ใช้คำนวณค่าสถิติ 30/09/2560   30/09/2561   30/09/2562   30/09/2563   30/09/2564  ", "")
        self.b=self.a.split('\n')

        # print("++++++++++")
        # print(self.b)

        # 9 - 15, 17 - 19, 22 - 23, 25 - 28
        counter=8
        counterkeyword=0
        self.arr=[]
        while counterkeyword < len(self.keywords):
            # print(counterkeyword)
            # print(counter)
            # print(self.b[counter])
            # print(self.keywords[counterkeyword])
            self.temp = self.b[counter].replace(self.keywords[counterkeyword], "")
            # print(self.temp)
            self.temp=self.temp.split(" ")
            self.arr.append(self.temp)
            # print(self.arr)
            counterkeyword = counterkeyword+1
            counter = counter + 1
            # print("=================")
        # print(self.arr)

    #removing null variables
        #removing null values within the variables
        self.b = [[i for i in item if i != ''] for item in self.arr]
        #removing null values in the list
        self.c = [item for item in self.b if item != []]
        # print(b)
        # print(c)
        return self.c

        self.driver.close()



# A = selenium()
# A.finstate("ADVANC")

# counter=9
#         counterkeyword=0
#         self.arr=[]
#         for i in range(len(self.keywords)):
#             if counter != 16 and counter != 20 and counter != 21 and counter != 24 and counter != 25:
#                 print(self.b[counter])
#                 print(self.keywords[i])
#                 self.temp = self.b[counter].replace(self.keywords[i], "")
#                 print(self.temp)
#                 # self.temp=self.temp.split(" ")
#                 # self.temp=self.temp.remove("")
#
#                 self.arr.append(self.temp)
#             counter=counter+1
#             counterkeyword=counterkeyword+1
#             print("=================")
#         print(self.arr)
#         return self.arr

# def simple_get(url):
#     """
#     Attempts to get the content at `url` by making an HTTP GET request.
#     If the content-type of response is some kind of HTML/XML, return the
#     text content, otherwise return None.
#     """
#     try:
#         with closing(get(url, stream=True, verify=False)) as resp:
#             if is_good_response(resp):
#                 return resp.content
#             else:
#                 return None
#
#     except RequestException as e:
#         log_error('Error during requests to {0} : {1}'.format(url, str(e)))
#         return None
#
#
# def is_good_response(resp):
#     """
#     Returns True if the response seems to be HTML, False otherwise.
#     """
#     content_type = resp.headers['Content-Type'].lower()
#     return (resp.status_code == 200
#             and content_type is not None
#             and content_type.find('html') > -1)
#
#
# def log_error(e):
#     """
#     It is always a good idea to log errors.
#     This function just prints them, but you can
#     make it do anything.
#     """
#     print(e)
#
# driver = webdriver.Chrome(executable_path="/Users/22NitaC/PycharmProjects/CompsciIA/chromedriver 2")
#
# symbol = 'ADVANC'
# url = "https://www.settrade.com/C04_03_stock_companyhighlight_p1.jsp?txtSymbol=ADVANC&ssoPageId=12&selectPage=3"
# driver.get(url)
#
# row = driver.find_elements_by_tag_name("div")
# counter = 0
# info = []
# for r in row:
#     if counter == 46:
#         info=r.text.split("\n")
#         break
#     counter = counter + 1
#
# print(info[18], info[20], info[22], info[32],info[34], info[36], info[40], info[48])
#
# class scrape2:
#     def __init__(self):
#         self.link = 'https://www.settrade.com/settrade/stock-quote/financialstatement?symbol=EE'
#         self.raw_html = simple_get(self.link)
#         self.html = BeautifulSoup(self.raw_html, 'html.parser')
#         # print(html.text)
#
#     def getTextinTbl2(self):
#         self.data_dict = dict()
#         self.table = self.html.find_all("div", attrs={'class':"table table-hover table-info"})
#         print(self.table)
#         # finds the specific class and area
#         self.all_tr = self.table[0].find_all('font')
#         print(self.all_tr)
#         # gets the information from specific table of choice (tr = row, td = column)
#         self.count = 0
#         for tr in self.all_tr:
#             self.count = self.count + 1
#             self.trim_text = ""
#             self.all_td = tr.find_all('td')
#
#             self.key = ""
#             self.value = ""
#             self.i = 0
#             for td in self.all_td:
#                 # gets specific row
#                 self.text = td.text
#                 # collects only the text
#                 self.text = self.text.strip()
#                 # strips spaces
#                 if self.i == 0:
#                     self.key = self.text
#                 else:
#                     self.value = self.text
#
#                 self.i = self.i + 1
#
#             self.data_dict[self.key] = self.value
#         # return data_dict
#         print(self.data_dict)
#
#
#
#
