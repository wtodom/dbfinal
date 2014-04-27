import itertools

from prettytable import PrettyTable


a = [["a1", "a2"]]
b = [["b1", "b2", "b3"]]
c = [["c1", "c2", "c3", "c4"]]

def build_table(db_file):
	with open(db_file, "r") as f:
		data = [row.split("	") for row in f.readlines()]
		for row in data:
			row[-1] = row[-1].rstrip()
		return data

def select(columns, table):
	key = [column in columns for column in table[0]]
	new_table = [list(itertools.compress(row, key)) for row in table[1]]
	return [columns, new_table]

def join(tables):
	if 'a' in tables and 'b' in tables and 'c' in tables:
		columns = a[0] + b[0] + c[0]
		res = itertools.product(a[1], b[1], c[1])
	elif 'a' in tables and 'b' in tables:
		columns = a[0] + b[0]
		res = itertools.product(a[1], b[1])
	elif 'a' in tables and 'c' in tables:
		columns = a[0] + c[0]
		res = itertools.product(a[1], c[1])
	elif 'b' in tables and 'c' in tables:
		columns = b[0] + c[0]
		res = itertools.product(b[1], c[1])
	elif 'a' in tables:
		return a
	elif 'b' in tables:
		return b
	elif 'c' in tables:
		return c
	else:
		raise SyntaxError("There was an error in your from clause - tables not found.")

	return [columns, [[item for sublist in row for item in sublist] for row in res]]

def where(conditions, table):
	pairs = []

	for condition in conditions:
		pairs.append([cond.strip(' \t\n\r') for cond in condition.split("=")])

	new_table = []

	for row in table[1]:
		match = True
		for pair in pairs:
			if pair[0] in table[0] and pair[1] in table[0]:  # [col, col]
				if row[table[0].index(pair[0])] != row[table[0].index(pair[1])]:
					match = False
					continue
			elif pair[0] in table[0] and not pair[1] in table[0]:  # [col, val]
				if row[table[0].index(pair[0])] != pair[1]:
					match = False
					continue
			elif not pair[0] in table[0] and pair[1] in table[0]:  # [val, col]
				if pair[0] != row[table[0].index(pair[1])]:
					match = False
					continue
			else:  # wtf?
				raise SyntaxError("There was an error in your where clause - multiple primatives.")
		if match:
			new_table.append(row)

	return [table[0], new_table]

def display(data):
	table = PrettyTable(data[0])
	for row in data[1]:
		table.add_row(row)
	print(table)

def select_terms(query):
	query = query.split("from")[0].split("select")[1]
	if ',' in query:
		return [term.strip(' \t\n\r') for term in query.split(',')]
	else:
		return [query.strip(' \t\n\r')]

def from_terms(query):
	query = query.split("from")[1]
	if "where" in query:
		query = query.split("where")[0]
	if ',' in query:
		return [term.strip(' \t\n\r') for term in query.split(',')]
	else:
		return [query.strip(' \t\n\r')]

def where_terms(query):
	if "where" not in query:
		return []
	query = query.split("where")[1]
	if 'and' in query:
		return [term.strip(' \t\n\r') for term in query.split('and')]
	else:
		return [query.strip(' \t\n\r')]

def parse_query(query):
	"""
	Returns a list of the form:
		[select_terms, from_terms, where_terms]
	where each element is a list of the terms for
	that part of the query.
	"""
	query = query.lower()[:-1]  # make parsing simpler

	s = select_terms(query)
	f = from_terms(query)
	w = where_terms(query)

	# sort them to preserve select and from operations
	# then unsort later
	return [[s, f, w], [sorted(s), sorted(f), sorted(w)]]

def reorder_columns(desired, table):
	indexes = []
	for column in desired:
		indexes.append(table[0].index(column))

	table[0] = [table[0][i] for i in indexes]
	table[1] = [[row[i] for i in indexes] for row in table[1]]

	return table

a.append(build_table("A.txt"))
b.append(build_table("B.txt"))
c.append(build_table("C.txt"))

def main():
	query = None
	while True:
		query = input("wesql> ")
		if query == "quit":
			print("Bye")
			return
		while query[-1] != ';':
			query += input("     > ")
		q = parse_query(query)
		if q[1][0] == ['*']:
			final_result = where(q[1][2], join(q[1][1]))
		else:
			result = select(q[1][0], where(q[1][2], join(q[1][1])))
			final_result = reorder_columns(q[0][0], result)
		display(final_result)

main()
