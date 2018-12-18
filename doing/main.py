import inspect
import paramiko
import threading
import subprocess
from os import sys
from concurrent.futures import ThreadPoolExecutor

lock = threading.Lock()

def build_database():
	list_of_jobs = []
	hosts = build_ping()
	for hostname in hosts:
		list_of_jobs.append([run_remote_command, hostname, 'show version'])
	ans = multi_threaded_execution(256, list_of_jobs)
	for i in range(len(ans)):
		if ans[i] != None:
			print(hosts[i], file = sys.stdout)
		else:
			print('Error in: ' + str(hosts[i]), file = sys.stderr)

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
			['/bin/ping', '-c', '1', '-W', '30', host]
		])
	idx = -1
	ans = []
	for i in multi_threaded_execution(256, list_of_jobs):
		idx += 1
		try:
			i.check_returncode()
			ans.append(hosts[idx])
		except subprocess.CalledProcessError:
			continue
	return ans

def initialize():
	global timeout, log, results, credentials
	timeout = 30
	try:
		log = open('log.txt', 'w')
		results = open('results.txt', 'w')
		with open('credentials.txt', 'r') as file_credentials:
			credentials = []
			v = file_credentials.readlines()
			for i in range(2):
				credentials.append(v[i].split('\'')[1].strip())
	except Exception as exception:
		print_exception_error(inspect.stack()[0], exception, sys.stderr)

def main():
	# show chassis hardware
	initialize()
	build_database()

def multi_threaded_execution(workers, list_of_jobs):
	ans = []
	try:
		threads = []
		with ThreadPoolExecutor(max_workers = workers) as executor:
			for parameters in list_of_jobs:
				threads.append(
					executor.submit(
						parameters[0],
						*parameters[1:]
					)
				)
		for thread in threads:
			ans.append(thread.result())
	except Exception as exception:
		print_exception_error(inspect.stack()[0], exception, sys.stderr)
	return ans

def print_exception_error(frame, exception, filename):
	with lock:
		info = inspect.getframeinfo(frame[0])
		print(
			'filename: ' + str(info.filename)
			+ ', function: ' + str(info.function)
			+ ', line: ' + str(info.lineno),
			file = filename
		)
		print(exception, file = filename)

def run_local_command(command):
	try:
		return subprocess.run(
			args = command,
			stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT,
		)
	except subprocess.CalledProcessError as exception:
		print_exception_error(inspect.stack()[0], exception, sys.stderr)

def run_remote_command(hostname, command):
	global credentials, log, timeout
	while True:
		try:
			with paramiko.SSHClient() as ssh:
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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
		except Exception as exception:
			print_exception_error(
				inspect.stack()[0],
				'hostname: ' + hostname + '\n'
				+ str(exception), sys.stderr
			)
			with lock:
				if str(exception).find('[Errno 104] Connection reset by peer') != -1:
					continue
				else:
					return None

main()