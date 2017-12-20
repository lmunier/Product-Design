#!/usr/bin/python3
# -*-coding:Utf-8 -*
#lm201217.0519

# File to manage database

import sys
sys.path.insert(0, '/home/pi/Product-Design/')

import pymysql.cursors
import os, re, base64
from cred_finder import return_cred
from dico import type_cred

my_DB = 'smartbin'

class MySQL_Helper:

	def __init__(self): # We init a connection to our database 'smartbin'
		Username, Password = return_cred(type_cred["mysql"])
		self.MySQLConnector = pymysql.connect(user=Username, password=Password, database=my_DB,  host='localhost')

	def close(self):
		self.MySQLConnector.close()

	def ExecuteQuery(self, SQLQuery, ReturnAsDictList=False):
		self.MySQLCursor = self.MySQLConnector.cursor() 	# Ccreate cursor
		self.MySQLCursor.execute(SQLQuery) 			# Execute query
		self.MySQLConnector.commit() 				# Send query to our database

		self.ReturnedRows = []

		while True: 						# Read all elements to find an empty one
			Row = self.MySQLCursor.fetchone() 		# Fetch lines

			if Row is None:
				break
			else:
				self.ReturnedRows.append(Row)

		return self.ReturnedRows 				# Return when all is fetch

