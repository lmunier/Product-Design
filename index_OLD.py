#!/usr/bin/python3

# Turn on debug mode.
import cgitb
import pymysql.cursors

cgitb.enable()

# Print necessary headers.
print("Content-Type: text/html")
print()

template = "<html><body><h1>Hello {who}!</h1></body></html>"
print(template.format(who="World"))

# Connect to the database.
conn = pymysql.connect(
	host="127.0.0.1",
	user="root",
	passwd="22MySq04RoOt2017",
	db="hello_world")
#c = conn.cursor()

# Insert some example data.
#c.execute("INSERT INTO numbers VALUES (1, 'One!')")
#c.execute("INSERT INTO numbers VALUES (2, 'Two!')")
#c.execute("INSERT INTO numbers VALUES (3, 'Three!')")
#conn.commit()

# Print the contents of the database.
#c.execute("SELECT * FROM numbers")
#print([(r[0], r[1]) for r in c.fetchall()])

