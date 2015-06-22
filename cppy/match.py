
import os
from datetime import datetime
import sqlite3
from terminaltables import AsciiTable

DEFAULT_PATH = './data'

class NumberLimitError(Exception):
	pass

class Match:
	def __init__(self, val):
		self.val = val
		self.match_type = 0

class PhoneMatch(Match):
	def __init__(self, val):
		self.val = self.format_val(val)
		self.match_type = 2

	def format_val(self, val):
		if len(val) > 16:
			raise NumberLimitError("Exceeds known number range")
		if '-' in val:
			init_len = len(val)
			for group in val.split('-'):
				val += group
			val = val[init_len:]
		return val

	def log(self):
		if self.val:
			conn = sqlite3.connect("data.db")
			with conn:
				cur = conn.cursor()    
				cur.execute("CREATE TABLE IF NOT EXISTS Numbers(Id INTEGER PRIMARY KEY, Value TEXT UNIQUE)")
				cur.execute('INSERT OR IGNORE INTO Numbers (Value) VALUES (?)', (self.val,))
		finish('number')

class EmailMatch(Match):
	def __init__(self, val):
		self.val = val
		self.match_type = 1
		self.domain = self.val[self.val.find('@')+1:self.val.find('.')]

	def log(self):
		if self.domain:
			conn = sqlite3.connect("data.db")
			with conn:
				cur = conn.cursor()    
				cur.execute("CREATE TABLE IF NOT EXISTS Emails(Id INTEGER PRIMARY KEY, Value TEXT UNIQUE, Domain TEXT)")
				cur.execute('INSERT OR IGNORE INTO Emails (Value, Domain) VALUES (?, ?)', (self.val, self.domain))
		finish('email')

def finish(table_type):
	conn = sqlite3.connect("data.db")
	with conn:
		cur = conn.cursor()  

		if table_type.lower() == 'number':
			cur.execute("SELECT * FROM Numbers")
			resultset = []
			while True:
					row = cur.fetchone()
					if row == None:
						break
					resultset.append([row[1]])
			resultset.insert(0, ['Phone Number'])
			table = AsciiTable(resultset)
			print table.table

		elif table_type.lower() == 'email':
			cur.execute("SELECT * FROM Emails")
			resultset = []
			while True:
					row = cur.fetchone()
					if row == None:
						break
					resultset.append([row[1], row[2]])
			resultset.insert(0, ['Email Address', 'Domain'])
			table = AsciiTable(resultset)
			print table.table
