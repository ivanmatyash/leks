#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3


print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Словарь</title>
	</head>
	<body>""")
print("<h1>Your Dictionary:</h1>")

conn = sqlite3.connect('/tmp/voc.db')
c = conn.cursor()

print('<table>')
for word, amount, tag in c.execute('SELECT * FROM voc ORDER BY word'):
	remove_str = '<a href = "delete.py/?DEL=1&ff=2">del</a>'
	print('<tr><td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td> </tr>'.format(word, tag, amount, remove_str))
print('</table>')
conn.close()
print("""</body>
	</html>""")
