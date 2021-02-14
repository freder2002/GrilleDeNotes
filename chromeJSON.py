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
notes = {}
notes['notes'] = []


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
    browser=webdriver.Chrome()

    url=r'' + session
    browser.get(url)

    input_a=browser.find_element_by_id("username")
    input_b=browser.find_element_by_id("password")
    input_a.send_keys(usernameUNI)
    input_b.send_keys(passwdUNI)
    browser.find_elements_by_class_name("btn-submit")[0].click()

    jason=json.loads(browser.find_elements_by_tag_name("pre")[
        0].get_attribute("innerText"))
    browser.close()

    for i in range(len(jason[0]) - 1):
        for j in range(len(jason[i]['evaluations'])):
            notes['notes'].append({
                'title': str(jason[i]['evaluations'][j]['title']),
                'value': formatANote(jason[i]['evaluations'][j]['score'], jason[i]['evaluations'][j]['weighting'])
            })

    diff=False
    nbItems=0
    with open('notes.json') as jsonFile:
        ancienneNotes=json.load(jsonFile)
        nbItems=len(ancienneNotes['notes'])
        for id, n in enumerate(notes['notes']):
            if(ancienneNotes['notes'][id]['value'] != n['value']):
                sendMail(str(n['title']) + " : " + str(n['value']))
                diff=True
                break
        if(nbItems != len(notes['notes'])):
            diff=True

    if diff or i == 0:
        with open('notes.json', 'w') as jsonFile:
            json.dump(notes, jsonFile)

except Exception as f:
    sendMail(str(f))
