from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from googletrans import Translator


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True, verify=False)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


# raw_html = simple_get('https://mail.google.com/mail/u/0/?zx=voke62zf0qv3#search/label%3Aunread')
# html = BeautifulSoup(raw_html, 'html.parser')
# html.find_all("span", class_="bA4")

def mathMen():
    raw_html = simple_get('http://www.fabpedigree.com/james/mathmen.htm')
    html = BeautifulSoup(raw_html, 'html.parser')
    # print(html.text)

    for i, li in enumerate(html.select('li')):
        print(i, li.text)


# mathMen()

class scrapearticle:
    def __init__(self, stockname):
        self.link = 'https://www.google.com/finance/quote/'+stockname+':BKK?sa=X&ved=2ahUKEwi5ur6DsvLyAhV3wTgGHdyDDMwQ_AUoAXoECAEQAw'
        self.raw_html = simple_get(self.link)
        self.html = BeautifulSoup(self.raw_html, 'html.parser')
        # print(html.text)

    def getlink(self):
        links = []
        for div in self.html.findAll('div', attrs={'class': 'z4rs2b'}):
            self.data = (div.find('a')['href'])
            links.append(self.data)
        # print(links)
        return links

    def getsource(self):
        self.text = self.html.find_all("div", class_="sfyJob")
        # finds the specific class and area
        sources_dict = dict()
        for i in range(0, 6):
            self.all_text = self.text[i]
            self.all_text = str(self.all_text).replace("<div class=\"sfyJob\">", " ").strip()
            self.all_text = str(self.all_text).replace("</div>", " ").strip()
            sources_dict[i] = self.all_text

        # print(sources_dict)
        return sources_dict

    def gettime(self):
        # finds the specific class and area
        self.text = self.html.find_all("div", class_="Adak")
        # finds the specific class and area
        time_dict = dict()
        for i in range(0, 6):
            self.all_text = self.text[i]
            self.all_text = str(self.all_text).replace("<div class=\"Adak\">", " ").strip()
            self.all_text = str(self.all_text).replace("</div>", " ").strip()
            time_dict[i] = self.all_text

        #print(time_dict)
        return time_dict

    def gettitle(self):
        self.text = self.html.find_all("div", class_="Yfwt5")
        # print(len(self.text))
        # finds the specific class and area
        title_dict = dict()
        for i in range(0, 6):
            self.all_text = self.text[i]
            self.all_text = str(self.all_text).replace("<div class=\"Yfwt5\">", " ").strip()
            self.all_text = str(self.all_text).replace("</div>", " ").strip()
            title_dict[i] = self.all_text

        # print(title_dict)
        return title_dict

# A = scrapearticle('EE')
# A.gettitle()

class scrape:
    def __init__(self, stockname, tab):
        self.link = 'https://www.settrade.com/C04_'+ tab +'_p1.jsp?txtSymbol=' + stockname + '&ssoPageId=9&selectPage=1'
        self.raw_html = simple_get(self.link)
        self.html = BeautifulSoup(self.raw_html, 'html.parser')
        # print(html.text)

    def getTextinTbl(self, classname, tblindex):
        data_dict=dict()
        self.table = self.html.find_all("table", attrs={'class':classname})
        #finds the specific class and area
        self.all_tr = self.table[tblindex].find_all('tr')
        #gets the information from specific table of choice (tr = row, td = column)
        self.count = 0
        for tr in self.all_tr:
            self.count = self.count + 1
            self.trim_text = ""
            self.all_td = tr.find_all('td')

            self.key = ""
            self.value = ""
            self.i = 0
            for td in self.all_td:
                #gets specific row
                self.text = td.text
                #collects only the text
                self.text = self.text.replace("\r","")
                self.text = self.text.replace("\n", "")
                self.text = self.text.replace("                                           ", "")
                self.text = self.text.strip()
                #strips spaces
                if self.i == 0:
                    self.key = self.text
                else:
                    self.value = self.text

                self.i = self.i + 1

            data_dict[self.key] = self.value
        # print(data_dict)
        return data_dict

    def getchangerate(self):
        self.div = self.html.find_all('h1')
        # finds the specific class and area
        data_dict = dict()
        for i in range(1,4):
            self.all_div = self.div[i]
            self.all_div = str(self.all_div).replace("\n","").strip()
            self.all_div = str(self.all_div).replace("                                    </h1>", "").strip()
            self.all_div = str(self.all_div).replace("<h1>", "").strip()
            self.all_div = str(self.all_div).replace("<h1 class=\"colorGreen\">\r                                        ", "").strip()
            self.all_div = str(self.all_div).replace(" <span aria-hidden=\"true\" class=\"glyphicon glyphicon-triangle-top colorGreen text-18\"></span></h1>", "").strip()
            self.all_div = str(self.all_div).replace(" <span aria-hidden=\"true\" class=\"glyphicon glyphicon-triangle-bottom colorGreen text-18\"></span></h1>","").strip()
            self.all_div = str(self.all_div).replace("<h1 class=\"colorRed\">\r                                        ", "").strip()
            self.all_div = str(self.all_div).replace(" <span aria-hidden=\"true\" class=\"glyphicon glyphicon-triangle-top colorRed text-18\"></span></h1>", "").strip()
            self.all_div = str(self.all_div).replace(" <span aria-hidden=\"true\" class=\"glyphicon glyphicon-triangle-bottom colorRed text-18\"></span></h1>", "").strip()
            self.all_div = str(self.all_div).replace("<h1 class=\"\">\r", "").strip()

            data_dict[i] = self.all_div
        print(data_dict)
        return(data_dict)

