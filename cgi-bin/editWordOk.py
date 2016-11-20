#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3

form_data = cgi.FieldStorage()
word = form_data.getfirst("word", "-1")
tag = form_data.getfirst("tag", "-1")
amount = form_data.getfirst("amount", "-1")
lastWord = form_data.getfirst("lastWord", "-1")
lastTag = form_data.getfirst("lastTag", "-1")
lastAmount = form_data.getfirst("lastAmount", "-1")


def editWord():
	word1 = word.lower()
	lastAmount1 = int(lastAmount)
	amount1 = int(amount)
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	
	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())
	
	c.execute("DELETE FROM voc WHERE word = '{0}' AND tagID = {1} AND amount = {2}".format(lastWord, sl[lastTag], lastAmount1))

	c.execute("SELECT COUNT(*) FROM voc WHERE word = '{0}' AND tagID = {1}".format(word1, sl[tag]))
	t = c.fetchall()[0]
	if t[0] == 0:
		c.execute("INSERT INTO voc (word, amount, tagID) SELECT '{0}', {1}, {2} WHERE NOT EXISTS (SELECT * FROM voc WHERE word = '{0}' AND tagID = {2});".format(word, amount1, sl[tag]))
	else:
		c.execute("UPDATE voc SET amount = amount + {2} WHERE word = '{0}' AND tagID = {1}".format(word, sl[tag], amount1))
	conn.commit()
	conn.close()


message ='<h2>Замена слова прошла успешно.</h2><b><h3>Информация о старом слове:</h3></b> \
	<table>\
	<tr><td><b>Слово: </b></td> <td>{0}</td></tr>\
	<tr><td><b>Тег: </b></td> <td>{1}</td></tr>\
	<tr><td><b>Количество: </b></td> <td> {2}</td></tr>\
	</table>\
	<h3>Информация о новом слове: </h3>\
	<table>\
	<tr><td><b>Слово: </b></td> <td>{3}</td></tr>\
	<tr><td><b>Тег: </b></td> <td>{4}</td></tr>\
	<tr><td><b>Количество: </b></td> <td> {5}</td></tr>\
	</table>'.format(lastWord, lastTag, lastAmount, word, tag, amount)

if word != '-1' and tag != '-1' and amount != '-1' and lastWord != '-1' and lastTag != '-1' and lastAmount != '-1':
	editWord()

else:
	message = "<h2>Произошла ошибка передачи данных от клиента к серверу. Попробуйте еще раз.</h2>"

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Добавление нового слова в словарь</title>
<script>
        function closeW() 
        {  
	
            var t=setTimeout("closeOpenedWindow();", 3000); // закрыть через 2 сек
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
print('''<br><center><a href="#" onclick="closeOpenedWindow();">[Закрыть отчет]</a></center>''')
print("""</body>
	</html>""")
