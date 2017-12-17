#!/bin/usr/python3
# -*-coding:Utf-8 -*

# File to automatically send e_mail

import sys
sys.path.insert(0, '/home/pi/Product-Design/')

import smtplib
from credFinder import returnCred

def send_mail(adress_who_send, adress_to_send, password, message):
	adress_who_send, password = returnCred(type_cred["mail"])

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(adress_who_send, password)

	server.sendmail(adress_who_send, adress_to_send, message)
	server.quit()
