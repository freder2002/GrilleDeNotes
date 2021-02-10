from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import hashlib
import smtplib
import datetime
import time
import json

usernameUNI = ''
passwdUNI = ''
session = ''
emailADDRToSend = ""
emailSender = ""
emailSenderPasswd = ''

def sendMail(note):
    email_text = """From: %s
    To: %s
    Subject: %s """ % (emailSender, emailADDRToSend, (str(note) + " !"))
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(emailSender, emailSenderPasswd)
    server.sendmail(emailSender, emailADDRToSend, email_text)
    server.close()

opts = webdriver.ChromeOptions()
opts.add_argument('headless')
browser = webdriver.Chrome(options=opts)

url = r'' + session
browser.get(url)

input_a = browser.find_element_by_id("username")
input_b = browser.find_element_by_id("password")
input_a.send_keys(usernameUNI)
input_b.send_keys(passwdUNI)
browser.find_elements_by_class_name("btn-submit")[0].click()

jason = json.loads(browser.find_elements_by_tag_name("pre")
                   [0].get_attribute("innerText"))

notes = open('notesJSON.json', 'r')
listeDuWeb = []
for i in range(len(jason[0]) - 1):
    for j in range(len(jason[i]['evaluations'])):
        listeDuWeb.append(str(jason[i]['evaluations'][j]['title']) + ":" + str(jason[i]['evaluations'][j]['score']))

diff = False
i = 0
while True:
    listeFichier = notes.readline()
    if not listeFichier:
        break
    if(listeDuWeb[i] != listeFichier):
        sendMail(listeDuWeb[i])
        diff = True
        break
    i += 1

notes.close()
f = open('notesJSON.json', 'w')
f.write(listeDuWeb)
f.close()
browser.close()