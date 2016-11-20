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
word = form_data.getfirst("word", "-1")
tag = form_data.getfirst("tag", "-1")
amount = form_data.getfirst("amount", "-1")

message ='Вы находитесь на странице редактирования слова "{0}" с тегом "{1}".'.format(word, tag)
form_str = ''

if word != '-1' and tag != '-1' and amount != '-1':
	select_str =  '<select name="tag">\
	<option>CC</option> <option>CD</option> <option>DT</option> <option>EX</option>\
	<option>FW</option> <option>IN</option> <option>JJ</option> <option>JJR</option>\
	<option>JJS</option> <option>LS</option> <option>MD</option> <option>NN</option>\
	<option>NNS</option> <option>NNP</option> <option>NNPS</option> <option>PDT</option>\
	<option>POS</option> <option>PRP</option> <option>PRP$</option> <option>RB</option>\
	<option>RBR</option> <option>RBS</option> <option>RP</option> <option>TO</option> \
	<option>UH</option> <option>VB</option> <option>VBD</option> <option>VBG</option> \
	<option>VBN</option> <option>VBP</option> <option>VBZ</option> <option>WDT</option>\
	<option>WP</option> <option>WP$</option> <option>WRB</option>\
	</select>'.format(tag)
	select_str = select_str.replace("<option>"+tag+"</option>", "<option selected>"+tag+"</option>")


	form_str = '<table>\
	<form method="post" action="/cgi-bin/editWordOk.py?lastWord={0}&lastTag={3}&lastAmount={2}">\
	<tr><td><b>Слово:</b></td> <td><input name = "word"type="text" size="12" value="{0}"></td></tr>\
	<tr><td><b>Тег:</b></td> <td>{1}</td></tr>\
	<tr><td><b>Количество:</b></td> <td><input name="amount" type="text" size="6" value = "{2}"></td></tr>\
	<tr><td><b>Отправить:</b></td><td><input type="submit" value="Send"></td></tr>'.format(word, select_str, amount, tag) + '</table>'
else:
	message = "Произошла ошибка передачи данных от клиента к серверу."

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Изменение слова в словаре</title>
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
print(form_str)
print('<br><center><a onclick="closeOpenedWindow();"href = "/cgi-bin/voc.py">[Закрыть это окно]</a></center>')
print("""</body>
	</html>""")
