#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


conn = sqlite3.connect('data/voc.db')
c = conn.cursor()
d = conn.cursor()
search_c = conn.cursor()

form_data = cgi.FieldStorage()
sorting = form_data.getfirst("sortedBy", "-1")
find = form_data.getfirst("find", "-1")


c.execute("DROP TABLE IF EXISTS voc_text")
c.execute('''CREATE TABLE IF NOT EXISTS voc_text (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, amount INTEGER DEFAULT 1, tagID INTEGER)''')
list1 = []
for word, tagID in c.execute("SELECT word, tagID FROM text"):
	list1.append((word.lower(), tagID))

dic = dict.fromkeys(list1, 0)
for item in list1:
	dic[item] +=1

for item in dic:
	c.execute("INSERT INTO voc_text (word, tagID, amount) VALUES('{0}', {1}, {2})".format(item[0], item[1], dic[item]))
	conn.commit()

def sortedByCount():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY amount'
def sortedByCountReverse():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY amount DESC'
def sortedByWords():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY word'
def sortedByWordsReverse():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY word DESC'
def sortedByTag():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.tagID'
def sortedByTagReverse():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.tagID DESC'
def sortedById():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.id'
def sortedByIdReverse():
	return 'SELECT v.id, v.word, v.amount, t.id, t.name, t.description, t.translate FROM voc_text v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.id DESC'


def findWord():
	kor = []
	c.execute("SELECT v.id, v.word, v.tagID FROM voc_text v WHERE v.word LIKE '{0}%'".format(find))
	temp1 = c.fetchall()
	for first, second, third in temp1:
		c.execute('SELECT name FROM tags WHERE id = {0}'.format(third))
		temp = c.fetchall()
		for a in temp:
			kor.append((first, second, third, a))
	return  kor



if find != '-1':
	global list_r
	list_r = findWord()
else:
	global list_r
	list_r = []


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
	if tagID1 == 37:
		continue
	d.execute("SELECT tagID FROM text WHERE id = {0}".format(item + 1))
	tagID2 = d.fetchall()[0][0]
	if tagID2 == 37 and (item + 1) == amountWordInText:
		break
	if tagID2 == 37:
		d.execute("SELECT tagID FROM text WHERE id = {0}".format(item + 2))
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




#БЛОК ПОИСКА
print('''<div id="search_block"><form enctype="multipart/form-data"  method="post" action="">
        <input type="text" value="" size="10" accept = "text/plain" name="find">
        <input type="submit" value="Поиск">
    </form></div>''')
print('<div id="search_results">')
if list_r:
	for item in list_r:
		print ('<a href="#{0}">{1}({2})</a>'.format(item[0],item[1],item[3][0]))
	print("<br>")
elif find != '-1':
	print('Не найдено слов по запросу "{0}"<br>'.format(find))
print('</div>')



#ВЫБОР СОРТИРОВКИ
str1 = '<a href = "stat_text.py?sortedBy=words">▲</a>'
str2 = '<a href = "stat_text.py?sortedBy=wordsReverse">▼</a>'
str3 = '<a href = "stat_text.py?sortedBy=count">▲</a>'
str4 = '<a href = "stat_text.py?sortedBy=countReverse">▼</a>'
str5 = '<a href = "stat_text.py?sortedBy=tag">▲</a>'
str6 = '<a href = "stat_text.py?sortedBy=tagReverse">▼</a>'
str7 = '<a href = "stat_text.py?sortedBy=id">▲</a>'
str8 = '<a href = "stat_text.py?sortedBy=idReverse">▼</a>'
zapros = ''
if sorting == 'wordsReverse':
	zapros = sortedByWordsReverse()
elif sorting == 'count':
	zapros = sortedByCount()
elif sorting == 'tag':
	zapros = sortedByTag()
elif sorting == 'tagReverse':
	zapros = sortedByTagReverse();
elif sorting == 'countReverse':
	zapros = sortedByCountReverse()
elif sorting == 'id':
	zapros = sortedById()
elif sorting == 'idReverse':
	zapros = sortedByIdReverse()
else:
	zapros = sortedByWords()

print('<br><hr><br> <center><h1>По кодам</h1></center><br>')
zapros1 = ('''SELECT * FROM tags''')
print('<table width = 100%>')
print("<tr><td><b>№</b></td> <td><b>Тег</b></td> <td><b>Описание</b></td> <td><b>Русское описание</b></td><td><b>Кол-во:</b></td></tr>")
for id, name, description, translate, color in c.execute(zapros1):
	d.execute("SELECT COUNT(*) FROM text WHERE tagID={0}".format(id))
	amountT = d.fetchall()[0][0]
	if amountT == 0:
		continue
	print('<tr style="background:#{0}">'.format("F5F5F5"))
	print('<td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td> <td>{4}</td>'.format(id, name, description, translate, amountT))
	print('</tr>')
print('</table>')

print('<hr><br> <center><h1>По паре слово-код</h1></center><br>')
print('<table width = 100%>')
print("<tr><td><b>#{6}{7}</b></td> <td><b>Word {0}{1}</b></td> <td><b>Tag{2}{3}</b></td> <td><b>Description</b></td> <td><b>Russian description</b></td> <td><b>Amount{4}{5}</b></td> <td><b>Amount (in dict)</b></td></tr>".format(str1, str2, str5, str6, str3, str4, str7, str8))

for (idWord, word, amount, idTag1, tag, en_d, ru_d) in c.execute(zapros):
	d.execute("SELECT amount FROM voc WHERE word = '{0}' AND tagID = {1}".format(word, idTag1))
	amountInDict = d.fetchall()
	if amountInDict:
		amountInDict = amountInDict[0][0]
	else:
		amountInDict = 0
	colorTR = "F5F5F5"
	if amount != amountInDict:
		colorTR = "FFA07A"
	idLink = '<a href="#{0}" name="{0}">{0}</a>'.format(idWord)
	print('<tr style="background:#{0}">'.format(colorTR))
	print('<td>{0}</td> <td>{1}</td> <td><center>{2}</center></td> <td>{3}</td> <td>{4}</td> <td><center>{5}</center></td><td><center>{6}</center></td>'.format(idLink, word, tag, en_d, ru_d, amount, amountInDict))
	print('</tr>')
print('</table>')


print('<hr><br> <center><h1>По парам кодов</h1></center><br>')
print('<table width = 100%>')
print("<tr><td><b>Последовательность кодов</b></td> <td><b>Первый код</b></td> <td><b>Второй код</b></td><td><b>Количество</b></td></tr>")

for temp in dic_main:
	c.execute("SELECT name, translate FROM tags WHERE id = {0}".format(temp[0]))
	res = c.fetchall()[0]
	tag1 = res[0]
	tag1D = res[1]
	c.execute("SELECT name, translate FROM tags WHERE id = {0}".format(temp[1]))
	res = c.fetchall()[0]
	tag2 = res[0]
	tag2D = res[1]
	
	print('<tr style="background:#{0}">'.format("F5F5F5"))
	print('<td>{0} / {1}</td> <td>{2}</td> <td>{3}</td> <td><center>{4}</center></td>'.format(tag1, tag2, tag1D, tag2D, dic_main[temp]))
	print('</tr>')
print('</table>')







conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
