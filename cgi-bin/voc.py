#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3


conn = sqlite3.connect('data/voc.db')
c = conn.cursor()

form_data = cgi.FieldStorage()
sorting = form_data.getfirst("sortedBy", "-1")





def sortedByCount():
	return 'SELECT v.word, v.amount, t.name, t.description, t.translate, t.color FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY amount'
def sortedByCountReverse():
	return 'SELECT v.word, v.amount, t.name, t.description, t.translate, t.color FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY amount DESC'
def sortedByWords():
	return 'SELECT v.word, v.amount, t.name, t.description, t.translate, t.color FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY word'
def sortedByWordsReverse():
	return 'SELECT v.word, v.amount, t.name, t.description, t.translate, t.color FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY word DESC'
def sortedByTag():
	return 'SELECT v.word, v.amount, t.name, t.description, t.translate, t.color FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.tagID'
def sortedByTagReverse():
	return 'SELECT v.word, v.amount, t.name, t.description, t.translate, t.color FROM voc v INNER JOIN tags t ON v.tagID = t.id ORDER BY v.tagID DESC'

c.execute("SELECT SUM(amount) FROM  voc")
amountOfWords = c.fetchall()[0][0]
c.execute("SELECT COUNT(*) FROM voc")
amountOfUniqueWords = c.fetchall()[0][0]


print('''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Главная | Словарь</title>
<link rel="stylesheet" type="text/css" href="/style.css"/>
<script type="text/javascript"> 
function destroy(a, b, c)
{
if (confirm('Bы уверены, что хотите удалить слово "' + a + '" c тегом "' + b + '" из словаря?')) {
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
var sel = document.getElementById("list_t"); // Получаем наш список
var val = sel.options[sel.selectedIndex].value;
var link1 = "/cgi-bin/addWord.py?word=" + word + "&tag=" + val
window.open(link1, '', 'Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');
}
</script>
</head>
<body>
<div id="container">
  <div id="header"> <a href="/">My dictionary</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a>&nbsp; &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp; &nbsp;<a> Слов в словаре: {0}</a> &nbsp; &nbsp; &nbsp; &nbsp; <a>Уникальных слов: {1}</a>'.format(amountOfWords, amountOfUniqueWords))
print(''' </div>
  <div id="mainV">''')


print('<div id="add_block">Добавить новый текст в словарь: ')
print('''<form enctype="multipart/form-data"  method="post" action="addText.py">
        <input type="file" accept = "text/plain" name="new_file">
        <input type="submit" value="Send">
    </form></div>''')

print('''<div id="addw_block"><form method="post">
  Добавить новое слово в словарь:<br>
   <input name="new_word" type="text" size="20">
  <select id="list_t">
	<option value="CC">CC</option> <option value="CD">CD</option> <option>DT</option> <option>EX</option>
<option>FW</option> <option>IN</option> <option>JJ</option> <option>JJR</option>
<option>JJS</option> <option>LS</option> <option>MD</option> <option>NN</option>
<option>NNS</option> <option>NNP</option> <option>NNPS</option> <option>PDT</option>
<option>POS</option> <option>PRP</option> <option>PRP$</option> <option>RB</option>
<option>RBR</option> <option>RBS</option> <option>RP</option> <option>TO</option> <option>UH</option> <option>VB</option> <option>VBD</option> <option>VBG</option> <option>VBN</option> <option>VBP</option> <option>VBZ</option> <option>WDT</option> <option>WP</option> <option>WP$</option> <option>WRB</option>
	</select>
<input onclick="addWordF(new_word.value)" type="submit" value="Send"></form>
  </div><br><br>''')


str1 = '<a href = "voc.py?sortedBy=words">▲</a>'
str2 = '<a href = "voc.py?sortedBy=wordsReverse">▼</a>'
str3 = '<a href = "voc.py?sortedBy=count">▲</a>'
str4 = '<a href = "voc.py?sortedBy=countReverse">▼</a>'
str5 = '<a href = "voc.py?sortedBy=tag">▲</a>'
str6 = '<a href = "voc.py?sortedBy=tagReverse">▼</a>'
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
else:
	zapros = sortedByWords()


print('<table width = 100%>')
print("<tr><td><b>#</b></td> <td><b>Word {0}{1}</b></td> <td><b>Tag{2}{3}</b></td> <td><b>Description</b></td> <td><b>Russian description</b></td> <td><b>Amount{4}{5}</b></td> <td><b>Edit</b></td> <td><b>Delete</b></td></tr>".format(str1, str2, str5, str6, str3, str4))
ind = 1
for word, amount, tag, en_d, ru_d, color in c.execute(zapros):

	edit_str = '<a href="javascript:void(0)" ONCLICK="window.open(' + "'editWord.py/?word={0}&tag={1}&amount={2}','','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=0,Width=550,Height=400');".format(word, tag, amount) + '">[edit]</a>'

	remove_str = '<a onclick="destroy(\'{0}\', \'{1}\', {2});" href = "javascript:void(0)"><center>[x]</center></a>'.format(word, tag, amount)
	print('<tr style="background:#{0}">'.format(color))
	print('<td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td> <td>{4}</td> <td>{5}</td> <td>{6}</td> <td>{7}</td>'.format(ind, word, tag, en_d, ru_d, amount, edit_str, remove_str))
	print('</tr>')
	ind += 1
print('</table>')
conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
