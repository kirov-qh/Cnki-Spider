# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy import signals
from datetime import datetime

class CnkiJsonPipeline(object):

	def __init__(self):
		self.file = codecs.open('Cnki_data.json', mode = 'wb', encoding = 'utf8')
		
	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line.decode("unicode_escape"))
		
		return item
'''		
class CnkiMySQLPipeline(object):
	
	def __init__(self):
		self.conn = MySQLdb.connect(user = 'root', passwd = '131072', db = 'cnkidb', host = '127.0.0.1', charset = 'utf8', use_unicode = True)
		self.cursor = self.conn.cursor()
		#Clean the form.
		self.cursor.execute("truncate table cnkitable;")
		self.conn.commit()
		
	def process_item(self, item, spider):
		self.cursor.execute('insert into cnkitable(title,abstract,keyword) values(%s,%s,%s)',(item['title'],item['abstract'],item['keyword']))
		self.conn.commit()
		
		return item'''
