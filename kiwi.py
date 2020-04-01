import csv
import sys
from datetime import datetime

class kiwi:

	def __init__(self, filename):
		self.filename = filename
		self.size = self.sizenow()
		self.content = self.contentnow()
		self.width = self.widthnow()

	# my specific terminal manipulations

	def execute(self, flag, something):
		identifier = datetime.now().strftime('%Y-%m-%d')
		index = self.fromflag(flag)
		if str(index) != 'Invalid flag':
			self.updaterow(identifier, index, something)
		else: 
			self.man()

	def man(self):
		print '*** MAN PAGE ***'; print
		print 'Usage: python kiwi.py -F -arg'; print

		print '-F should be one of the following flags'
		print '   ' + self.fromfield('Sport') + ' for sport field'
		print '   ' + self.fromfield('Screentime') + ' for screentime field'
		print '   ' + self.fromfield('Workload') + ' for orkload field'
		print '   ' + self.fromfield('Fruits') + ' for fruits field'
		print '   ' + self.fromfield('Showers') + ' for showers field'

		print '-arg should be filled in with content for given flag'; print

		print 'Data is then stored in a database identified by the current date'

		print 'Use python kiwi.py -r to read the databse'

	def fromfield(self, field):
		switcher = {
			'Date': 'd',
			'Sport': 'sp',
			'Screentime': 'sc',
			'Workload': 'w',
			'Fruits': 'fr',
			'Showers': 'sh',
			'Readmode': 'r'
		}

		return switcher.get(field, 'Invalid field')

	def fromflag(self, flag):
		switcher = {
			self.fromfield('Date'): 0,
			self.fromfield('Sport'): 1,
			self.fromfield('Screentime'): 2,
			self.fromfield('Workload'): 3,
			self.fromfield('Fruits'): 4,
			self.fromfield('Showers'): 5
		}

		return switcher.get(flag, 'Invalid flag')

	# basic manipulation methods

	# need to change this method
	def write(self):
		file = self.readyfile('wb')
		writer = csv.writer(file)
		writer.writerow(['Date', 'Sport', 'Screentime', 'Workload', 'Fruits', 'Showers'])
		writer.writerow(['12-12-2020', '', '', '', '', ''])
		file.close()
		self.update()
	
	def read(self):
		file = self.readyfile('r')
		reader = csv.reader(file)
		for row in reader:
			print row
		file.close()

	def erase(self):
		file = self.readyfile('wb')
		writer = csv.writer(file)
		writer.writerow([None])
		file.close()
		self.update()

	def updaterow(self, identifier, index, something):
		file = self.readyfile('wb')
		writer = csv.writer(file)
		exist = False

		for row in self.content:
			if row[0] == identifier:
				exist = True
				newRow = [None] * self.width
				for i in range(self.width):
					if i == index:
						newRow[i] = something
					else:
						newRow[i] = row[i]
				writer.writerow(newRow)
			else:
				writer.writerow(row)

		file.close()
		self.update()

		if not exist:
			newRow = [None] * self.width
			newRow[0] = identifier
			for i in range(1, self.width):
				if i == index:
					newRow[i] = something
				else:
					newRow[i] = ''
			self.writerow(newRow)
		

	def writerow(self, something):
		file = self.readyfile('wb')
		writer = csv.writer(file)
		for row in self.content:
			writer.writerow(row)

		rowWidth = len(something)
		if rowWidth == self.width:
			writer.writerow(something)
		else:
			delta = abs(rowWidth - self.width)
			if rowWidth < self.width:
				for i in range(delta):
					something.append('')
				writer.writerow(something)
			else:
				print 'In function kiwi.writerow arg: ' + str(something)
				print 'Error: Row does not fit actual width'
		file.close()
		self.update()

	def addcol(self, identifier):
		file = open(self.filename, 'wb')
		writer = csv.writer(file)
		rows = self.content
		for index in range(self.size):
			row = rows[index]
			if index == 0: row.append(identifier)
			else: row.append('')
			writer.writerow(row)
		file.close()
		self.update()

	def remcol(self, identifier):
		rows = self.content
		exist = False
		for elem in rows[0]:
			if elem == identifier:
				idx = rows[0].index(elem)
				exist = True
				break

		if not exist:
			print 'In function kiwi.remcol arg: ' + identifier
			print 'Error: Indentifier not found' 
			return
		else:
			file = self.readyfile('wb')
			writer = csv.writer(file)
			for index in range(self.size):
				row = rows[index]
				row.pop(idx)
				writer.writerow(row)
			file.close()
			self.update()

	# kiwi update methods

	def update(self):
		self.size = self.sizenow()
		self.content = self.contentnow()
		self.width = self.widthnow()

	def contentnow(self):
		file = self.readyfile('r')
		reader = csv.reader(file)
		rows = self.size * [None]
		index = 0
		for row in reader:
			rows[index] = row
			index += 1
		file.close()
		return rows

	def sizenow(self):
		file = self.readyfile('r')
		reader = csv.reader(file)
		size = 0
		for row in reader:
			size += 1
		file.close()
		return size

	def widthnow(self):
		size = 0
		if len(self.content) == 0: return 0
		for elem in self.content[0]:
			size += 1
		return size

	# tools methods

	# user must close the file after usage!
	def readyfile(self, openmode):
		return open(self.filename, openmode)

	def close(self, file):
		file.close()

def runfromfiles(kiwi):
	if len(sys.argv) == 3 and sys.argv[1][1:] != kiwi.fromfield('Readmode'):
		flag = sys.argv[1][1:] # to remove dash
		something = sys.argv[2]
		kiwi.execute(flag, something)
	else:
		if len(sys.argv) > 1 and sys.argv[1][1:] == kiwi.fromfield('Readmode'):
			kiwi.read()
		else:
			kiwi.man()

def runfrombash(kiwi):
	if sys.argv[1] == '':
		kiwi.read()
	elif sys.argv == 'man':
		kiwi.man()
	else:
		flag = sys.argv[1][1:] # to remove dash
		something = sys.argv[2]
		kiwi.execute(flag, something)

if __name__ == '__main__':
	kiwi = kiwi('/Users/Andrea/Documents/Coding/python/kiwi/db.csv')
	if sys.argv[0] == 'kiwi.py':
		runfromfiles(kiwi)
	else:
		runfrombash(kiwi)