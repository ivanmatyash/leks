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

	
form_data = cgi.FieldStorage()
idGroup = form_data.getfirst("idGroup", "-1")
message = ''


if idGroup != '-1':
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	c.execute('SELECT idMain FROM groups WHERE id = {0}'.format(idGroup))
	idMainWord = c.fetchall()[0][0]
	c.execute('SELECT word FROM voc WHERE idWord = {0}'.format(idMainWord))
	mainWord = c.fetchall()[0][0]
	words = []
	for word in c.execute("SELECT word FROM voc WHERE idGroup = {0} AND word != '{1}'".format(idGroup, mainWord)):
		words.extend(word)
	conn.commit()
	conn.close()
	message ='<h2>Информация о группе №{0}.</h2>\
	<table>\
	<tr> <td><b>Id группы: </b></td> <td>{0}</td> </tr>\
	<tr> <td><b>Главное слово: </b></td> <td>{1}</td> </tr>\
	<tr> <td><b>Другие формы: </b></td> <td>{2}</td> </tr>\
	</table>'.format(idGroup, mainWord, words)
	
	message += '<br><br><center><a href ="#" onclick="destroy({0});">[Удалить группу]</a></center>'.format(idGroup)
	
	
else:
	message = "Произошла ошибка передачи данных от клиента к серверу, это окно закроется автоматически"

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Информация о группе</title>
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
	function destroy(a)
	{
		if (confirm('Bы уверены, что хотите удалить группу №' + a + ' из словаря?')) 
		{
			location.href = '/cgi-bin/deleteGroup.py/?idGroup=' + a;
		}
	}
    </script>

	</head>
	<body>""")
print(message)
print('''<br><center><a href="#" onclick="closeOpenedWindow();">[Закрыть окно]</a></center>''')
print("""</body>
	</html>""")
