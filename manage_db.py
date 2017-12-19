#!/usr/bin/python3
# -*-coding:Utf-8 -*
#lm181217.0145

# File to refresh data on the webpage

import re
from mariaDB import MySQL_Helper

def get_data(id_bin, number):
	web_view = ""

	# Create connector to database "smartbin"
	database = MySQL_Helper()

	query = "SELECT * from filling_bins WHERE id_bin = '{0}' ORDER BY timestamp LIMIT {1};".format(id_bin, number)
	datas = database.ExecuteQuery(query)

	for elements in datas:
		web_view += "<div>Measurement: {0}</div><div>ID: {1}</div><div>Filling: {2}</div><div>Battery: {3}\n".format(elements[0], elements[1], elements[2], elements[3])

	return web_view

def get_id():
	str_bins_id = ""

	# Create connector to databse "smartbin"
	database = MySQL_Helper()

	query = "SELECT DISTINCT id_bin from filling_bins;"
	bins_id = database.ExecuteQuery(query)

	for id in bins_id:
		str_bins_id += str(id[0])

	return str_bins_id

def add_data(data_to_add):
	# Recovery infos given
	id_bin_val = re.findall(r'id_bin (.*),', data_to_add)[0]
	filling_val = re.findall(r' filling (.*),', data_to_add)[0]
	battery_val = re.findall(r' battery (.*)', data_to_add)[0]

	# Create connector to database "smartbin"
	database = MySQL_Helper()

	query = "INSERT INTO filling_bins (timestamp, id_bin, filling, battery) VALUES(NOW(), '{0}', {1}, {2});".format(id_bin_val, filling_val, battery_val)
	database.ExecuteQuery(query)

if __name__ == '__main__':
	print("{}".format(get_data('Test_bin 10', 4)))
