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

print('''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Группы слов | Словарь</title>
<link rel="stylesheet" type="text/css" href="/style.css"/>
<script type="text/javascript"> 	
function truncate()
{
if (confirm('Bы уверены, что хотите очистить весь словарь?')) 
if (confirm('Вы хорошо подумали? Словарь будет полностью очищен...'))
{
window.open('/cgi-bin/truncate.py', '', 'Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');
}
}
</script>
</head>
<body>
<div id="container">
  <div id="header"> <a href="/">Группы слов</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/groups.py">Группы</a> &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp;<a> Слов в словаре: {0}</a>  &nbsp; &nbsp; &nbsp; <a>Уникальных: {1}</a>'.format(amountOfWords, amountOfUniqueWords))
print(''' </div>
  <div id="mainV">''')

zapros = ('''SELECT * FROM groups''')

print('<table width = 100%>')
print("<tr><td><b>№ группы</b></td> <td><b>Основная форма</b></td> <td><b>Другие формы</b></td></tr>")
for id, idMain in c.execute(zapros):
	d.execute('SELECT word FROM voc WHERE idWord = {0}'.format(idMain))
	mainW = d.fetchall()[0][0]
	otherWords = []
	for word in d.execute("SELECT word FROM voc WHERE idGroup = {0} AND word != '{1}'".format(id, mainW)):
		otherWords.extend(word)
	idStr = '<a href="javascript:void(0)" ONCLICK="window.open(' + "'getGroup.py/?idGroup={0}','','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');".format(id) + '">{0}</a>'.format(id)
	print('<tr style="background:#{0}">'.format("F5F5F5"))
	print('<td>{0}</td> <td>{1}</td> <td>{2}</td>'.format(idStr, mainW, otherWords))
	print('</tr>')
print('</table>')

conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
