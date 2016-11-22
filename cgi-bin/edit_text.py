#!/usr/bin/env python3
import nltk
import sqlite3

tags = []
def addTags(c):
	inp = open("tags_table.sql", "rt")
	for strin in inp:
		c.execute(strin)
	print("Теги успешно добавлены")
	inp.close()
def addWords(dic, c):
	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())
	for item in dic:
		c.execute('INSERT INTO voc (word, amount, tagID) VALUES ("{0}","{1}", "{2}")'.format(item[0], dic[item], sl[item[1]]))
		
	

def makeVoc(filename):
	tokens = []
	file_in = open("data/" + filename, "rt")
	for inputStr in file_in:
		inputStr = inputStr.lower()
		tokens.extend(nltk.word_tokenize(inputStr))
	list_rm = []
	for i in tokens:
#		if i[0].isupper():		
#			for b in tokens:
#				if b[0].islower() and i.lower() == b:
#					for k in tokens:
#						if k == i:
#							tokens[tokens.index(k)] = i.lower()
		if not i.isalpha():
			list_rm.append(i)				

	for i in list_rm:
		tokens.remove(i)	
	tags.extend(nltk.pos_tag(tokens))
	file_in.close()
	dic = dict.fromkeys(tags, 0)
	for item in tags:
		dic[item] += 1
	addDB(dic)
	return len(tags)

def addDB(dic):
	conn = sqlite3.connect("data/voc.db")
	c = conn.cursor()
	c.execute('''DROP TABLE IF EXISTS voc''')
	c.execute('''DROP TABLE IF EXISTS groups''')
	c.execute('''CREATE TABLE IF NOT EXISTS voc (idWord INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, amount INTEGER DEFAULT 1, tagID INTEGER, idGroup INTEGER DEFAULT -1)''')
	c.execute('''CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name TEXT, description TEXT, translate TEXT, color TEXT)''')
	c.execute('''CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, idMain INTEGER)''')

	conn.commit()
	c.execute('''SELECT COUNT(*) FROM tags''')
	t = c.fetchall()[0]
	if t[0] == 0:
		addTags(c)
		conn.commit()
	
	
	addWords(dic, c)
	conn.commit()
	conn.close()
