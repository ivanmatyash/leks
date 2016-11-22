#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


def getGroups():
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	d = conn.cursor()
	e = conn.cursor()
	result = ""
	result += '<table width=100%>'
	result += '<tr><td><b>Id группы</b></td> <td><b>Главное слово</b></td> <td><b>Другие формы:</b></td><td><b>Добавить:</b></td></tr>'
	for id, idMain in c.execute('''SELECT id, idMain FROM groups'''):
		d.execute('SELECT word FROM voc WHERE idWord = {0}'.format(idMain))
		mainWord = d.fetchall()[0][0]
		d.execute('SELECT tagID FROM voc WHERE idWord = {0}'.format(idMain))
		tagM = d.fetchall()[0][0]
		addString = '<a href="/cgi-bin/addGroup.py?idWord={0}&idExcGroup={1}">Добавить</a>'.format(idWord, id)
		otherForms = []
		for w in e.execute("SELECT word FROM voc WHERE idGroup={0}  AND (word != '{1}' OR tagID != {2})".format(id, mainWord, tagM)):
			otherForms.extend(w)
		result += '<tr>'
		result += '<td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td>'.format(id, mainWord, otherForms, addString)
		result += '</tr>'
	result += '</table>'
	conn.commit()
	conn.close()
	return result

form_data = cgi.FieldStorage()
idWord = form_data.getfirst("idWord", "-1")


listGroups = getGroups()
message = "Существующие группы:<br>"

if idWord != '-1':
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	c.execute('SELECT word FROM voc WHERE idWord = {0}'.format(idWord))
	slovo = c.fetchall()[0][0]
	message = 'Вы хотите добавить "<b>{0}</b>".<br><br>Существующие группы:'.format(slovo) 
	conn.commit()
	conn.close()
	if listGroups == '':
		message += "[Список пуст]"	
	else:
		message += listGroups
	message += '<br><a href = "/cgi-bin/addGroup.py?idWord={0}">Создать новую группу</a>'.format(idWord)
else:
	message = "Произошла ошибка передачи данных от клиента к серверу, это окно закроется автоматически"

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Выбор группы для добавления слова</title>
<script>
        function closeW() 
        {  
	
            var t=setTimeout("closeOpenedWindow();", 5000); // закрыть через 2 сек
        }  
        function closeOpenedWindow()
        {  
        	window.close();
        } 
    </script>
	</head>
	<body>""")
print(message)

print('''<br><center><a href="#" onclick="closeOpenedWindow();">[Закрыть окно]</a></center>''')
print("""</body>
	</html>""")
