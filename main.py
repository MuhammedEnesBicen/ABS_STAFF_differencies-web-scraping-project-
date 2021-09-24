import sys

import requests
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QStackedWidget, QLineEdit, QMessageBox,QAction
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPen, QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QVBoxLayout


from htmlParse.main import GetDataFromInternet
from utilities import DBConnection
from utilities.firatDao import FiratDao
from utilities import mailSender
from parsingPage import Ui_Dialog

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomePage.ui", self)

        self.img_firat = QLabel(self)
        self.img_firat.setGeometry(650,10,200,100)
        pixmap = QPixmap('firat_logo.png')
        self.img_firat.setPixmap(pixmap)
        self.img_firat.resize(pixmap.width(),pixmap.height())
        self.ph_loginPage.clicked.connect(self.gotoLogin)
        self.ph_createAccountPage.clicked.connect(self.gotoCreateAccount)
        self.ph_parserPage.clicked.connect(self.gotoParse)
        self.ph_who.clicked.connect(self.gotoWho)



    # --------------------------------------
    def gotoParse(self):
        parse = ParsingScreen()
        widget.addWidget(parse)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # --------------------------------------
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCreateAccount(self):
        createAccount = CreateAccountScreen()
        widget.addWidget(createAccount)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoWho(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Getting data from internet takes time. It can took a few minutes. Untill complete mesage appear dont close program.")
        msg.setWindowTitle("Warning")
        msg.exec_()

        try:
            a = GetDataFromInternet()
            f = a.birimParser();
            for i, v in f.items():
                a.bolumParser(v)
            a.getStaffData()
        except Exception as e:
            print(e)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(
            "Getting data copleted.")
        msg.setWindowTitle("Warning")
        msg.exec_()



class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("loginPage.ui", self)
        self.ph_login.clicked.connect(self.loginScreen)
        self.ln_passwd.setEchoMode(QLineEdit.Password)
        self.createAccount.clicked.connect(self.gotoCreateAccount)
        self.ph_back.clicked.connect(self.gotoWelcome)

    def loginScreen(self):
        db = DBConnection.DBConnection()
        check = db.login(email=self.ln_email.text(), passwd=self.ln_passwd.text())
        if (check):
            self.gotoParse()
        else:
            self.mesaj.setText("Email or password is wrong !!!")

    def gotoParse(self):
        parse = ParsingScreen()
        widget.addWidget(parse)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCreateAccount(self):
        createAccount = CreateAccountScreen()
        widget.addWidget(createAccount)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoWelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAccountScreen(QDialog):
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        loadUi("createAccountPage.ui", self)
        self.ph_create.clicked.connect(self.gotoVerificationCodeScreen)
        self.loginPage.clicked.connect(self.gotoLogin)
        self.ph_back.clicked.connect(self.gotoWelcome)

    def gotoVerificationCodeScreen(self):
        codeResult = mailSender.sendMail(self.ln_email.text())

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Currently sending mail is simulated. If you really want to send mail,"
                    " fill in the mail and password section in the "
                    "MailSender class and make sure you allow low-security applications in your mail.")
        msg.setWindowTitle("Warning")
        msg.exec_()


        if (codeResult[0]):
            print("Mail sent")
            verificationCode = VerificationCodeScreen(firstname=self.ln_firstname.text(),
                                                      lastname=self.ln_lastname.text(),
                                                      email=self.ln_email.text(), passwd=self.ln_passwd.text(),
                                                      code=codeResult[1])
            widget.addWidget(verificationCode)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        else:
            print("Mail didn't sent!!!")

    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoWelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class VerificationCodeScreen(QDialog):
    def __init__(self, firstname, lastname, email, passwd, code):
        super(VerificationCodeScreen, self).__init__()
        loadUi("verificationPage.ui", self)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.passwd = passwd
        self.code = code
        print(code)
        self.ph_send.clicked.connect(self.verification)

    def verification(self):
        if (str(self.code) == str(self.ln_verificationCode.text())):
            db = DBConnection.DBConnection()
            db.createAccount(firstname=self.firstname, lastname=self.lastname, email=self.email, passwd=self.passwd)
            self.gotoLogin()
        else:
            self.mesaj.setText("Verification code is wrong !!!")

    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ParsingScreen(QDialog):
    def __init__(self):
        super(ParsingScreen, self).__init__()
        self.firatDao = FiratDao()
        self.domain = "https://abs.firat.edu.tr/"
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #self.ui.ph_difference =  QAction(QIcon("r3.png"), "Search", self) #*adding icon to button
        #self.ui.ph_display.setIcon(QIcon("r3.png"))
        header = self.ui.tableAbs.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)


        header2 = self.ui.tableStaff.horizontalHeader()
        header2.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.ph_display.clicked.connect(self.display)
        self.comboboxBirimUpdate()

        self.ui.ph_errors.clicked.connect(self.errors)

        self.ui.cb_birim.currentIndexChanged.connect(self.updateBolum)
        self.updateBolum(self.ui.cb_birim.currentIndex())

        self.ui.ph_difference.clicked.connect(self.difference)


    def comboboxBirimUpdate(self):
        listDao = sorted(self.firatDao.getAbsAll())

        birimler = []
        for ls in listDao:
            tmp = ls[1]
            birimler.append(tmp)

        birimler = sorted(set(birimler))
        print(birimler)
        for br in birimler:
            bolumler = []
            for i in listDao:
                if i[1] == br:
                    tmp = i[0]
                    bolumler.append(tmp)
            self.ui.cb_birim.addItem(br, bolumler)

    def updateBolum(self,index):
        self.ui.cb_bolum.clear()
        bolumler = self.ui.cb_birim.itemData(index)
        if bolumler:
            self.ui.cb_bolum.addItems(bolumler)

    def display(self):
        self.ui.tableAbs.clear()
        self.ui.tableStaff.clear()
        self.ui.tableAbs.setRowCount(0)
        self.ui.tableStaff.setRowCount(0)

        birimName = str(self.ui.cb_birim.currentText())
        bolumName = str(self.ui.cb_bolum.currentText())

        if birimName == "Tıp Fakültesi" or birimName == "Veteriner Fakültesi" or birimName == "Diş Hekimliği Fakütesi" or birimName== "Devlet Konservatuvarı" or birimName == "Yabancı Diller Yüksekokulu":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The instructors of the {} deparment you have chosen are available on the staff website, not under deparments, but all together. Therefore, the comparisons to be made are made between the instructors of the selected department in abs and all the instructors in the staff.".format(birimName))
            msg.setWindowTitle("Warning")
            msg.exec_()

        resultAbs = self.firatDao.getAbs(bolumName, birimName)
        resultStaff = self.firatDao.getStaff(bolumName, birimName)
        if (len(resultStaff) < 1):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("There is no {} 'deparment in the staff service".format(bolumName))
            msg.setWindowTitle("Warning")
            msg.exec_()

        # Abs datas adding table
        for row_number, row_data, in enumerate(resultAbs):
            self.ui.tableAbs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):

                if column_number == 4:
                    r = requests.get(self.domain + column_data, stream=True)
                    assert r.status_code == 200
                    img = QImage()
                    assert img.loadFromData(r.content)
                    w = QLabel()

                    w.setScaledContents(True)
                    w.setGeometry(QtCore.QRect(0,0,50,50))
                    w.setPixmap(QPixmap.fromImage(img))

                    item = w
                    self.ui.tableAbs.setRowHeight(row_number,100)
                    self.ui.tableAbs.setCellWidget(row_number,column_number,item)
                    #self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))
                else :
                    item = str(column_data)
                    self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))


        #Staff datas adding table
        for row_number, row_data, in enumerate(resultStaff):
            self.ui.tableStaff.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = str(column_data)
                self.ui.tableStaff.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))



    def difference(self):
        self.ui.tableAbs.clear()
        self.ui.tableStaff.clear()
        self.ui.tableAbs.setRowCount(0)
        self.ui.tableStaff.setRowCount(0)

        birimName = str(self.ui.cb_birim.currentText())
        bolumName = str(self.ui.cb_bolum.currentText())

        resultAbs = self.firatDao.getAbs(bolumName, birimName)
        resultStaff = self.firatDao.getStaff(bolumName, birimName)

        dataAbs = self.findDifferencies(resultAbs, resultStaff)
        dataStaff = self.findDifferencies(resultStaff, resultAbs)


        # Abs datas adding table
        for row_number, row_data, in enumerate(dataAbs):
            self.ui.tableAbs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                if column_number == 4:
                    r = requests.get(self.domain + column_data, stream=True)
                    assert r.status_code == 200
                    img = QImage()
                    assert img.loadFromData(r.content)
                    w = QLabel()

                    w.setScaledContents(True)
                    w.setGeometry(QtCore.QRect(0, 0, 50, 50))
                    w.setPixmap(QPixmap.fromImage(img))

                    item = w
                    self.ui.tableAbs.setRowHeight(row_number, 100)
                    self.ui.tableAbs.setCellWidget(row_number, column_number, item)
                else :
                    item = str(column_data)
                    self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))

        # Staff datas adding table
        for row_number, row_data, in enumerate(dataStaff):
            self.ui.tableStaff.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = str(column_data)
                self.ui.tableStaff.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))



    def errors(self):
        self.ui.tableAbs.clear()
        self.ui.tableStaff.clear()
        self.ui.tableAbs.setRowCount(0)
        self.ui.tableStaff.setRowCount(0)

        birimName = str(self.ui.cb_birim.currentText())
        bolumName = str(self.ui.cb_bolum.currentText())

        resultAbs = self.firatDao.getAbs(bolumName, birimName)
        resultStaff = self.firatDao.getStaff(bolumName, birimName)

        dataAbs = self.findErrors(resultAbs, resultStaff)

        # Abs datas adding table
        for row_number, row_data, in enumerate(dataAbs):
            self.ui.tableAbs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                if column_number == 4:
                    r = requests.get(self.domain + column_data, stream=True)
                    assert r.status_code == 200
                    img = QImage()
                    assert img.loadFromData(r.content)
                    w = QLabel()

                    w.setScaledContents(True)
                    w.setGeometry(QtCore.QRect(0, 0, 50, 50))
                    w.setPixmap(QPixmap.fromImage(img))

                    item = w
                    self.ui.tableAbs.setRowHeight(row_number, 100)
                    self.ui.tableAbs.setCellWidget(row_number, column_number, item)
                else:
                    item = str(column_data)
                    self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))




    def isExist(self,x, name):
        return True if (x[2] == name) else False

    def findDifferencies(self,firstLilst, secondList):
        # Returns those that are in the 1st list but not in the second, in the order given
        responseList = []
        for i in firstLilst:
            sonuc = any(self.isExist(j, i[2]) for j in secondList)
            if (sonuc == False):
                responseList.append(i)

        return responseList

    def getItem(self,name, secondList):
        for i in secondList:
            if (i[2] == name):
                return i

        return None

    def findErrors(self,firstList, secondList):  # 1.liste: abs - 2. liste: staff
        # when this function is called, the first parameter should be the abs list because the title part is redundant abs -> staff: Prof. abs: Prof. Dr.        result = []
        result = []
        for i in firstList:
            errors = ""
            temp = self.getItem(i[2], secondList)
            if (temp != None):
                if (temp[0] != i[0]):
                    errors += "deparment information does not match; {} - {} \n".format(i[0], temp[0])
                if (str(i[1]).__contains__(temp[1]) == False):
                    errors += "title information does not match; {} - {}".format(i[1], temp[1])
                if (errors != ""):
                    tempList =list(i)
                    tempList[3]=errors
                    i=tuple(tempList)
                    result.append(i)
        return result





app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.setWindowTitle("Firat University head of IT department")
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1550)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
