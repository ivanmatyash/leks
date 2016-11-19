#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3
import nltk



def addInfo(word, tag):
	word = word.lower()
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	
	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())
	
	c.execute("SELECT COUNT(*) FROM voc WHERE word = '{0}' AND tagID = {1}".format(word, sl[tag]))
	t = c.fetchall()[0]
	if t[0] == 0:
		c.execute("INSERT INTO voc (word, amount, tagID) SELECT '{0}', {1}, '{2}' WHERE NOT EXISTS (SELECT * FROM voc WHERE word = '{0}' AND tagID = {2});".format(word, 1, sl[tag]))
	else:
		c.execute("UPDATE voc SET amount = amount + 1 WHERE word = '{0}' AND tagID = {1}".format(word, sl[tag]))

	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
newWord = form_data.getfirst("word", "-1")
tag = form_data.getfirst("tag", "-1")

message ='Слово "{0}" с тегом "{1}" успешно добавлено в словарь. Это окно закроется автоматически.'.format(newWord, tag)

if newWord != '-1' and tag != '-1':
	addInfo(newWord, tag)
else:
	message = "Произошла ошибка передачи данных от клиента к серверу, это окно закроется автоматически"

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
            window.close()  
        } 
    </script>
	</head>
	<body>""")
print(message)
print('''<script type="text/javascript">
closeW()
</script>''')
print("""</body>
	</html>""")
