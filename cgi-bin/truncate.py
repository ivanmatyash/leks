#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3
import time


conn = sqlite3.connect('data/voc.db')
c = conn.cursor()
t1 = time.time()
c.execute('''SELECT COUNT(*) FROM voc''')
amountW = c.fetchall()[0][0]
c.execute('''SELECT SUM(amount) FROM voc''')
amountS = c.fetchall()[0][0]
c.execute('''DROP TABLE voc''')
c.execute('''CREATE TABLE voc (word TEXT, amount INTEGER DEFAULT 1, tagID INTEGER)''')
conn.commit()
t2 = time.time()

message ='<h2>Очистка словаря прошла успешно.</h2><b><h3>Информация об очистке:</h3></b> \
	<table>\
	<tr><td><b>Количество удаленных слов: </b></td> <td>{0}</td></tr>\
	<tr><td><b>В том числе уникальных: </b></td> <td>{1}</td></tr>\
	<tr><td><b>Время удаления: </b></td> <td>{2:.4f} сек.</td></tr>\
	</table>Это окно закроется через 5 секунд автоматически.<br>'.format(amountS, amountW, t2-t1)

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Очистка словаря</title>
<script>
        function closeW() 
        {  
	
            var t=setTimeout("closeOpenedWindow();", 5000); // закрыть через 2 сек
        }  
        function closeOpenedWindow()
        {  
		window.opener.location.reload();
        	window.close()  
        } 
    </script>
	</head>
	<body>""")
print(message)
print('''<script type="text/javascript">
closeW()
</script>''')
print('''<br><center><a href="#" onclick="closeOpenedWindow();">[Закрыть отчет]</a></center>''')
print("""</body>
	</html>""")
