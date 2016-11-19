#!/usr/bin/env python3
import nltk
import sqlite3

tags = []

def makeVoc(filename):
	tokens = []
	file_in = open("/tmp/" + filename, "rt")
	for inputStr in file_in:
		tokens.extend(nltk.word_tokenize(inputStr))
	list_rm = []
	for i in tokens:
		if i[0].isupper():		
			for b in tokens:
				if b[0].islower() and i.lower() == b:
					for k in tokens:
						if k == i:
							tokens[tokens.index(k)] = i.lower()
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
	return 1

def addDB(dic):
	conn = sqlite3.connect("/tmp/voc.db")
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS voc (word text, amount integer DEFAULT 1, tag text)''')
	conn.commit()
	for item in dic:
		c.execute('INSERT INTO voc (word, amount, tag) VALUES ("{0}","{1}", "{2}")'.format(item[0], dic[item], item[1]))
		conn.commit()
	conn.close()
