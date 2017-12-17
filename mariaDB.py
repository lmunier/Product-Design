#!/usr/bin/python3
# -*-coding:Utf-8 -*

# File to manage database

import sys
sys.path.insert(0, '/home/pi/Product-Design/')

import pymysql.cursors
import os, re, base64
from credFinder import returnCred

class MySQL_Helper:

	def __init__(self): # on fait la connexion ici, en décodant le password directement
		Username, Password = returnCred(tyep_cred["mysql"])
		self.MySQLConnector = pymysql.connect(user=Username, password=Password, database='hello_world',  host='localhost')

	def close(self):
		self.MySQLConnector.close()

	def ExecuteQuery(self, SQLQuery, ReturnAsDictList=False):
		self.MySQLCursor = self.MySQLConnector.cursor() #création du curseur
		self.MySQLCursor.execute(SQLQuery) #exécution de la requête
		self.MySQLConnector.commit() #envoi de la requete à la DB

		self.ReturnedRows = []

		while True: #itère jusqu'à trouver une ligne entièremene entièrement vide
			Row = self.MySQLCursor.fetchone() #fetch les lignes

			if Row is None:
				break
			else:
				self.ReturnedRows.append(Row)

		return self.ReturnedRows #retourne quand tout a été fetch

