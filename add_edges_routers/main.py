import sys, threading, paramiko, getpass, random

g = {}
aux = {}
invalid = []
database = {}
new_tunnel = {}
exceptions = []
credentials = []
possible_errors = []
# possible_errors = ['timed out', 'Incompatible version', 'Authentication failed', 'Authentication timeout', 'Unable to connect to port 22']
lock = threading.Lock()
types = ['P', 'PE', 'BORDA']
prefixes = ['189.39.3.', '200.225.196.', '200.225.199.', '200.225.200.', '200.225.254.']

def run_command(host, username, password, timeout, command, limit):
	for iteration in range(limit):
		ssh = paramiko.SSHClient()
		with ssh:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(host, username = username, password = password, allow_agent = False, look_for_keys = False, timeout = timeout, banner_timeout = timeout, auth_timeout = timeout)
				stdin, stdout, stderr = ssh.exec_command(command, timeout = timeout)
				with lock:
					aux[host] = []
					for line in stdout.readlines():
						line = line.strip()
						if len(line) > 0:
							aux[host].append(line)
					return
			except Exception as error:
				with lock:
					error_string = str(error)
					exceptions.append(host + ' ' + error_string)
					print(host + ' ' + error_string, file = sys.stderr)
					for i in possible_errors:
						if error_string.find(i) != -1:
							return

def build(filename):
	g['P'] = ['P', 'PE']
	g['PE'] = ['P', 'PE', 'BORDA']
	g['BORDA'] = ['PE', 'BORDA']
	with open(filename, 'r') as f:
		for s in f.readlines():
			s = s.strip()
			v = s.split(';')
			database[v[0]] = {}
			database[v[0]]['lsp'] = v[1]
			database[v[0]]['os'] = v[2]

def build_user(timeout):
	while True:
		username = input('Username: ').strip()
		password = getpass.getpass()
		host = random.choice(list(database.keys()))
		command = 'show version'
		print('trying to log in to: ', host)
		run_command(host, username, password, timeout, command, 10)
		if aux.get(host) != None and len(aux[host]) > 0:
			print('sucessfully logged in as: ' + username)
			credentials.append(username)
			credentials.append(password)
			return

def assert_string(other, valid):
	s = ''
	for i in other:
		for j in valid:
			if i >= j[0] and i <= j[1]:
				s += i
				break
	if len(s) == 0:
		return 'Invalid input'
	return s

def valid_host(host):
	v = host.split('.')
	if len(v) != 4:
		return False
	for i in prefixes:
		if host.find(i) != -1:
			return int(v[3]) >= 0 and int(v[3]) <= 255
	return False

def valid_type(htype):
	for i in types:
		if htype == i:
			return True
	return False

def query_new_tunnel():
	while True:
		print()
		new_tunnel['host'] = assert_string(input('Insert loopback ip, example -> 189.39.3.1: '), [('0', '9'), ('.', '.')])
		new_tunnel['lsp'] = assert_string(input('Insert lsp without \'FROM\' and \'TO\', example -> MX960-A-SPO-PIA-C: '), [('A', 'Z'), ('a', 'z'), ('-', '-'), ('0', '9')])
		new_tunnel['type'] = assert_string(input('Insert type, example -> P, PE, BORDA: ').upper(), [('A', 'Z')])
		if valid_host(new_tunnel['host']) == False:
			print('Invalid loopback ip: ' + new_tunnel['host'])
			continue
		if new_tunnel['lsp'] == 'Invalid input':
			print('Invalid lsp: ' + new_tunnel['lsp'])
			continue
		if valid_type(new_tunnel['type']) == False:
			print('Invalid type: ' + new_tunnel['type'])
			continue
		print()
		print('Please confirm:')
		print('loopback ip: ' + new_tunnel['host'])
		print('lsp: ' + new_tunnel['lsp'])
		print('type: ' + new_tunnel['type'])
		response = input('Do you confirm? (YES or NO): ')
		for i in response:
			if i.lower() == 'y' or i.lower() == 'e' or i.lower() == 's':
				return

def check_valid():
	for host in database:
		if host == new_tunnel['host']:
			invalid.append('loopback already been used by: ' + host + ' ' + database[host]['lsp'])
		if database[host]['lsp'] == new_tunnel['lsp']:
			invalid.append('lsp already been used by: ' + host + ' ' + database[host]['lsp'])
	for i in invalid:
		print(i)
	return len(invalid) == 0

def main():
	build('correct')
	timeout = 60 * 5
	build_user(timeout)
	while True:
		query_new_tunnel()
		if check_valid() == True:
			break
	print('SÓ VAI')

main()