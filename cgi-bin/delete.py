#!/usr/bin/env python3
import cgi, os
import html
import sqlite3

form = cgi.FieldStorage()
delete_but = form.getfirst("DEL", "123")
delete1 = form.getfirst("ff", "456")
print("Content-type: text/html\n")
print('''<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Deleting</title>
	</head>
	<body>''')
print("<p><h1>{0}, {1}</h1></p>".format(delete_but, delete1))
print("</body>")
print("</html>")
