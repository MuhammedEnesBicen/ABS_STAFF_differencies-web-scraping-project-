import sqlite3 as lite
import os.path

class DBConnection:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "firatDB.sqlite")
        self.vt = lite.connect(db_path)
        self.cr = self.vt.cursor()

    def createAccount(self, firstname, lastname, email, passwd):
        sql = """INSERT INTO users VALUES (?, ?, ?, ?)"""
        self.cr.execute(sql,(firstname,lastname,email,passwd))
        self.vt.commit()

    def login(self, email, passwd):
        self.cr.execute("""select * from users where email = '%s'and passwd = '%s'"""%(email, passwd))
        user = self.cr.fetchone()
        if(user):
            print("Hoşgeldin {} {}".format(user[0], user[1]))
            return True
        else:
            print("Kullanıcı adı veya parola hatalı")
            return False

    def readPersonelAbs(self, bolumName, birim):

        result = []
        personel = self.cr.execute("""select * from personel where bolum = '%s' and birim = '%s'"""%(bolumName, birim))
        for i in personel:
            result.append(i)

        return result

    def readPersonelStaff(self, bolumName, birim:str):

        if birim == "Tıp Fakültesi":
            birim  = "TIP FAKÜLTESİ"
        elif birim == "Veteriner Fakültesi":
            birim = "VETERİNER FAKÜLTESİ"
        elif birim == "Diş Hekimliği Fakütesi":
            birim = "DİŞ HEKİMLİĞİ"
        elif birim == "Devlet Konservatuvarı":
            birim = "DEVLET KONSERVATUVARI"
        elif birim == "Yabancı Diller Yüksekokulu":
            birim = "YABANCI DİLLER YÜKSEKOKULU"
        elif bolumName == "MAKİNA MÜHENDİSLİĞİ":
            birim = "MAKİNE MÜHENDİSLİĞİ"

        result = []
        personel = self.cr.execute("""select * from staff where bolum = '%s' or bolum = '%s'"""%(bolumName, birim))
        for i in personel:
            result.append(i)

        return result

    def readPersonelAbsAll(self):
        self.cr.execute("""select bolum, birim from personel """)
        personel = self.cr.fetchall()
        result = set(personel)

        return result







# db = DBConnection()
# # strings = db.readPersonelAbs("KLİNİK BİLİMLER","Diş Hekimliği Fakütesi")
#
# print(db.readPersonelAbsAll())


