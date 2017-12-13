#!/usr/bin/python3

# Turn on debug mode.
import cgitb
import mysql.connector

cgitb.enable()

# Print necessary headers.
print("Content-Type: text/html")
print()

template = "<html><body><h1>Hello {who}!</h1></body></html>"
print(template.format(who="Reader"))

# Connect to the database.
conn = mysql.connector.connect(
	host="localhost",
	user="root",
	database="hello_world",
	password="22MySq04RoOt2017")
c = conn.cursor()

# Insert some example data.
c.execute("INSERT INTO numbers VALUES (1, 'One!')")
c.execute("INSERT INTO numbers VALUES (2, 'Two!')")
c.execute("INSERT INTO numbers VALUES (3, 'Three!')")
conn.commit()

# Print the contents of the database.
c.execute("SELECT * FROM numbers")
print([(r[0], r[1]) for r in c.fetchall()])
