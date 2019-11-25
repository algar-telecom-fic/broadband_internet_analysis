# Trata arquivos com "no_config"... 
def build_result_final(filepath):
	with open(filepath, 'r') as file:
		ftr = ''
		ans = {}
		U = 0
		F = 0
		N = 0
		OK = 0
		no_config = 0
		for line in file:
			if line[0] == ' ':
				ftr += line.replace('\n', ' ')
		for idx, elem in enumerate(ftr):
			if elem == 'F':
				F += 1
			elif elem == 'U':
				U += 1
			elif elem == 'O' and ftr[idx+1] == 'K':
				OK += 1
			elif elem == 'N':
				if ftr[idx+1] == ' ':
					N += 1
				elif ftr[idx+3] == 'c':
					no_config += 1
		ans["Capacidade"] = U  + F + N + OK + no_config
		ans["Ocupado"]    = F + N + OK
		ans["Disponivel"] = U  + no_config
		return ans

# Trata arquivos comuns...
def build_result_commom(filepath):
	with open(filepath,'r') as file:
		ftr = ''
		ans = {}
		U  = 0
		FN = 0
		for line in file:
			if line[0] == ' ':
				ftr += line.replace('\n', ' ').replace('Slot No.','')
		for i in ftr:
			if i == 'F' or i == 'N':
				FN += 1
			elif i == 'U':
				U  += 1
		ans["Capacidade"] = U + FN
		ans["Ocupado"]    = FN
		ans["Disponivel"] = U
		return ans
