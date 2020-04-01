import csv

def read():
	with open('db.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			print row
		file.close()

def write():
	with open('db.csv', 'wb') as file:
		writer = csv.writer(file)
		writer.writerow(['id1', 'id2', 'id3'])
		writer.writerow(['SN', 'Movie', 'Protagonist'])
		writer.writerow(['SN', 'Movie', 'Protagonist'])
		writer.writerow(['SN', 'Movie', 'Protagonist'])
		file.close()

def addColumn(identifier):
	rows = content()
	sz = size()
	with open('db.csv', 'wb') as file:
		writer = csv.writer(file)
		for index in range(sz):
			row = rows[index]
			if index == 0:
				row.append(identifier)
			else:
				row.append('')
			writer.writerow(row)

		file.close()

def removeColumn(identifier):
	rows = content()
	sz = size()

	firstRow = rows[0]
	idIndex = 0
	identifierExists = False
	for elem in firstRow:
		if elem == identifier:
			identifierExists = True
			break
		idIndex += 1

	if not identifierExists:
		print 'indentifier not found sorry'
		return
	else:
		with open('db.csv', 'wb') as file:
			writer = csv.writer(file)
			for index in range(sz):
				row = rows[index]
				row.pop(idIndex)
				writer.writerow(row)

def override():
	rows = content()
	sz = size()
	with open('db.csv', 'wb') as file:
		writer = csv.writer(file)
		for index in range(sz):
			row = rows[0]
			override = (index != 0) and (row[0] == 'SN')
			if override:
				writer.writerow(['SE', 'Movie', 'Protagonist'])
			else:
				writer.writerow(row)
		file.close()

def content():
	with open('db.csv', 'r') as file:
		reader = csv.reader(file)
		rows = size() * [None]
		index = 0
		for row in reader:
			rows[index] = row
			index += 1
		file.close()
		return rows


def size():
	with open('db.csv', 'r') as file:
		reader = csv.reader(file)
		size = 0
		for row in reader:
			size += 1
		file.close()
		return size

write()
addColumn('id4')
removeColumn('id4')
read()