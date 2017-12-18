#!/usr/bin/python3
# -*-coding:Utf-8 -*

# File to test mariaDB

from mariaDB_help import MySQL_Helper

database = MySQL_Helper()
#query = "USE hello_world;"
#database.ExecuteQuery(query)

query = "INSERT INTO numbers (num, word) VALUES(40, 'test3');"
database.ExecuteQuery(query)

query = "SELECT * from numbers;"
result= database.ExecuteQuery(query)

print("{0}".format(result[0]))

database.close()
