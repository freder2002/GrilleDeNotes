from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

usernameUNI = ''
passwdUNI = ''
session = ''
emailADDRToSend = ""
emailSender = ""
emailSenderPasswd = ''

def sendMail(txt):
    msg = MIMEMultipart()
    msg['Subject'] = txt
    msg['From'] = emailSender
    msg['To'] = emailADDRToSend
    msgText = MIMEText(' ', 'html')
    msg.attach(msgText)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(emailSender, emailSenderPasswd)
    server.sendmail(emailSender, emailADDRToSend, msg.as_string())
    server.close()


def formatANote(value, total):
    return ("None" if value == None else str(value) + "/" + str(total) + " => " + str("{:.2f}".format(value / total * 100)) + "%")


try:
    browser = webdriver.Chrome()

    url = r'' + session
    browser.get(url)

    input_a = browser.find_element_by_id("username")
    input_b = browser.find_element_by_id("password")
    input_a.send_keys(usernameUNI)
    input_b.send_keys(passwdUNI)
    browser.find_elements_by_class_name("btn-submit")[0].click()

    jason = json.loads(browser.find_elements_by_tag_name("pre")[
        0].get_attribute("innerText"))
    browser.close()

    notes = open('notesJSON.json', 'r')
    listeDuWeb = []
    for i in range(len(jason[0]) - 1):
        for j in range(len(jason[i]['evaluations'])):
            listeDuWeb.append(str(jason[i]['evaluations'][j]['title']) + formatANote(
                jason[i]['evaluations'][j]['score'], jason[i]['evaluations'][j]['weighting']))

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
    f.writelines(listeDuWeb)
    f.close()
except Exception as f:
    print(f)
