#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


def removeInfo(word, tag):
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	
	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())

	c.execute("DELETE FROM voc WHERE word = '{0}' AND tagID = {1}".format(word, sl[tag]))
	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
word = form_data.getfirst("word", "-1")
tag = form_data.getfirst("tag", "-1")
amount = form_data.getfirst("amount", "-1")

message ='<h2>Удаление слова прошло успешно.</h2><b><h3>Информация об удаленном слове:</h3></b> \
	<table>\
	<tr><td><b>Слово: </b></td> <td>{0}</td></tr>\
	<tr><td><b>Тег: </b></td> <td>{1}</td></tr>\
	<tr><td><b>Количество: </b></td> <td> {2}</td></tr>\
	</table>Это окно закроется через 5 секунд автоматически.<br>'.format(word, tag, amount)

if word != '-1' and tag != '-1' and amount != '-1':
	removeInfo(word, tag)
else:
	message = "Произошла ошибка передачи данных от клиента к серверу, это окно закроется автоматически."

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Удаление слова из словаря</title>
<script>
        function closeW() 
        {  
	
            var t=setTimeout("closeOpenedWindow();", 5000); // закрыть через 5 сек
        }  
        function closeOpenedWindow()
        {  
		window.opener.location.reload();
        	window.close();
        } 
    </script>

	</head>
	<body>""")
print(message)
print('''<script type="text/javascript">
closeW()
</script>''')
print('''<br><center><a href="#" onclick="closeOpenedWindow();">[Закрыть отчет]</a></center>''')
print("""</body>
	</html>""")
