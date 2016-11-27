#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


conn = sqlite3.connect('data/voc.db')
c = conn.cursor()
d = conn.cursor()

c.execute("SELECT SUM(amount) FROM  voc")
amountOfWords = c.fetchall()[0][0]
c.execute("SELECT COUNT(*) FROM voc")
amountOfUniqueWords = c.fetchall()[0][0]

form_data = cgi.FieldStorage()

c.execute("SELECT id FROM text WHERE tagID = 36")
ids = c.fetchall()
listIds = []
for item in ids:
	listIds.append(item[0])
c.execute("SELECT word FROM voc GROUP BY word HAVING COUNT(word) > 1")
ids1 = c.fetchall()
idsList = []


for item in listIds:
	tag = form_data.getfirst("select{0}".format(item), "-1")
	c.execute("SELECT id FROM tags WHERE name = '{0}'".format(tag))
	itTag = c.fetchall()[0][0]
	c.execute("UPDATE text SET tagID = {0} WHERE id = {1}".format(itTag, item))
	conn.commit()

for item in ids1:
	c.execute("SELECT COUNT(*) FROM text WHERE LOWER(word) = '{0}'".format(item[0]))
	am = c.fetchall()[0][0]
	if am != 0:
		c.execute("SELECT id FROM text WHERE LOWER(word) ='{0}'".format(item[0]))
		listPovtor = c.fetchall()
		for item1 in listPovtor:
			tag = form_data.getfirst("select{0}".format(item1[0]), "-1")
			c.execute("SELECT id FROM tags WHERE name = '{0}'".format(tag))
			itTag = c.fetchall()[0][0]
			c.execute("UPDATE text SET tagID = {0} WHERE id = {1}".format(itTag, item1[0]))
			conn.commit()


result = ""
for word, nameTag, translate in c.execute("SELECT t.word, tag.name, tag.translate FROM text t INNER JOIN tags tag ON tag.id = t.tagID"):
	result += '<a title="{0},{1}" onclick="">{2} </a>'.format(nameTag, translate, word)


print('''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Готовый текст | Словарь</title>
<link rel="stylesheet" type="text/css" href="/style.css"/>

<script type="text/javascript"> 	
function truncate()
{
if (confirm('Bы уверены, что хотите очистить весь словарь?')) 
if (confirm('Вы хорошо подумали? Словарь будет полностью очищен...'))
{
window.open('/cgi-bin/text.py', '', 'Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');
}
}

</script>
</head>
<body>
<div id="container">
  <div id="header"> <a href="/">Готовый текст</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/groups.py">Группы</a> &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/text.py" >Текст</a> &nbsp; &nbsp; &nbsp;<a> Слов в словаре: {0}</a>  &nbsp; &nbsp; &nbsp; <a>Уникальных: {1}</a>'.format(amountOfWords, amountOfUniqueWords))
print(''' </div>
  <div id="mainV">''')

print(result)
print('<br><br>	<a href="/cgi-bin/stat_text.py" target="_blank">Получить статистику по тексту</a>')
conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
