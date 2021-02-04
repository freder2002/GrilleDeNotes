from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import hashlib
import smtplib
import datetime
import time

usernameUNI = 'uni username'
passwdUNI = 'uni passwd'
session = 'H21'
emailADDRToSend = "email to send email to "
emailSender = "email to send from"
emailSenderPasswd = 'passwd for that email'
email_text = """\
From: %s
To: %s
Subject: %s
""" % (emailSender,emailADDRToSend,'Une nouvelle note est disponible')


def sendMail():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(emailSender, emailSenderPasswd)
        server.sendmail(emailSender, emailADDRToSend, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')

opts = webdriver.ChromeOptions()
opts.add_argument('headless')
browser = webdriver.Chrome(options=opts)

url = r'url to la grille de note' + session
browser.get(url)

input_a = browser.find_element_by_id("username")
input_b = browser.find_element_by_id("password")
input_a.send_keys(usernameUNI)
input_b.send_keys(passwdUNI)
browser.find_elements_by_class_name("btn-submit")[0].click()

f = open("notesHASH.txt", "r")

hash_object = hashlib.md5(browser.page_source.encode())
print("hash de la page actuel	  ==>: " + str(hash_object.hexdigest()))
hash = str(f.read())
print("hash de la derniere lecture ==>: " + str(hash))

if(hash != ""):
    if(str(hash_object.hexdigest()) != hash):
        print("les hashs sont differents")
        f.close()
        f = open("notesHASH.txt", "w")
        sendMail()
        f.write(hash_object.hexdigest())
        f.close()
    else:
        print("Les hashs sont pareils")
        f.close()
else:
    f.close()
    f = open("notesHASH.txt", "w")
    f.write(hash_object.hexdigest())
    f.close()
