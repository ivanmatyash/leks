#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3


conn = sqlite3.connect('/tmp/voc.db')
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

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Словарь</title>
	</head>
	<body>""")
print("<h1>Your Dictionary:</h1>")
print("Sorted by:")
print('<a href = "voc.py?sortedBy=words">words↓</a>')
print('<a href = "voc.py?sortedBy=wordsReverse">words↑</a>')
print('<a href = "voc.py?sortedBy=count">count↓</a>')
print('<a href = "voc.py?sortedBy=countReverse">count↑</a>')
print('<a href = "voc.py?sortedBy=tag">tag↓</a>')
print('<a href = "voc.py?sortedBy=tagReverse">tag↑</a>')

print('<br><br>Добавить новый текст в словарь: ')
print('''<form enctype="multipart/form-data"  method="post" action="addText.py">
        <input type="file" accept = "text/plain" name="new_file">
        <input type="submit" value="Send">
    </form><br>''')

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

print('<table>')
print("<tr><td><b>Word</b></td> <td><b>Tag</b></td> <td><b>Description</b></td> <td><b>Rus. description</b></td> <td><b>Amount</b></td> <td><b>Delete</b></td></tr>")
for word, amount, tag, en_d, ru_d, color in c.execute(zapros):
	remove_str = '<a href = "delete.py/?DEL=1&ff=2">del</a>'
	print('<tr style="background:#{0}">'.format(color))
	print('<td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td> <td>{4}</td> <td>{5}</td>'.format(word, tag, en_d, ru_d, amount, remove_str))
	print('</tr>')
print('</table>')

conn.close()
print("""</body>
	</html>""")
