import itertools

from prettytable import PrettyTable

a = [["A1", "A2"]]
b = [["B1", "B2", "B3"]]
c = [["C1", "C2", "C3", "C4"]]
d = [["d1", "d2"]]
e = [["e1", "e2"]]

def build_table(db_file):
	with open(db_file, "r") as f:
		data = [row.split("	") for row in f.readlines()]
		for row in data:
			row[-1] = row[-1].rstrip()
		return data

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

def select(columns, table):
	key = [1 if column in columns else 0 for column in table[0]]  # correct
	new_table = [list(itertools.compress(row, key)) for row in table[1]]
	return [columns, new_table]

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
d.append(build_table("d.txt"))
e.append(build_table("e.txt"))

def debug():
	# display(a[0], a[1])
	# display(b[0], b[1])
	# display(c[0], c[1])

	# for row in join(['a', 'b', 'c'][1]):
	# 	print(row)

	# display(join(['b', 'c']))
	# print(join(['b', 'c']))
	display(select(["B1", "C2"], join(["b", "c"])))

debug()
