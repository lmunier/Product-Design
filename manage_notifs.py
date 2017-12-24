#!/bin/usr/python3
# -*-coding:Utf-8 -*
#lm201217.0405

# File to automatically send e_mail

import sys
sys.path.insert(0, '/home/pi/Product-Design/')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from cred_finder import return_cred
from dico import type_cred

def send_mail(adress_to_send, message):
	adress_who_send, password = return_cred(type_cred["mail"])

	fromaddr = adress_who_send
	toaddr = adress_who_send
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "PO1_M1 needs help"

	body = "WARNING: Bin is {}% full ! Please come to save it..!".format(message)
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)

	server.quit()

if __name__ == "__main__":
	send_mail("smartbin.zip@gmail.com", "90")
