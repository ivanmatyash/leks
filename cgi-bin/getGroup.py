#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


	
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
	c.execute('SELECT tagID FROM voc WHERE idWord = {0}'.format(idMainWord))
	tagM = c.fetchall()[0][0]
	resStr = ''
	for idWord, word, tag in c.execute("SELECT v.idWord, v.word, t.name FROM voc v INNER JOIN tags t ON v.tagID = t.id WHERE v.idGroup = {0} AND (v.word != '{1}' OR v.tagID != {2}) ".format(idGroup, mainWord, tagM)):
		resStr += word + "(" + tag + ")[" + '<a href="#" onclick="remove({0}, {1});">x</a>]; '.format(idWord, idGroup)
	c.execute("SELECT t.name FROM tags t INNER JOIN voc v ON v.tagID = t.id WHERE v.idWord = {0}".format(idMainWord))
	mainWord += "(" + c.fetchall()[0][0] + ")"
	conn.commit()
	conn.close()
	message ='<h2>Информация о группе №{0}.</h2>\
	<table>\
	<tr> <td><b>Id группы: </b></td> <td>{0}</td> </tr>\
	<tr> <td><b>Основная форма: </b></td> <td>{1}</td> </tr>\
	<tr> <td><b>Другие формы: </b></td> <td>{2}</td> </tr>\
	</table>'.format(idGroup, mainWord, resStr)
	
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
		window.opener.location.reload();
        	window.close();
        } 
	function destroy(a)
	{
		if (confirm('Bы уверены, что хотите удалить группу №' + a + ' из словаря?')) 
		{
			location.href = '/cgi-bin/deleteGroup.py/?idGroup=' + a;
		}
	}
	function remove(a, b)
	{
		if (confirm('Bы уверены, что хотите удалить слово #' + a + ' из группы #' + b + '?')) 
		{
			location.href = '/cgi-bin/deleteFromGroup.py/?idWord=' + a + '&idGroup=' + b;
		}
	}
</script>

	</head>
	<body>""")
print(message)
print('''<br><center><a href="#" onclick="closeOpenedWindow();">[Закрыть окно]</a></center>''')
print("""</body>
	</html>""")
