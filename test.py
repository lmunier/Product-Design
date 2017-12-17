#!/usr/bin/python3
# -*-coding:Utf-8 -*

# File to test requests

import requests

r = requests.get('http://localhost')
print('{0}'.format(r.text))
