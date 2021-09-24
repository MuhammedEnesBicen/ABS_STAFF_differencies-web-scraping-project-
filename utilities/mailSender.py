import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def sendMail(toMailAdress):
    
    mesaj = MIMEMultipart()
    
    mesaj["from"] = "firatabs23@gmail.com"
    mesaj["to"] = toMailAdress
    mesaj["subject"] = "confirmation code"

    num = random.randrange(1000,9999)
    yazi = "Your code for login is : {}".format(num)
    mesaj_yapisi = MIMEText(yazi, "plain")
    mesaj.attach(mesaj_yapisi)
    try:
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        #change mail and password in following line
        mail.login("firatabs23@gmail.com", "")
        mail.sendmail(mesaj["from"], mesaj["to"], mesaj.as_string())
        print("Mail sent")
        mail.close()
        return (True,num)
    except:
        return (False,num)


