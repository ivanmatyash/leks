#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


def removeInfo(idWord):
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	c.execute('UPDATE voc SET idGroup = -1 WHERE idWORD = {0}'.format(idWord))
	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
idWord = form_data.getfirst("idWord", "-1")
idGroup = form_data.getfirst("idGroup", "-1")

message = "Success!"

if idWord != '-1' and idGroup != '-1':
	removeInfo(idWord)
else:
	message = "Произошла ошибка передачи данных от клиента к серверу, это окно закроется автоматически."

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Удаление слова из группы</title>
	<script>
	function refresh(a) 
        {  
		location.href= "/cgi-bin/getGroup.py?idGroup=" + a;
		window.opener.location.reload();
        }  
	</script>
	</head>
	<body>""")
print(message)
print('<script type="text/javascript"> refresh({0}) </script>'.format(idGroup))
print("""</body>
	</html>""")
