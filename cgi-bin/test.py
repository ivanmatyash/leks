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

c.execute("SELECT SUM(amount) FROM  voc_text")
amountText = c.fetchall()[0][0]
c.execute("SELECT COUNT(*) FROM voc_text")
amountUText = c.fetchall()[0][0]

c.execute("SELECT COUNT(*) FROM text")
amountWordInText= c.fetchall()[0][0]


dic_main = {}

for item in range(1,amountWordInText):
	c.execute("SELECT tagID FROM text WHERE id = {0}".format(item))
	tagID1 = c.fetchall()[0][0]
	d.execute("SELECT tagID FROM text WHERE id = {0}".format(item + 1))
	tagID2 = d.fetchall()[0][0]
	if (tagID1, tagID2) in dic_main:
		dic_main[(tagID1, tagID2)] += 1
	else:
		dic_main[(tagID1, tagID2)] = 1

print('''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Статистика по тексту | Словарь</title>
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
<a style="position:fixed;padding:20px;" href = "#">Наверх</a>
<div id="container">
  <div id="header"> <a href="/">Статистика по тексту</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a>&nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/groups.py">Группы</a> &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/text.py">Текст</a>&nbsp; &nbsp; &nbsp; <a> Слов в словаре: {0}</a>&nbsp; &nbsp; &nbsp; <a>Уникальных: {1}</a> &nbsp; &nbsp; &nbsp; <a>Слов в тексте: {2}</a> &nbsp; &nbsp; &nbsp; <a>Уникальных: {3}</a>'.format(amountOfWords, amountOfUniqueWords, amountText, amountUText))
print(''' </div>
  <div id="mainV">''')





print (dic_main)
conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
