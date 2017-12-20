#!/bin/usr/python3
# -*-coding:Utf-8 -*
#lm201217.0403

# File to return credentials stocked in another secured file

import sys
sys.path.insert(0, '/home/pi/Product-Design/')

import re
import base64
from dico import type_cred

def return_cred(credentials):
        # Get credentials from MySQL Python Agent config file
        fid = open('/home/pi/pythonAgent.conf', 'r')
        ConfigFileBody = fid.read()
        fid.close()

        # Parse credentials
        user = re.findall(r'USER\=(.*)\n', ConfigFileBody)[0]
        mail = re.findall(r'MAIL\=(.*)\n', ConfigFileBody)[0]
        password_mysql = re.findall(r'PASS_MYSQL\=(.*)\n', ConfigFileBody)[0]
        password_mail = re.findall(r'PASS_MAIL\=(.*)\n', ConfigFileBody)[0]

        my_password_mysql = base64.b64decode(password_mysql).decode('utf-8')
        my_password_mail = base64.b64decode(password_mail).decode('utf-8')

        if credentials == type_cred["mail"]:
                return mail, my_password_mail
        elif credentials == type_cred["mysql"]:
                return user, my_password_mysql
