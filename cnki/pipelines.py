# -*- coding: utf-8 -*-

import json
import codecs
import MySQLdb
import MySQLdb.cursors
import pymongo
from twisted.enterprise import adbapi
from scrapy import signals
from datetime import datetime

class CnkiJsonPipeline(object):

	def __init__(self):
		self.file = codecs.open('Cnki_data.json', mode = 'wb', encoding = 'utf8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line.decode("unicode_escape"))
		log.msg('The item was added to JSON file successfully.',
				level = log.INFO,spider=spider)

		return item

class CnkiMySQLPipeline(object):

	def __init__(self):
		self.conn = MySQLdb.connect(user='root', passwd='131072', db='cnkidb',
									host='127.0.0.1', charset='utf8',
									use_unicode=True)
		self.cursor = self.conn.cursor()
		#Clean the form.
		self.cursor.execute("truncate table cnkitable;")
		self.conn.commit()

	def process_item(self, item, spider):
		self.cursor.execute(
			'insert into cnkitable(title,abstract,keyword) values(%s,%s,%s)',
			(item['title'], item['abstract'], item['keyword']))
		self.conn.commit()
		log.msg('The item was added to MySQL database successfully.',
				level = log.INFO,spider=spider)

		return item

class CnkiMongoDBPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem('Missing{0}!'.format(data))
		if valid:
			self.collection.insert(dict(item))
			log.msg('The item was added to MongoDB database successfully.',
					level = log.INFO,spider=spider)
		return item
