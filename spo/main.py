# Considerações importantes sobre a maneira de tratar cada tabela especificado no arquivo "tables.json"
# 1 - TABELA ÚNICA
# 2 - TABELA DUPLICADA QUE NÃO POSSUI MÓDULO, CONSIDERAR OS VALORES DE UMA LINHA, E EXCLUIR AS OUTRAS
# 3 - TABELA DUPLICADA COM MÓDULO, CONSIDERAR DO MÓDULO 1000 AO 1006. SOMAR OS VALORES DE MAXIMUM TUPLE E USED NUMBER 
# 4 - TABELA DUPLICADA COM MÓDULO, CONSIDERAR DO MÓDULO 1500 AO 1506. SOMAR OS VALORES DE MAXIMUM TUPLE E USED NUMBER
# 5 - TABELA DUPLICADA COM MÓDULO, CONSIDERAR DO MÓDULO 1700 AO 1701. SOMAR OS VALORES DE MAXIMUM TUPLE E USED NUMBER

import json
import os
import datetime
import sys
sys.path.append("/home/otsuka/doing/spo")
from my_sql import mySQL

# faz o mesmo tratamento, mas só altera a faixa de módulos, especificada nas linhas 34, 36 e 38.
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

# pega cada tabela e trata do jeito que estiver especificado no json "tables"
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
	dirt = os.getcwd()
	aux = []
	table = []

	with open(dirt + "/files/" + filename, "r") as file:
		for line in file:
			# Insere numa lista todas as linhas que não são lixo... TOMAR CUIDADO, CONFERIR COM ANDRIO
			if line[:4] == ' tbl' or line[:4] == ' TBL': # realmente todas as linhas uteis começam com tbl ou TBL??
				aux.append(line.split())
		# Ordena pra agrupar as tabelas que possuem mesmo id
		aux.sort()

	# Insere numa lista auxiliar todas as linhas que representam a mesma tabela e trata essa lista quando
	# encontra alguma linha da próxima tabela
	table.append(aux[0])
	for teste in aux[1:]:
		if teste[1] != table[0][1]:
			treat_table(table, tod)
			table = []
		table.append(teste)
	# Ao final, a última tabela também deve ser tratada, já q nunca entrará no if.
	treat_table([teste], tod)

	# info do banco de dados e das tabelas
	spo_files = read_json(dirt + "/files/spo_config.json")
	filepath = spo_files ["database_credentials"]
	credentials = read_json(filepath)

	db_name = spo_files ["database_name"]
	table_name = spo_files ["table_name"]
	table_info = spo_files ["table_info"]
	spo_info = read_json(table_info)
	db = mySQL(credentials, db_name)
	# insere no banco a resposta final
	db.insert_into(table_name, spo_info, fans)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')


fans = []
# pega um json que relaciona cada tipo de tabela com o jeito de tratar cada uma...
info = read_json(os.getcwd() + "/files/tables.json")
if __name__ == "__main__":
	main("TABELAS SPO - 21-10-2019.txt", datetime.date(2019, 10, 11))
