import json
import sys
sys.path.append("/home/gardusi/github/sql_library")
from sql_json import mySQL


def build_result(file):
	result = {}
	U = 0
	F = 0
	N = 0
	flag = False
	for line in file.readlines():
		if "---" in line:
			flag = not flag
		if flag:
			U += line.count(" U")
			F += line.count(" F")
			N += line.count(" N")
	result["Fault"] = F
	result["Ocupado"] = N
	result["Disponivel"] = U
	resultl = []
	resultl.append(result)
	return resultl


def db_inserction(filepath, db_name, tb_name, db_info, docs):
	credentials = read_json(filepath)
	db_i = read_json(db_info)
	db = mySQL(credentials, db_name)
	db.create_table(tb_name, db_i)
	print(docs)
	db.insert_into(tb_name, db_i, docs)


def main():

	files = read_json("/home/otsuka/doing/gerencia/files/config.json")
	items = open_file(files["filepath"], build_result)
	db_inserction(
		files["database_credentials"],
		files["database_name"],
		files["table_name"],
		files["table_info"],
		items
	)


def open_file(filepath, fun_kappa):
	with open(filepath, "r", encoding='ISO-8859-1') as file:
		return fun_kappa(file)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')


if __name__ == "__main__":
	main()
