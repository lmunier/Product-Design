#!/usr/bin/python3
# -*-coding:Utf-8 -*
#lm181217.0145

# File to refresh data on the webpage

import re
from mariaDB import MySQL_Helper

def refreshDataView():
	dico_datas = {}

	# Create connector to database "smartbin"
	database = MySQL_Helper()

	query = "SELECT DISTINCT id_bin from filling_bins;"
	datas = database.ExecuteQuery(query)

	for elements in datas:
		query = "SELECT * from filling_bins WHERE id_bin = '{}' ORDER BY timestamp LIMIT 1;".format(elements[0])
		last_time = database.ExecuteQuery(query)
		dico_datas[elements[0]] = last_time[0]

	return dico_datas

def addData(data_to_add):
	# Recovery infos given
	id_bin_val = re.findall(r'id_bin (.*),', data_to_add)[0]
	filling_val = re.findall(r' filling (.*),', data_to_add)[0]
	battery_val = re.findall(r' battery (.*)', data_to_add)[0]

	# Create connector to database "smartbin"
	database = MySQL_Helper()

	query = "INSERT INTO filling_bins (timestamp, id_bin, filling, battery) VALUES(NOW(), '{0}', {1}, {2});".format(id_bin_val, filling_val, battery_val)
	database.ExecuteQuery(query)

if __name__ == '__main__':
	print("{}".format(dico))
