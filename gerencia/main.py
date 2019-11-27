import subprocess
import json
import utils
import sys
import os
sys.path.append("/home/otsuka/doing/gerencia/piloto_mgw")
from my_sql import mySQL
import datetime


# Função que usa uma busca binária para encontrar uma  estação específica em um dicionário 
# Retorna todas as informações antigas da estação passada.
def find_old(estacao, old_cities):
	lo = 0
	hi = len(old_cities) - 1
	while(lo <= hi):
		me = int((lo + hi)/2)
		if old_cities[me][0] == estacao:
			return old_cities[me]
		elif old_cities[me][0] > estacao:
			hi = me-1
		else:
			lo = me+1
	return -1


def main(tod):
	# os.getcwd pega caminho pro diretório atual, onde está sendo executado o códoigo.
	dirt = os.getcwd()
	# mgw_files é um dicionário que contém as informações da tabela que vai ser alterada
	mgw_files = read_json(dirt + "/files/mgw_config.json")
	# filepath mostra o caminho para a credencial pra acessar o banco
	filepath = mgw_files ["database_credentials"]
	# Coloca as informações de acesso ao banco em um dicionário
	credentials = read_json(filepath)

	# Inicialização das variáveis usadas para fazer a conexão com o banco mysql
	db_name = mgw_files ["database_name"]
	table_name = mgw_files ["table_name"]
	table_info = mgw_files ["table_info"]

	# db é o cursor que aponta para o banco de dados e mgw_info contém a descrição da tabela
	db = mySQL(credentials, db_name)
	mgw_info = read_json(table_info)

	# Calcula e armazena em um auxiliar (aux_day) o dia que dá 6 meses antes do dia dos arquivos (tod)
	DD = datetime.timedelta(days=180)
	aux_day = tod - DD
	aux_time = datetime.datetime.min.time()
	aux_day = datetime.datetime.combine(aux_day, aux_time)

	# essa query puxa todos os dias distintos entre si e coloca numa lista (dates) 
	query1 = "select distinct Dia from mgw"
	dates = db.executaQuery(query1)
	query_date = tod #default
	# Busca na lista de dias, de trás pra frente, por eficiência, uma data que tenha no mínimo 6 meses de diferença
	# e armazena na variável query date
	for d in reversed(dates):
		if (d[0] <= aux_day):
			query_date = str(d[0]).split()[0]
			break

	# puxa as informações da data especificada, pois são elas que vão ser utilizadas para calcular crescimento
	query2 = f"select Estacao, Ocupado, Dia from mgw where dia = '{query_date}';"
	old_cities = db.executaQuery(query2)
	old_cities.sort()

	# Calcula a quantidade de dias exatos que há entre o dia encontrado em query_date com o dia atual
	# Essa informação é utilizada  para o cálculo do crescimento, na linha 86
	delta = tod - query_date
	delta = delta.days

	# fans é a final answer que deve ser inserida no banco, é uma lista de dicionários
	fans  = []
	# usa comandos do linux para remover o diretório antigo e dar um unzip no arquivo atual com os mgw
	subprocess.call(['rm', '-r', 'mgw'])
	subprocess.call(['unzip', 'mgw.zip', '-d', 'mgw'])
	# dicionário que pega informações imutáveis que já foram passadas a princípio num json
	dictf = read_json(dirt + '/files/mgw_elem.json')

	# Monta o resultado de cada uma das estações
	for filename in dictf:
		# encontra as informações antigas
		old = find_old(dictf[filename][1], old_cities)
		ans = []
		# deve tratar separadamente os arquivos que possuem "no config" no nome.
		if filename.find('no config') == -1:
			ans = utils.build_result_commom (dirt + '/mgw/' + filename)
		else:
			ans = utils.build_result_final (dirt + '/mgw/' + filename)
		# monta o dicionário específico da estação.
		ans['Localidade']    = dictf[filename][0]
		ans['Estacao']       = dictf[filename][1]
		ans['Elemento']      = dictf[filename][2]
		ans['Dia']           = tod
		ans['Crescimento']   = round ( ( ans['Ocupado'] - old[1] ) / delta * 30 )
		ans['Esgotamento_M'] = "" # CUIDADO, DEVE ALTERAR ESSA COLUNA
		try:
			ans['Esgotamento'] = ans['Disponivel'] / ans['Crescimento']
		except ZeroDivisionError:
			ans['Esgotamento'] = 0
		ans['Taxa_Ocupacao'] = ( ans['Capacidade'] - ans['Disponivel'] ) / ans['Capacidade']

		# Coloca na  lista final o dicionário da estação calculada
		fans.append(ans)

	# Insere no banco
	db.insert_into(table_name, mgw_info, fans)


# Lê um arquivo json e retorna aquelas informações em um dicionário.
def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')


# deve alterar isso dependendo da data do relatório... Ver com o pedro qual é a melhor forma de fazer isso
# de acordo com a interface
if __name__ == "__main__":
	main(datetime.date(2019, 10, 11))
