#!/bin/usr/python3
# -*-coding:Utf-8 -*
#lm201217.0405

# File to automatically send e_mail

import sys
sys.path.insert(0, '/home/pi/Product-Design/')

import smtplib
from cred_finder import return_cred
from dico import type_cred

def send_mail(adress_to_send, message):
	adress_who_send, password = return_cred(type_cred["mail"])

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(adress_who_send, password)

	message_to_send = "WARNING: Bin is {} full ! Please come to save it..!".format(message)
	message_to_send = "Hello"
	server.sendmail(adress_who_send, adress_to_send, message_to_send)
	server.quit()

if __name__ == "__main__":
	send_mail("louis.munier17@gmail.com", "90")
