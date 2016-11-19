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
print("<tr><td><b>Word</b></td> <td><b>Tag</b></td> <td><b>Description</b></td> <td><b>Rus. description</b></td> <td><b>Amount</b></td> <td><b>Delete</b></td></tr>")
for word, amount, tag, en_d, ru_d, color in c.execute('SELECT v.word, v.amount, t.name, t.description, t.translate, t.color FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY word'):
	remove_str = '<a href = "delete.py/?DEL=1&ff=2">del</a>'
	print('<tr style="background:#{0}">'.format(color))
	print('<td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td> <td>{4}</td> <td>{5}</td>'.format(word, tag, en_d, ru_d, amount, remove_str))
	print('</tr>')
print('</table>')
conn.close()
print("""</body>
	</html>""")
