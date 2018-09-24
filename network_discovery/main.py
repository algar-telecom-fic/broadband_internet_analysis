import sys, threading, paramiko, os

ans = {}
ips = []
output = []
timeout = 60 * 5
credentials = []
lock = threading.Lock()
os_names = ['juniper', 'cisco-xr', 'cisco-ios']
os_convert = {
	'JUNOS': os_names[0],
	'IOS XR': os_names[1],
	'IOS Software': os_names[2]
}
loopback_commands = {
	os_names[0]: 'show configuration | display set | match lo0 | match inet | match add | match inte | except inet6',
	os_names[1]: 'sh ip inte bri | in Loopback0',
	os_names[2]: 'sh ip inte bri | in Loopback0'
}
lsp_commands = {
	os_names[0]: 'show mpls lsp ingress',
	os_names[1]: 'show interfaces description | include tt',
	os_names[2]: 'show int description | include Tu'
}
prefixes = ['189.39.3.', '200.225.196.', '200.225.199.', '200.225.200.', '200.225.254.']
possible_errors = [
	'Error reading SSH protocol banner',
	'Unable to connect to port 22',
	'Incompatible version',
	'timed out'
]

def build_credentials():
	with open('credentials.txt', 'r') as f:
		for i in f.readlines():
			for j in i.split('\n'):
				if j.find('username:') != -1:
					credentials.append(j[10: -1])
				elif j.find('password:') != -1:
					credentials.append(j[10: -1])

def build_database():
	threads = []
	for i in ips:
		t = threading.Thread(target = solve, args = [i])
		t.start()
		threads.append(t)
	for t in threads:
		t.join()
	for host in ans:
		if ans[host].get('os') != None and ans[host].get('lsp') != None:
			output.append(host + ';' + ans[host]['lsp'] + ';' + ans[host]['os'])
	output.sort()

def build_pinged_ips():
	threads = []
	for i in range(256):
		suffix = str(i)
		for prefix in prefixes:
			host = prefix + suffix
			t = threading.Thread(target = ping, args = [host])
			t.start()
			threads.append(t)
	for t in threads:
		t.join()

def get_loopback(host):
	run_command(host, loopback_commands[ans[host]['os']])
	with lock:
		for s in ans[host]['output']:
			if ans[host]['os'] == os_names[0]:
				pos = s.find('address')
				if pos != -1:
					for i in range(pos + 8, len(s)):
						if s[i] == '/':
							ans[host]['loopback'] = s[pos + 8: i]
							return
			else:
				pos = s.find('Loopback0')
				if pos != -1:
					start = -1
					for i in range(pos + 9, len(s)):
						if start == -1 and s[i] != ' ':
							start = i
						elif start != -1 and (s[i] < '0' or s[i] > '9') and s[i] != '.':
							ans[host]['loopback'] = s[start: i]
							return

def get_lsp(host):
	run_command(host, lsp_commands[ans[host]['os']])
	with lock:
		for s in ans[host]['output']:
			pos = s.find('FROM-')
			if pos != -1:
				while True:
					other = s.find('FROM', pos + 1)
					if other == -1:
						break;
					pos = other
				pos += 5
				for i in range(pos, len(s)):
					if s[i].isalnum() == False and s[i] != '-':
						ans[host]['lsp'] = s[pos: i]
						return
					elif i == len(s) - 1:
						ans[host]['lsp'] = s[pos:]
						return

def get_os(host):
	run_command(host, 'show version')
	with lock:
		if ans[host].get('output') != None:
			for s in ans[host]['output']:
				for i in os_convert:
					if s.find(i) != -1:
						ans[host]['os'] = os_convert[i]
						return

def main():
	build_pinged_ips()
	build_credentials()

	#  solve('')
	build_database()

	for i in output:
		print(i)

def ping(host):
	if os.system('ping -c 1 -t 60 ' + host + ' > /dev/null') == 0:
		with lock:
			ips.append(host)

def run_command(host, command):
	global timeout
	with paramiko.SSHClient() as ssh:
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		password_counter = 0
		while password_counter < 10:
			try:
				ssh.connect(host, username = credentials[0], password = credentials[1], timeout = timeout, banner_timeout = timeout, auth_timeout = timeout)
				stdin, stdout, stderr = ssh.exec_command(command, timeout = timeout)
				with lock:
					ans[host]['output'] = []
					for line in stdout.readlines():
						line = line.strip()
						if len(line) > 0:
							ans[host]['output'].append(line)
					return
			except Exception as error:
				with lock:
					error_str = str(error)
					print('******************** Exception on ' + host + ': ' + error_str, file = sys.stderr)
					for i in possible_errors:
						if error_str.find(i) != -1:
							return
					if error_str.find('Authentication failed') != -1:
						password_counter += 1

def solve(host):
	with lock:
		ans[host] = {}
	get_os(host)
	with lock:
		if ans[host].get('os') == None:
			return
	get_loopback(host)
	with lock:
		if ans[host].get('loopback') == None or ans[host]['loopback'] != host:
			return
	get_lsp(host)
	with lock:
		if ans[host].get('lsp') == None:
			return

main()