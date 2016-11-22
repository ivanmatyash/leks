#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


def addInfo(idWord):
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	
	c.execute('INSERT INTO groups (idMain) VALUES({0})'.format(idWord))
	c.execute('SELECT id FROM groups WHERE idMain = {0}'.format(idWord))
	t = c.fetchall()[0][0]
	c.execute('UPDATE voc SET idGroup = {0} WHERE idWord={1}'.format(t, idWord))

	conn.commit()
	conn.close()

def addInGroup(idWord, idExcGroup):
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	c.execute('UPDATE voc SET idGroup = {0} WHERE idWord={1}'.format(idExcGroup, idWord))

	conn.commit()
	conn.close()
	
form_data = cgi.FieldStorage()
idWord = form_data.getfirst("idWord", "-1")
idExcGroup = form_data.getfirst("idExcGroup", "-1")
message = ''


if idWord != '-1' and idExcGroup == '-1':
	addInfo(idWord)
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	
	c.execute('SELECT word FROM voc WHERE idWord = {0}'.format(idWord))
	wordS = c.fetchall()[0][0]
	c.execute('SELECT id FROM groups  WHERE idMain = {0}'.format(idWord))
	idGr = c.fetchall()[0][0]
	conn.commit()
	conn.close()
	message ='<h2>Добавление слова в группу прошло успешно.</h2>\
	<h3>Информация о добавленном слове: </h3>\
	<table>\
	<tr> <td><b>Id слова: </b></td> <td>{0}</td> </tr>\
	<tr> <td><b>Слово: </b></td> <td>{1}</td> </tr>\
	<tr> <td><b>Id новой группы: </b></td> <td>{2}</td> </tr>\
	</table><br>Это окно закроется через 5 секунд автоматически.<br>'.format(idWord, wordS, idGr)
elif idWord != '-1' and idExcGroup != '-1':
	addInGroup(idWord, idExcGroup)
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	c.execute('SELECT word FROM voc WHERE idWord = {0}'.format(idWord))
	wordS = c.fetchall()[0][0]
	conn.commit()
	conn.close()
	message ='<h2>Добавление слова в группу прошло успешно.</h2>\
	<h3>Информация о добавленном слове: </h3>\
	<table>\
	<tr> <td><b>Id слова: </b></td> <td>{0}</td> </tr>\
	<tr> <td><b>Слово: </b></td> <td>{1}</td> </tr>\
	<tr> <td><b>Id группы: </b></td> <td>{2}</td> </tr>\
	</table><br>Это окно закроется через 5 секунд автоматически.<br>'.format(idWord, wordS, idExcGroup)
	
else:
	message = "Произошла ошибка передачи данных от клиента к серверу, это окно закроется автоматически"

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Добавление слова в группу</title>
<script>
        function closeW() 
        {  
	
            var t=setTimeout("closeOpenedWindow();", 5000); // закрыть через 2 сек
        }  
        function closeOpenedWindow()
        {  
		window.opener.document.location="/cgi-bin/voc.py";
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
