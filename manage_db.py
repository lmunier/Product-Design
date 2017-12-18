#!/usr/bin/python3
# -*-coding:Utf-8 -*
#lm181217.0145

# File to refresh data on the webpage

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

if __name__ == '__main__':
	print("{}".format(dico))