# A = scrape("EE", '01_stock_quote')
# A.getchangerate()

    def getshareholders(self, classname):
        shareholders = []
        self.table = self.html.find_all("table", attrs={'class': classname})
        # finds the specific class and area
        self.all_tr = self.table[0].find_all('tr')
        # gets the information from specific table of choice (tr = row, td = column)
        self.count = 0
        for tr in self.all_tr:
            temp = []
            self.count = self.count + 1
            self.trim_text = ""
            self.all_td = tr.find_all('td')

            self.key = ""
            self.value = ""
            for td in self.all_td:
                # gets specific row
                self.text = td.text
                # collects only the text
                self.text = self.text.replace("\r", "")
                self.text = self.text.replace("\n", "")
                self.text = self.text.replace("                                           ", "")
                # strips spaces
                self.text = self.text.strip()

                temp.append(self.text)
            shareholders.append(temp)
        print(shareholders)
        return shareholders

    def gettotalshareholders(self):
        self.total = []
        self.div = self.html.find_all("div", attrs={'class': 'col-xs-12 col-md-6'})
        # finds the specific class and area
        self.all_div = self.div[2].find_all('col-xs-4')
        self.total.append(self.all_div)
        # print(self.total)
        return(self.total)

class scrape2:
    def __init__(self):
        self.link = 'https://www.settrade.com/settrade/stock-quote/financialstatement?symbol=EE'
        self.raw_html = simple_get(self.link)
        self.html = BeautifulSoup(self.raw_html, 'html.parser')
        # print(html.text)

    def getTextinTbl2(self):
        print('hello')
        for div in self.html.find_all('div', attrs={'class': "table-responsive"}):
            print(div.text)

# A = scrape2()
# A.getTextinTbl2()
        # data_dict = dict()
        # self.table = self.html.find_all("div", attrs={'class': "card"})
        # print(self.table)
        # # finds the specific class and area
        # self.all_tr = self.table[0].find_all('font')
        # print(self.all_tr)
        # gets the information from specific table of choice (tr = row, td = column)
        # self.count = 0
        # for tr in self.all_tr:
        #     self.count = self.count + 1
        #     self.trim_text = ""
        #     self.all_td = tr.find_all('td')
        #
        #     self.key = ""
        #     self.value = ""
        #     self.i = 0
        #     for td in self.all_td:
        #         # gets specific row
        #         self.text = td.text
        #         # collects only the text
        #         self.text = self.text.strip()
        #         # strips spaces
        #         if self.i == 0:
        #             self.key = self.text
        #         else:
        #             self.value = self.text
        #
        #         self.i = self.i + 1
        #
        #     data_dict[self.key] = self.value
        # # return data_dict
        # print(data_dict)

# translator = Translator()
# result = translator.translate()
# print(result.text)

# A= scrape('EE', '05_stock_majorshareholder')
# # dict = A.getTextinTbl('table table-info', 1)
# A.getshareholders('table table-info')
# A.getchangerate()
# A.getshareholders('table table-info')
# A.gettotalshareholders()

# B = scrape2()
# B.getTextinTbl2()

# A= scrape('ADVANC', '03_stock_companyhighlight')
# A.getTextinTbl('col-xs-12', )

# KEY:
# scrape(stock, '01_stock_quote')
# #A.getchangerate()
#     Last Trade = data_dict[1]
#     Change = data_dict[2]
#     % Change = data_dict[3]
#
##A.getTextinTbl('table table-info', 0)
#     Prior = data_dict[ราคาปิดก่อนหน้า]
#     Open = data_dict[ราคาเปิด]
#     High = data_dict[ราคาสูงสุด]
#     Low	= data_dict[ราคาต่ำสุด]
#     Average Price = data_dict[ราคาเฉลี่ย]
#
##A.getTextinTbl('table table-info', 1)
#     Volume (Shares)	= data_dict[ปริมาณซื้อขาย (หุ้น)]
#     Value ('000 Baht) = data_dict[มูลค่าซื้อขาย ('000 บาท)]
#     Par Value (Baht) = data_dict[ราคาพาร์ (บาท)]
#     Ceiling	= data_dict[ราคา Ceiling]
#     Floor = data_dict[ราคา Floor]
#
##A.getTextinTbl('table table-info', 2)
#     Bid / Volume Bid = data_dict[ราคาเสนอซื้อ / ปริมาณเสนอซื้อ]
#     Offer / Volume Offer = data_dict[ราคาเสนอขาย / ปริมาณเสนอขาย]





