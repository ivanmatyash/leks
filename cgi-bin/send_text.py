#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3

def isZnakPrep(it):
	return it in ',.!?()[]'

form = cgi.FieldStorage()
file_name = form["filenameText"]


if file_name.filename:
	fn = os.path.basename(file_name.filename)
	open("data/" + fn, 'wb').write(file_name.file.read())
	file1 = open("data/" + fn, 'rt')
	textSTR = file1.read()

slova = textSTR.split()
words = []
for item in slova:
	if isZnakPrep(item[-1]):
		words.append(item[0:-1])
		words.append(item[-1])
	else:
		words.append(item)

conn = sqlite3.connect('data/voc.db')
c = conn.cursor()
d = conn.cursor()

c.execute("SELECT SUM(amount) FROM  voc")
amountOfWords = c.fetchall()[0][0]
c.execute("SELECT COUNT(*) FROM voc")
amountOfUniqueWords = c.fetchall()[0][0]

c.execute("DELETE FROM text")


for w in words:
	if w.isdigit():
		c.execute("INSERT INTO text (word,tagID) VALUES(\'{0}\', 38)".format(w))
		conn.commit()
		continue
	if isZnakPrep(w):
		c.execute("INSERT INTO text (word, tagID) VALUES(\'{0}\', 37)".format(w))
		conn.commit()
		continue
	c.execute("SELECT COUNT(*) FROM voc WHERE word = \'{0}\'".format(w.lower()))
	amount = c.fetchall()[0][0]
	if amount == 0:
		c.execute("INSERT INTO text (word, tagID, color) VALUES(\'{0}\', 36, 'FF4500')".format(w))
		conn.commit()
	elif amount == 1:
		c.execute("SELECT tagID FROM voc WHERE word = \'{0}\'".format(w.lower()))
		tagid = c.fetchall()[0][0]
		c.execute("INSERT INTO text (word, tagID, color) VALUES(\'{0}\', {1}, '00CD00')".format(w, tagid))
		conn.commit()
	elif amount > 1:
		c.execute("SELECT tagID FROM voc WHERE word = \'{0}\' AND amount=(SELECT MAX(amount) FROM voc WHERE word = \'{0}\') LIMIT 1".format(w.lower()))
		tagid = c.fetchall()[0][0]
		c.execute("INSERT INTO text (word, tagID, color) VALUES(\'{0}\', {1}, 'EEC900')".format(w, tagid))
		conn.commit()
		
result = '<form method="post" action="updateText.py">'
for id, WORD, TAG, COLOR in c.execute("SELECT id, word, tagID, color FROM text"):
	d.execute("SELECT name, translate FROM tags WHERE id = {0}".format(TAG))
	listRes = d.fetchall()[0]
	tagTXT = listRes[0]
	translateTXT = listRes[1]
	massID=[]
	listItog = []
	if COLOR == 'FF4500':
		selectStr = "select{0}".format(id)
		strOpt = '<select name="{0}">'.format(selectStr)
		strOpt +='''<option value="CC">CC</option> <option value="CD">CD</option> <option>DT</option> <option>EX</option>
<option>FW</option> <option>IN</option> <option>JJ</option> <option>JJR</option>
<option>JJS</option> <option>LS</option> <option>MD</option> <option>NN</option>
<option>NNS</option> <option>NNP</option> <option>NNPS</option> <option>PDT</option>
<option>POS</option> <option>PRP</option> <option>PRP$</option> <option>RB</option>
<option>RBR</option> <option>RBS</option> <option>RP</option> <option>TO</option> <option>UH</option> <option>VB</option> <option>VBD</option> <option>VBG</option> <option>VBN</option> <option>VBP</option> <option>VBZ</option> <option>WDT</option> <option>WP</option> <option>WP$</option> <option>WRB</option>'''
		strOpt += "</select>"
		result += '<font size = "4" color = "#{3}"><a title = "({1}, {2})" onclick="">{0}({4}) </a></font>'.format(WORD, tagTXT, translateTXT, COLOR, strOpt)
	elif COLOR == 'EEC900':
		d.execute("SELECT t.name FROM tags t INNER JOIN voc v ON v.tagID = t.id WHERE word = '{0}'".format(WORD.lower()))
		massID = d.fetchall()
		selectStr = "select{0}".format(id)
		strOpt = '<select name="{0}">'.format(selectStr)
		for i1 in massID:
			strOpt += "<option>{0}</option>".format(i1[0])
		strOpt += "</select>"
		
		result += '<font size = "4" color = "#{3}"><a title = "({1}, {2})" onclick="">{0}({4}) </a></font>'.format(WORD, tagTXT, translateTXT, COLOR, strOpt)
	else:
		result += '<font size = "4" color = "#{3}"><a title = "({1}, {2})" onclick="">{0} </a></font>'.format(WORD, tagTXT, translateTXT, COLOR)

result += '<br><br><input type="submit" value="Отправить"></form>'
print('''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Отправить текст | Словарь</title>
<link rel="stylesheet" type="text/css" href="/style.css"/>

</head>
<body>
<div id="container">
  <div id="header"> <a href="/">Отправить текст</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/groups.py">Группы</a> &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/text.py" >Текст</a> &nbsp; &nbsp; &nbsp;<a> Слов в словаре: {0}</a>  &nbsp; &nbsp; &nbsp; <a>Уникальных: {1}</a>'.format(amountOfWords, amountOfUniqueWords))
print(''' </div>
  <div id="mainV">''')

print(result)
conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
