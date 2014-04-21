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
	key = [1 if column in columns else 0 for column in table[0]]
	new_table = [list(itertools.compress(row, key)) for row in table[1]]
	return [columns, new_table]

def join(tables_to_join):
	if 'a' in tables_to_join and 'b' in tables_to_join and 'c' in tables_to_join:
		columns = a[0] + b[0] + c[0]
		res = itertools.product(a[1], b[1], c[1])
	elif 'a' in tables_to_join and 'b' in tables_to_join:
		columns = a[0] + b[0]
		res = itertools.product(a[1], b[1])
	elif 'a' in tables_to_join and 'c' in tables_to_join:
		columns = a[0] + c[0]
		res = itertools.product(a[1], c[1])
	elif 'b' in tables_to_join and 'c' in tables_to_join:
		columns = b[0] + c[0]
		res = itertools.product(b[1], c[1])
	elif 'a' in tables_to_join:
		return a
	elif 'b' in tables_to_join:
		return b
	elif 'c' in tables_to_join:
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
				# print("neither")
				pass
		if match:
			new_table.append(row)

	return [table[0], new_table]

def display(data):
	table = PrettyTable(data[0])
	for row in data[1]:
		table.add_row(row)
	print(table)

def parse_query(query):
	"""
	Returns a list of the form:
		[select_terms, from_terms, where_terms]
	where each element is a list of the terms for
	that part of the query.
	"""
	query = query.lower()[:-1]  # make parsing simpler

	select_terms = []
	from_terms = []
	where_terms = []

	# where
	if "where" in query:
		query = query.split("where")
		for term in query[1].split("and"):
			where_terms.append(term.strip(' \t\n\r'))
	# from
	query = query[0].split("from")
	for term in query[1].split(","):
		from_terms.append(term.strip(' \t\n\r'))
	# select
	query = query[0].split("select")
	for term in query[1].split(","):
		select_terms.append(term.strip(' \t\n\r'))

	return [select_terms, from_terms, where_terms]

a.append(build_table("A.txt"))
b.append(build_table("B.txt"))
c.append(build_table("C.txt"))

def debug():
	query = "SELECT A1, C2 FROM A, C WHERE A1=C4 and C1=145;"
	query2 = "select a1, b1 from a, b where a1=b2 and b1=35;"
	q = parse_query(query2)

	# display(a)
	# display(b)
	# display(c)
	display(where(q[2], join(q[1])))
	print(query2)
	display(select(q[0], where(q[2], join(q[1]))))

debug()
