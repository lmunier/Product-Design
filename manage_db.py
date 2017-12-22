#!/usr/bin/python3
# -*-coding:Utf-8 -*
#lm201217.0405

# File to refresh data on the webpage

import re
from c_maria_db import MySQL_Helper

def get_data(id_bin, number):
	web_view = ""

	# Create connector to database "smartbin"
	database = MySQL_Helper()

	query = "SELECT * from filling_bins WHERE id_bin = '{0}' ORDER BY timestamp DESC LIMIT {1};".format(id_bin, number)
	datas = database.ExecuteQuery(query)

	for elements in datas:
		web_view += "{1}\\{0}\\{2}\\{3}/".format(elements[0], elements[1], elements[2], elements[3])

	return web_view

def get_id():
	str_bins_id = ""

	# Create connector to databse "smartbin"
	database = MySQL_Helper()

	query = "SELECT DISTINCT id_bin from filling_bins ORDER BY id_bin;"
	bins_id = database.ExecuteQuery(query)

	for id in bins_id:
		str_bins_id += str(id[0])
		str_bins_id += "/"
	return str_bins_id

def add_data(data_to_add):
	# Recovery infos given
	id_bin_val = re.findall(r'id\_bin ([\w ]*),', data_to_add)[0]
	filling_val = re.findall(r'filling (.*),', data_to_add)[0]
	battery_val = re.findall(r'battery (.*)', data_to_add)[0]

	# Create connector to database "smartbin"
	database = MySQL_Helper()

	query = "INSERT INTO filling_bins (timestamp, id_bin, filling, battery) VALUES(NOW(), '{0}', {1}, {2});".format(id_bin_val, filling_val, battery_val)
	database.ExecuteQuery(query)
