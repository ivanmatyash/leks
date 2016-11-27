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
function remove(a, b)
	{
		if (confirm('Bы уверены, что хотите удалить слово #' + a + ' из группы #' + b + '?')) 
		{
			var link1 = '/cgi-bin/deleteFromGroup.py/?idWord=' + a + '&idGroup=' + b;
			window.open(link1,'','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');
			
		}
	}
</script>
</head>
<body>
<div id="container">
  <div id="header"> <a href="/">Группы слов</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/groups.py">Группы</a> &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/text.py">Текст</a> &nbsp; &nbsp; &nbsp;<a> Слов в словаре: {0}</a>  &nbsp; &nbsp; &nbsp; <a>Уникальных: {1}</a>'.format(amountOfWords, amountOfUniqueWords))
print(''' </div>
  <div id="mainV">''')

zapros = ('''SELECT * FROM groups''')



print('<table width = 100%>')
print("<tr><td><b>№ группы</b></td> <td><b>Основная форма</b></td> <td><b>Другие формы</b></td></tr>")
for idGroup, idMain in d.execute(zapros):
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
	
	idStr = '<a href="javascript:void(0)" ONCLICK="window.open(' + "'getGroup.py/?idGroup={0}','','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');".format(idGroup) + '">{0}</a>'.format(idGroup)
	print('<tr style="background:#{0}">'.format("F5F5F5"))
	print('<td><center>{0}</center></td> <td>{1}</td> <td>{2}</td>'.format(idStr, mainWord, resStr))
	print('</tr>')
print('</table>')

conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
