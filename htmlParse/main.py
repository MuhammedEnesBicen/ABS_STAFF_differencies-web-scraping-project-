import requests
import sqlite3 as lite
import os.path
from selenium import webdriver
import time


from bs4 import BeautifulSoup
from obspy.core.util.attribdict import AttribDict

class GetDataFromInternet() :

    def __init__(self):
        #os.chdir("..") i close this because i call this func. from main folder
        os.chdir("utilities/")
        print(os.getcwd())

        #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.getcwd()
        print(BASE_DIR)
        db_path = os.path.join(BASE_DIR, "firatDB.sqlite")
        self.vt = lite.connect(db_path)
        self.cr = self.vt.cursor()

        self.domain = "https://abs.firat.edu.tr/arama/birimler.html"
        self.personeller = []
        self.birimler = AttribDict()
        self.bolumler = AttribDict()
        self.clearDatabase()

    def personelParse(self,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        veri = soup.find_all("div", {"class": "content-wrapper"})
        tablo = veri[0]
        tablo = tablo.find_all("div", {"class": "container"})
        tablo = tablo[0].find_all("section", {"class": "content nopadding"})
        tablo = tablo[0].find_all("table", {"class": "tablesorter"})
        hocalar = tablo[0].find_all("tbody")
        hocalar = hocalar[0].find_all("tr")

        temp = None
        self.personeller = []
        for hoca in hocalar:
            isim_ve_unvan = hoca.find_all("a")
            fakulte = hoca.find_all("p")
            img = hoca.find("img")

            temp = [img.attrs["src"], isim_ve_unvan[0].text, str(fakulte[1].text), str(fakulte[0].text)]
            self.parcalaVeDbEkle(img.attrs["src"], isim_ve_unvan[0].text, str(fakulte[1].text), str(fakulte[0].text))
            self.personeller.append(temp)
        return self.personeller


    def isimUnvanParcala(isimUnvan):
        getindex = isimUnvan.rfind(".")
        return isimUnvan[0:getindex + 1], isimUnvan[getindex + 2:]


    def birimParser(self):
        url = self.domain
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table", {"id": "tablesorter-ahmet"})
        tbody = table.find_all("tbody")
        birimler = tbody[0].find_all("tr")

        for i in birimler:
            a = i.find("a")
            birimUrl = a.attrs["href"]
            birimName = a.text
            self.birimler[birimName] = birimUrl

        return self.birimler


    def bolumParser(self,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table", {"id": "tablesorter-ahmet"})

        tbody = table.find_all("tbody")
        bolumler = tbody[0].find_all("tr")
        self.bolumler = AttribDict()

        for i in bolumler:
            a = i.find("a")
            bolumUrl = a.attrs["href"]
            bolumName = a.text
            self.bolumler[bolumName] = bolumUrl

            self.personelParse(bolumUrl)

        return self.bolumler

    def parcalaVeDbEkle(self, img, isimUnvan, birim, bolum):
        isim = ""
        unvan = ""
        try:
            if (isimUnvan.__contains__("Prof. Dr.")):
                unvan = "Prof. Dr."
                isim = isimUnvan.replace(unvan, "")
            elif (isimUnvan.__contains__("Doç. Dr.")):
                unvan = "Doç. Dr."
                isim = isimUnvan.replace(unvan, "")
            elif (isimUnvan.__contains__("Dr. Öğr. Üyesi")):
                unvan = "Dr. Öğr. Üyesi"
                isim = isimUnvan.replace(unvan, "")
            elif (isimUnvan.__contains__("Arş. Gör. Dr.")):
                unvan = "Arş. Gör. Dr."
                isim = isimUnvan.replace(unvan, "")
            elif (isimUnvan.__contains__("Öğr. Gör. Dr.")):
                unvan = "Öğr. Gör. Dr."
                isim = isimUnvan.replace(unvan, "")
            elif (isimUnvan.__contains__("Arş. Gör.")):
                unvan = "Arş. Gör."
                isim = isimUnvan.replace(unvan, "")
            elif (isimUnvan.__contains__("Öğr. Gör.")):
                unvan = "Öğr. Gör."
                isim = isimUnvan.replace(unvan, "")

            isim = isim.replace("i", "İ").upper().strip()
            unvan = unvan.strip()
            birim = birim.strip()
            bolum = bolum.replace("i", "İ").upper().replace(" BÖLÜMÜ", "").strip()

            sql = """INSERT INTO personel VALUES (?, ?, ?,?,?)"""
            self.cr.execute(sql, (bolum, unvan, isim, birim, img))
            self.vt.commit()

            print("'{}' '{}' '{}' '{}'".format(isim, unvan, birim, bolum))

        except Exception as e:
            print(e)
            print("Eror: {} {} {} de meydana geldi. htmlparse satır 135".format(isimUnvan, birim, bolum))

    def addDb(self, bolum, unvan, isim, birim, img):
        sql = """INSERT INTO personel VALUES (?, ?, ?,?,?)"""
        self.cr.execute(sql,(bolum, unvan, isim, birim, img))
        self.vt.commit()



    def getStaffData(self):
        def verileriGetir():

            bolumAdi = browser.find_element_by_xpath("/html/body/div/div/div[3]/div[1]/a/strong")
            print(bolumAdi.text)

            liste = browser.find_elements_by_class_name("profile_view")

            # print(liste)
            for i in liste:
                try:
                    unvanAd = i.find_elements_by_tag_name("h2")
                    email = i.find_element_by_tag_name("p").text
                    ABDDahili = i.find_elements_by_tag_name("li")

                    unvan = unvanAd[0].text
                    ad = unvanAd[1].text
                    ABD = ABDDahili[0].text
                    Dahili = ABDDahili[1].text
                    #print("{} {} {} {} {}".format( unvan, ad, email, ABD, Dahili) )

                    sql = """INSERT INTO staff VALUES (?, ?, ?, ?, ?, ?)"""
                    self.cr.execute(sql, (str(bolumAdi.text), str(unvan), str(ad), str(email), str(ABD), str(Dahili)))
                    self.vt.commit()
                except:
                    continue

        print("*" * 30)
        print()

        browser = webdriver.Chrome()

        browser.get("https://staff.firat.edu.tr")
        # time.sleep(7) #site yüklensin diye

        fakulte = browser.find_elements_by_tag_name("form")

        for i in range(len(fakulte)):

            try:

                fakulte[i].submit()
                # print(i)
                verileriGetir()
                fakulte = browser.find_elements_by_tag_name("form")

                time.sleep(2)
            except:
                print(i)

        browser.get("https://staff.firat.edu.tr/faculty.jsp?value1=4&value2=1042") #tıp için
        verileriGetir()
        browser.get("https://staff.firat.edu.tr/faculty.jsp?value1=5&value2=1043") #veterinerlik linki
        verileriGetir()
        browser.get("https://staff.firat.edu.tr/faculty.jsp?value1=37&value2=1004") # diş hekimliği
        verileriGetir()
        browser.get("https://staff.firat.edu.tr/faculty.jsp?value1=22&value2=1003") # devlet conservatuarı
        verileriGetir()
        browser.get("https://staff.firat.edu.tr/faculty.jsp?value1=34&value2=1044")  # yabancı diller yüksek okulu
        verileriGetir()

    def clearDatabase(self):
        sql = """DELETE FROM personel"""
        self.cr.execute(sql)
        sql = """DELETE FROM staff"""
        self.cr.execute(sql)
        self.vt.commit()


# a = GetDataFromInternet();
# # We getting data from internet and fill db in here...
# f = a.birimParser();
# for i,v in f.items():
#     a.bolumParser(v)
# a.getStaffData()


