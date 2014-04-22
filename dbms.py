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
				pass
		if match:
			new_table.append(row)

	return [table[0], new_table]

def display(data):
	table = PrettyTable(data[0])
	for row in data[1]:
		table.add_row(row)
	print(table)

def select_terms(query):
	terms = []
	query = query.split("from")
	query = query[0].split("select")[1]
	if ',' in query:
		for term in query.split(','):
			terms.append(term.strip(' \t\n\r'))
		return terms
	else:
		return [query.strip(' \t\n\r')]

def from_terms(query):
	terms = []
	query = query.split("from")[1]
	if "where" in query:
		query = query.split("where")[0]
	if ',' in query:
		for term in query.split(','):
			terms.append(term.strip(' \t\n\r'))
		return terms
	else:
		return [query.strip(' \t\n\r')]

def where_terms(query):
	terms = []
	if "where" not in query:
		return []
	query = query.split("where")[1]
	if 'and' in query:
		for term in query.split('and'):
			terms.append(term.strip(' \t\n\r'))
		return terms
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

	return [select_terms(query), from_terms(query), where_terms(query)]

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
		q = parse_query(query)
		display(select(q[0], where(q[2], join(q[1]))))

main()
# debug()
