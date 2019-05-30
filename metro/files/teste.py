import json

def read_json(filepath):
	with open(filepath, 'rb') as file:
		return json.load(file, encoding = 'utf-8')

db_i = read_json("/home/otsuka/Documents/Projects/doing/agile/metro/files/table_info.json")
print(db_i)