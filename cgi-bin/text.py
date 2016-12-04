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
<title>Раскрасить текст | Словарь</title>
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
  <div id="header"> <a href="/">Раскрасить текст</a> </div>
  <div id="menu"> ''')

print('<a href="/">Главная</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/voc.py">Словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/stat.py">Статистика</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/groups.py">Группы</a> &nbsp; &nbsp; &nbsp; <a onclick="truncate();" href="javascript:void(0)" >Очистить словарь</a> &nbsp; &nbsp; &nbsp; <a href="/cgi-bin/text.py" >Текст</a> &nbsp; &nbsp; &nbsp;<a> Слов в словаре: {0}</a>  &nbsp; &nbsp; &nbsp; <a>Уникальных: {1}</a>'.format(amountOfWords, amountOfUniqueWords))
print(''' </div>
<div id="sidebar">
 <img src = "/img/text.png">
  </div>
  <div id="main">
Вы находитесь на странице, куда можно загрузить свой текст. Система автоматически предложит разбиение вашего текста по частям речи.


<h2>Как это работает?</h2>
На предыдущих шагах вы создали словарь, куда внесли много слов. Теперь вы подаёте на вход текст. В этом тексте каждое слово проверяется на принадлежность к вашему словарю. Если слово найдено в словаре - ему приписывается тег. Если тегов у такого слова несколько - вам предлагается выбрать из них один. Если такого слова в словаре нет, вам предлагается самостоятельно назначить слову тег. <a href="/cgi-bin/stat_text.py">Статистика прошлых текстов</a>.

<h2>Раскрасить текст</h2>
''')


print('''
<form enctype="multipart/form-data"  method="post" action="/cgi-bin/send_text.py">
        <input type="file" accept = "text/plain" name="filenameText">
        <input type="submit" value="Отправить">
    </form> ''')

conn.close()
print("""</div>
  <div id="footer"> &copy; 2016 Все права защищены &nbsp;<span class="separator">|</span>&nbsp; <a href="http://vk.com/ivan_matyash" target="blank">Ivan Matsiash</a> </div>
</div>
</body>
</html>""")
