
from utilities.DBConnection import DBConnection

class FiratDao():

    def __init__(self):
        self.dbconnection = DBConnection()
        self.listMainAbs = []
        self.listAbs = []
        self.listStaff = []


    def getAbs(self,bolumName, birim):
        self.listAbs = self.dbconnection.readPersonelAbs(bolumName, birim)
        return self.listAbs

    def getStaff(self,bolumName, birim):
        self.listStaff = self.dbconnection.readPersonelStaff(bolumName, birim)
        return self.listStaff

    def getAbsAll(self):
        self.listMainAbs = self.dbconnection.readPersonelAbsAll()
        return self.listMainAbs


