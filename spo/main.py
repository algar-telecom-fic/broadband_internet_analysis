import json
import os
import datetime
import sys
import operator
from openpyxl import Workbook
sys.path.append("/home/marcos/spo")
from my_sql import mySQL

def aux_treat(table, interval, tod):
	ans = {}
	ans['Table_name'] = table[0][0]
	ans['Table_id'] = int(table[0][1])
	ans['Maximum_Tuple_Number'] = 0
	ans['Used_number'] = 0
	ans['Dia'] = tod
	for i in table:
		if len(i) < 5:
			continue
		elif int(i[2]) >= interval[0] and int(i[2]) <= interval[1]:
			ans['Maximum_Tuple_Number'] += int(i[3])
			ans['Used_number'] += int(i[4])
	return ans


def treat_table(table, tod):
	ans = {}
	spec = info[str(table[0][1])]
	if spec == 1 or spec == 2:
		ans['Table_name'] = table[0][0]
		ans['Table_id'] = int(table[0][1])
		ans['Maximum_Tuple_Number'] = int(table[0][2])
		ans['Used_number'] = int(table[0][3])
		ans['Dia'] = tod
	elif spec == 3:
		ans = aux_treat(table, [1000, 1006], tod)
	elif spec == 4:
		ans = aux_treat(table, [1500, 1506], tod)
	elif spec == 5:
		ans = aux_treat(table, [1700, 1701], tod)
	fans.append(ans)


def main(filename, tod):
	flag_fst = True
	dirt = os.getcwd()
	aux = []
	table = []

	with open(dirt + "/files/data/" + filename, "r") as file:
		for line in file:
			if line[:4] == ' tbl' or line[:4] == ' TBL':
				aux.append(line.split())
		aux.sort()

	table.append(aux[0])
	for teste in aux[1:]:
		if teste[1] != table[0][1]:
			treat_table(table, tod)
			table = []
		table.append(teste)
	# Ao final, a última tabela também deve ser tratada, já q nunca entrará no if.
	treat_table([teste], tod)
	spo_files = read_json(dirt + "/files/spo_config.json")
	filepath = spo_files ["database_credentials"]
	credentials = read_json(filepath)

	db_name = spo_files ["database_name"]
	table_name = spo_files ["table_name"]
	table_info = spo_files ["table_info"]
	spo_info = read_json(table_info)
	db = mySQL(credentials, db_name)
	db.insert_into(table_name, spo_info, fans)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')

def fill_sheet():
	wb = Workbook()
	ws = wb.active
	header = ['Table_name', 'Table_id', 'Maximum_Tuple_Number', 'Used_number']
	ws.append(header)
	for row in fans:
		aux_row = []
		for key in header:
			aux_row.append(row[key])
		ws.append(aux_row)
	for col in ws.columns:
		for cell in col:
			alignment_obj = cell.alignment.copy(horizontal='center', vertical='center')
			cell.alignment = alignment_obj
	wb.save("Planilha Final - SPO.xlsx")

fans = []
info = read_json(os.getcwd() + "/files/tables.json")
if __name__ == "__main__":
	main("TABELAS SPO - 21-10-2019.txt", datetime.date(2019, 10, 11))
	fans.sort(key=operator.itemgetter('Table_id'))
	fill_sheet()
