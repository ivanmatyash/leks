#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3

form = cgi.FieldStorage()
file_name = form["filename"]

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Создание нового словаря</title>
	</head>
	<body>""")
print("<h1>Your Dictionary:</h1>")

if file_name.filename:
	fn = os.path.basename(file_name.filename)
	open('/tmp/' + fn, 'wb').write(file_name.file.read())
	res = edit_text.makeVoc(fn)

	if res == 1:
		message = "Success"
	else:
		message = "error"
else:
	message = "WRONG"

conn = sqlite3.connect('/tmp/voc.db')
c = conn.cursor()

print('<a href = "voc.py">Dictionary</a>')
conn.close()
print("<p>status: {}</p>".format(message))
print("""</body>
	</html>""")