#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


conn = sqlite3.connect('data/voc.db')
c = conn.cursor()
search_c = conn.cursor()

form_data = cgi.FieldStorage()
sorting = form_data.getfirst("sortedBy", "-1")
find = form_data.getfirst("find", "-1")




def sortedByCount():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY amount'
def sortedByCountReverse():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY amount DESC'
def sortedByWords():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY word'
def sortedByWordsReverse():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY word DESC'
def sortedByTag():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.tagID'
def sortedByTagReverse():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.tagID DESC'
def sortedById():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.idWord'
def sortedByIdReverse():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.idWord DESC'
def sortedByGroup():
	return 'SELECT v.idWord, v.word, v.amount, t.name, t.description, t.translate, t.color, v.idGroup FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.idGroup DESC'

def findWord():
	kor = []
	c.execute("SELECT v.idWord, v.word, v.tagID FROM voc v WHERE v.word LIKE '{0}%'".format(find))
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


print('''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Таблица слов | Словарь</title>
<link rel="stylesheet" type="text/css" href="/style.css"/>
<script type="text/javascript"> 
function destroy(a, b, c)
{
if (confirm('Bы уверены, что хотите удалить слово "' + a + '" c тегом "' + b + '" из словаря? (если это слово является основной формой в группе, то группа тоже будет удалена)')) {
var link1 = "deleteWord.py/?word=" + a + "&tag=" + b + "&amount=" + c;
window.open(link1, '', 'Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');
}
}
function truncate()
{
if (confirm('Bы уверены, что хотите очистить весь словарь?')) 
if (confirm('Вы хорошо подумали? Словарь будет полностью очищен...'))
{
window.open('/cgi-bin/truncate.py', '', 'Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');
}
}
function addWordF(word)
{
location.href='/cgi-bin/voc.py'
var sel = document.getElementById("list_t"); // Получаем наш список
var val = sel.options[sel.selectedIndex].value;
var link1 = "/cgi-bin/addWord.py?word=" + word + "&tag=" + val
window.open(link1, '', 'Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');

}
</script>
</head>
<body>
<a style="position:fixed;padding:20px;" href = "#">Наверх</a>
<div id="container">
  <div id="header"> <a href="/">Таблица слов</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a>&nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/groups.py">Группы</a> &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp;<a> Слов в словаре: {0}</a>&nbsp; &nbsp; &nbsp; <a>Уникальных: {1}</a>'.format(amountOfWords, amountOfUniqueWords))
print(''' </div>
  <div id="mainV">''')


print('<div id="add_block">Добавить новый текст в словарь: ')
print('''<form enctype="multipart/form-data"  method="post" action="addText.py">
        <input type="file" size="5" accept = "text/plain" name="new_file">
        <input type="submit" value="Добавить">
    </form></div>''')

print('''<div id="addw_block"><form method="post">
  Добавить новое слово в словарь:<br>
   <input name="new_word" type="text" size="17">
  <select id="list_t">
	<option value="CC">CC</option> <option value="CD">CD</option> <option>DT</option> <option>EX</option>
<option>FW</option> <option>IN</option> <option>JJ</option> <option>JJR</option>
<option>JJS</option> <option>LS</option> <option>MD</option> <option>NN</option>
<option>NNS</option> <option>NNP</option> <option>NNPS</option> <option>PDT</option>
<option>POS</option> <option>PRP</option> <option>PRP$</option> <option>RB</option>
<option>RBR</option> <option>RBS</option> <option>RP</option> <option>TO</option> <option>UH</option> <option>VB</option> <option>VBD</option> <option>VBG</option> <option>VBN</option> <option>VBP</option> <option>VBZ</option> <option>WDT</option> <option>WP</option> <option>WP$</option> <option>WRB</option>
	</select>
<input onclick="addWordF(new_word.value)" type="submit" value="Send"></form>
  </div>''')



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
str1 = '<a href = "voc.py?sortedBy=words">▲</a>'
str2 = '<a href = "voc.py?sortedBy=wordsReverse">▼</a>'
str3 = '<a href = "voc.py?sortedBy=count">▲</a>'
str4 = '<a href = "voc.py?sortedBy=countReverse">▼</a>'
str5 = '<a href = "voc.py?sortedBy=tag">▲</a>'
str6 = '<a href = "voc.py?sortedBy=tagReverse">▼</a>'
str7 = '<a href = "voc.py?sortedBy=id">▲</a>'
str8 = '<a href = "voc.py?sortedBy=idReverse">▼</a>'
str9 = '<a href = "voc.py?sortedBy=group">▼</a>'
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
elif sorting == 'group':
	zapros = sortedByGroup()
else:
	zapros = sortedByWords()


print('<table width = 100%>')
print("<tr><td><b>#{6}{7}</b></td> <td><b>Word {0}{1}</b></td> <td><b>Tag{2}{3}</b></td> <td><b>Description</b></td> <td><b>Russian description</b></td> <td><b>Amount{4}{5}</b></td> <td><b>Edit</b></td> <td><b>Delete</b></td><td><b>Group{8}</b></td></tr>".format(str1, str2, str5, str6, str3, str4, str7, str8, str9))

for (idWord, word, amount, tag, en_d, ru_d, color, idGroup) in c.execute(zapros):
	edit_str = '<a href="javascript:void(0)" ONCLICK="window.open(' + "'editWord.py/?word={0}&tag={1}&amount=		{2}','','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');".format(word, tag, amount) + '">[edit]</a>'
	remove_str = '<a onclick="destroy(\'{0}\', \'{1}\', {2});" href = "javascript:void(0)"><center>[x]</center></a>'.format(word, tag, amount)
	idLink = '<a href="#{0}" name="{0}">{0}</a>'.format(idWord)
	

	if idGroup == -1:
		idGroup = '<a href="javascript:void(0)" ONCLICK="window.open(' + "'chooseGroup.py/?idWord={0}','','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');".format(idWord) + '">[+]</a>'.format(idWord)
	else:
		f = conn.cursor()
		mainWord = ''
		otherWords = []
		f.execute("SELECT idMain FROM groups WHERE id = {0}".format(idGroup))
		indMain = f.fetchall()[0][0]
		f.execute("SELECT word FROM voc WHERE idWord = {0}".format(indMain))
		mainWord = f.fetchall()[0][0]
		for wordM in f.execute("SELECT word FROM voc WHERE idGroup = {0} AND word != '{1}'".format(idGroup, mainWord)):
			otherWords.extend(wordM)
		if otherWords:
			podskazka = "Main form: {0}, other forms: {1}".format(mainWord, otherWords)
		else:
			podskazka = "Main form: {0}, other forms: NO".format(mainWord)
		idGroup = '<a title="{0}" href="javascript:void(0)" ONCLICK="window.open('.format(podskazka) + "'getGroup.py/?idGroup={0}','','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');".format(idGroup) + '">{0}</a>'.format(idGroup)



	print('<tr style="background:#{0}">'.format("F5F5F5"))
	print('<td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td> <td>{4}</td> <td>{5}</td> <td>{6}</td> <td>{7}</td><td><center>{8}</center></td>'.format(idLink, word, tag, en_d, ru_d, amount, edit_str, remove_str, idGroup))
	print('</tr>')
print('</table>')
conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
