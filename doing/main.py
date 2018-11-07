import paramiko
import subprocess
from os import sys
from concurrent.futures import ThreadPoolExecutor

def build_database():
	list_of_jobs = []
	hosts = build_ping()
	for hostname in hosts:
		list_of_jobs.append([run_remote_command, hostname, 'show version'])
	idx = -1
	for i in multi_threaded_execution(256, list_of_jobs):
		idx += 1
		print('host: ' + hosts[idx] + ', result: ' + str(i))

def build_ping():
	prefixes = [
		'189.39.3.',
		'200.225.196.',
		'200.225.199.',
		'200.225.200.',
		'200.225.254.',
	]
	hosts = []
	for prefix in prefixes:
		for suffix in range(256):
			hosts.append(prefix + str(suffix))
	list_of_jobs = []
	for host in hosts:
		list_of_jobs.append([
			run_local_command, 
			['/bin/ping', '-c', '2', '-W', '30', host]
		])
	idx = -1
	ans = []
	for i in multi_threaded_execution(256, list_of_jobs):
		idx += 1
		try:
			i.check_returncode()
			ans.append(hosts[idx])
		except subprocess.CalledProcessError as error:
			continue
	return ans
	
def initialize():
	global timeout, log, results, credentials
	timeout = 30
	log = open('log.txt', 'w')
	results = open('results.txt', 'w')
	credentials = ['gardusi', 'Kappaloiro-13']

def main():
	initialize()
	build_database()
	
def multi_threaded_execution(workers, list_of_jobs):
	threads = []
	with ThreadPoolExecutor(max_workers = workers) as executor:
		for parameters in list_of_jobs:
			threads.append(
				executor.submit(
					parameters[0],
					*parameters[1:]
				)
			)
		ans = []
		for thread in threads:
			ans.append(thread.result())
		return ans

def run_local_command(command):
	try:
		return subprocess.run(
			args = command,
			stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT,
		)
	except subprocess.CalledProcessError as error:
		print('Return code error on "run_local_command", command: ' + command + ', returncode: ' + str(error.returncode), file = log)
		return error

def run_remote_command(hostname, command):
	global credentials, log, timeout
	with paramiko.SSHClient() as ssh:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			ssh.connect(
				hostname,
				username = credentials[0],
				password = credentials[1],
				timeout = timeout,
				banner_timeout = timeout,
				auth_timeout = timeout,
				look_for_keys = False,
				allow_agent = False,
			)
			stdin, stdout, stderr = ssh.exec_command(command, timeout = timeout)
			ans = []
			for line in stdout.readlines():
				ans.append(line.strip())
			return ans
		except Exception as error:
			print('host: ' + hostname + ', error: ' + str(error), file = log)
			return None

main()