#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3

def removeGroup(idGroup):
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	c.execute('SELECT idMain FROM groups WHERE id = {0}'.format(idGroup))
	indMainWord = c.fetchall()[0][0]
	c.execute('SELECT word FROM voc WHERE idWord = {0}'.format(indMainWord))
	global mainWord
	mainWord = c.fetchall()[0][0]
	global otherWords
	otherWords = []
	for temp in c.execute("SELECT word FROM voc WHERE idGroup = {0} AND word != '{1}'".format(idGroup, mainWord)):
			otherWords.extend(temp)

	c.execute('DELETE FROM groups WHERE id ={0}'.format(idGroup))
	c.execute('UPDATE voc SET idGroup = -1 WHERE idGroup = {0}'.format(idGroup))
	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
idGroup = form_data.getfirst("idGroup", "-1")

message = ''

if idGroup != '-1':
	removeGroup(idGroup)
	message ='<h2>Удаление группы прошло успешно.</h2><b><h3>Информация об удаленной группе:</h3></b> \
	<table>\
	<tr><td><b>Главное слово: </b></td> <td>{0}</td></tr>\
	<tr><td><b>Другие формы: </b></td> <td>{1}</td></tr>\
	<tr><td><b>Номер группы: </b></td> <td> {2}</td></tr>\
	</table>Это окно закроется через 5 секунд автоматически.<br>'.format(mainWord,otherWords,idGroup)
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
		window.opener.location.reload()
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
