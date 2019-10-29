# dict = {
# 	"table_name":       ,
# 	"table_id":			,
# 	"max_tuple_num":	,
# 	"used_num"
# }

# final_answer = [list(public) + list(private)]

# Criar função genérica para tratar cada tipo de tabela.

# def treat_line(line, pub, pri):
# 	aux = line.split()
# 	if len(aux) == 4:
# 		if aux in pub:				# Mudar para Busca Binária
# 			pass
# 		else:
# 			pub.append(aux)
# 	else:

def treat_table(table, pub, pri):
	print()
	for i in table:
		print(i)
	print()

		
def main():
	dirt = "/home/otsuka/Documents/Projects/doing/spo/"
	pub = []
	pri = []
	# Lista que contém temporariamente as tabelas a serem tratadas
	table = []
	with open(dirt + "TABELA-SPO-22-08-2019.txt", "r") as file:
		for idx, line in enumerate(file):
			# Ignorar a linha com o nome das colunas
			if idx == 0:
				continue
			# Acumular as linhas até que a ID da tabela (line[1]) seja diferente.
			# Nesse caso temos o fim de uma tabela e a tratamos.
			elif idx == 1:
				table.append(line.split())
			else: 
				if line.split()[1] != table[0][1]:
					treat_table(table, pub, pri)
					table = []
				table.append(line.split())
		# Ao final a última tabela também deve ser tratada, já q nunca entrará no if.
		treat_table(table,pub,pri)


if __name__ == "__main__":
	main()
