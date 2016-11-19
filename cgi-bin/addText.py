#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3
import nltk



def addInfo(filename):
	conn = sqlite3.connect('/tmp/voc.db')
	c = conn.cursor()
	inpFile = open("/tmp/" + filename, "rt")
		
	tokens = []
	for inputStr in inpFile:
		inputStr = inputStr.lower()
		tokens.extend(nltk.word_tokenize(inputStr))
	list_rm = []
	for i in tokens:
		if not i.isalpha():
			list_rm.append(i)				
	for i in list_rm:
		tokens.remove(i)
	tags = []
	tags.extend(nltk.pos_tag(tokens))
	inpFile.close()

	dic = dict.fromkeys(tags, 0)
	for item in tags:
		dic[item] += 1

	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())
	for item in dic:
		#c.execute('INSERT INTO voc (word, amount, tagID) VALUES ("{0}","{1}", "{2}")'.format(item[0], dic[item], sl[item[1]]))
		c.execute("INSERT INTO voc (word, amount, tagID) SELECT '{0}', {1}, '{2}' WHERE NOT EXISTS (SELECT * FROM voc WHERE word = '{0}' AND tagID = {2});".format(item[0], dic[item], sl[item[1]]))
	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
file_name = form_data["new_file"]


if file_name.filename:
	fn = os.path.basename(file_name.filename)
	open('/tmp/' + fn, 'wb').write(file_name.file.read())
	addInfo(fn)



print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Добавление нового текста в словарь</title>
	</head>
	<body>""")


print("lol")

print("""</body>
	</html>""")
