import paramiko
import threading
import subprocess
from os import sys
from concurrent.futures import ThreadPoolExecutor

lock = threading.Lock()

class servers_structure:

    def __init__(self, filename):
        self.commands_loopback = {
            0: 'show configuration | '
                + 'display set | '
                + 'match lo0 | '
                + 'match inet | '
                + 'match add | '
                + 'match inte | '
                + 'except inet6',
            1: 'sh ip inte bri | '
                + 'in Loopback0',
            2: 'sh ip inte bri | '
                + 'in Loopback0',
            3: '?'
        }
        self.commands_hardware = {
            0: 'show chassis hardware',
            1: '?',
            2: '?',
            3: '?',
        }
        self.commands_os = [
            'display version',
            'show version',
        ]
        self.ip_prefixes = [
            '189.39.3.',
            '200.225.196.',
            '200.225.199.',
            '200.225.200.',
            '200.225.254.',
        ]
        self.operational_systems = {
            'JUNOS': 0,
            'IOS XR': 1,
            'IOS Software': 2,
            'HUAWEI': 3,
        }
        try:
            with open(filename, 'r') as file:
                self.credentials = []
                v = file.readlines()
                for i in range(2):
                    self.credentials.append(v[i].split('\'')[1].strip())
        except FileNotFoundError:
            print(
                'Failed to read file: \"' + filename + '\"',
                file = sys.stderr
            )

    def __ping_single_ip(self, host):
        result = local_access_run(['/bin/ping', '-c', '1', '-W', '32', host])
        try:
            result.check_returncode()
            return True
        except subprocess.CalledProcessError:
            return False

    def ping_all_prefix_ips(self):
        self.hosts = []
        for prefix in self.ip_prefixes:
            for suffix in range(256):
                self.hosts.append(prefix + str(suffix))
        job_list = []
        for host in self.hosts:
            job_list.append([self.__ping_single_ip, host])
        ans = []
        idx = -1
        results = multi_threaded_execution(256, job_list)
        for result in results:
            idx += 1
            print(
                'host: ' + self.hosts[idx] + ', ping: ' + str(result),
                file = sys.stderr
            )
            if result == True:
                ans.append(self.hosts[idx])
        self.hosts = ans

    def __get_os_single_ip(self, host):
        for command in self.commands_os:
            output = remote_access_run(host, command, self.credentials)
            if output == None:
                continue
            for os, hash in self.operational_systems.items():
                for line in output:
                    if line.find(os) != -1:
                        return hash
        return None

    def get_os_all_ips(self):
        job_list = []
        for host in self.hosts:
            job_list.append([self.__get_os_single_ip, host])
        ans = []
        idx = -1
        results = multi_threaded_execution(256, job_list)
        for result in results:
            idx += 1
            print(
                'host: ' + self.hosts[idx] + ', os: ' + str(result != None),
                file = sys.stderr
            )
            if results[idx] == None:
                continue
            ans.append((self.hosts[idx], results[idx]))
        self.hosts = ans

    def __get_single_loopback(self, host, hash):
        result = remote_access_run(host, self.commands_loopback[hash], self.credentials)
        if result == None:
            return None
        for s in result:
            if hash == 0:
                pos = s.find('address')
                if pos != -1:
                    for i in range(pos + 8, len(s)):
                        if s[i] == '/':
                            return s[pos + 8: i]
            else:
                pos = s.find('Loopback0')
                if pos != -1:
                    start = -1
                    for i in range(pos + 9, len(s)):
                        if start == -1 and s[i] != ' ':
                            start = i
                        elif start != -1 and (s[i] < '0' or s[i] > '9') and s[i] != '.':
                            return s[start: i]
        return None

    def get_all_loopback(self):
        job_list = []
        for host, hash in self.hosts:
            job_list.append([self.__get_single_loopback, host, hash])
        ans = []
        idx = -1
        results = multi_threaded_execution(256, job_list)
        for result in results:
            idx += 1
            print(
                'host: ' + self.hosts[idx][0] + ', loopback: ' + str(result == self.hosts[idx][0]),
                file = sys.stderr
            )
            if results[idx] == self.hosts[idx][0]:
                ans.append(self.hosts[idx])
        self.hosts = ans

    def __get_single_hardware(self, host, hash):
        if hash == 0:
            return remote_access_run(host, self.commands_hardware[hash], self.credentials)
        return None

    def get_all_hardware(self):
        job_list = []
        for host, hash in self.hosts:
            job_list.append([self.__get_single_hardware, host, hash])
        self.hardware = []
        idx = -1
        results = multi_threaded_execution(256, job_list)
        for result in results:
            idx += 1
            print(
                'host: ' + self.hosts[idx][0] + ', hardware: ' + str(result != None),
                file = sys.stderr
            )
            self.hardware.append(results[idx])

def main():
    servers_list = servers_structure(input())

    servers_list.ping_all_prefix_ips()

    print('ping_all_prefix_ips:')
    for i in servers_list.hosts:
        print(i)
    print()

    servers_list.get_os_all_ips()

    print('get_os_all_ips:')
    for i in servers_list.hosts:
        print(i)


    servers_list.get_all_loopback()

    for i in servers_list.hosts:
        print(i)
    print()

    servers_list.get_all_hardware()

    idx = -1
    for i in range(len(servers_list.hosts)):
        idx += 1
        print(servers_list.hosts[idx][0] + ': ' + str(servers_list.hardware[idx]))
    print()

def multi_threaded_execution(workers, job_list):
    ans = []
    threads = []
    with ThreadPoolExecutor(max_workers = workers) as executor:
        for parameters in job_list:
            threads.append(
                executor.submit(
                    parameters[0],
                    *parameters[1:]
                )
            )
    for thread in threads:
        ans.append(thread.result())
    return ans

def local_access_run(command):
    return subprocess.run(
        args = command,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
    )

def remote_access_run(hostname, command, credentials):
    allowed_errors = [
        '[Errno 104] Connection reset by peer',
    ]
    timeout = 32
    remaining_attempts = 128
    while remaining_attempts > 0:
        remaining_attempts -= 1
        with paramiko.SSHClient() as ssh:
            try:
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
                stdin, stdout, stderr = ssh.exec_command(
                    command,
                    timeout = timeout
                )
                ans = []
                for line in stdout.readlines():
                    ans.append(line.strip())
                return ans
            except Exception as exception:
                allowed = False
                s = str(exception)
                print(exception, file = sys.stderr)
                for error in allowed_errors:
                    if s.find(error) != -1:
                        allowed = True
                        break
                if allowed == False:
                    return None

main()