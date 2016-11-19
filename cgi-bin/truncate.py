#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3
import nltk



conn = sqlite3.connect('data/voc.db')
c = conn.cursor()
c.execute('''DROP TABLE voc''')
c.execute('''CREATE TABLE voc (word TEXT, amount INTEGER DEFAULT 1, tagID INTEGER)''')
conn.commit()


message ='Словарь успешно был очищен. Это окно закроется автоматически.'


print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Очистка словаря</title>
<script>
        function closeW() 
        {  
	
            var t=setTimeout("closeOpenedWindow();", 3000); // закрыть через 2 сек
        }  
        function closeOpenedWindow()
        {  
            window.close()  
        } 
    </script>
	</head>
	<body>""")
print(message)
print('''<script type="text/javascript">
closeW()
</script>''')
print('<br><a href = "/cgi-bin/voc.py">Назад к словарю</a>')
print("""</body>
	</html>""")
