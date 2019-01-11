import paramiko
import threading
import subprocess
from os import sys
from concurrent.futures import ThreadPoolExecutor

lock = threading.Lock()

class servers_structure:

  # ~ def __get_single_hardware(self, host, hash):
    # ~ return remote_access_run(host, self.commands_hardware[hash], self.credentials)

  def __get_single_hostname(self, ip):
    result = local_access_run([
      'snmpget',
      '-v', '2c',
      '-c', 'V01prO2005',
      ip,
      'sysName.0'
    ])
    return result.stdout.decode('utf-8').strip()[32:]

  def __get_single_loopback(self, ip, os):
    result = remote_access_run(ip, self.commands_loopback[os], self.credentials)
    if result != None:
      for s in result:
        if os == 0:
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

  def __get_single_os(self, ip):
    for command in self.commands_os:
      output = remote_access_run(ip, command, self.credentials)
      if output == None:
        continue
      for os, v in self.operational_systems.items():
        for line in output:
          if line.find(os) != -1:
            return v
    return -1

  def __get_single_ping(self, ip):
    result = local_access_run([
      '/bin/ping',
      '-c', '1',
      '-W', '32',
      ip
    ])
    try:
      result.check_returncode()
      return True
    except subprocess.CalledProcessError:
      return False

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
    self.credentials = []
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
    self.info = {}
    for prefix in self.ip_prefixes:
      for suffix in range(256):
        self.info[prefix + str(suffix)] = {}
    try:
      with open(filename, 'r') as file:
        v = file.readlines()
        for i in range(2):
          self.credentials.append(v[i].split('\'')[1].strip())
    except FileNotFoundError:
      print(
        'Failed to read file: \"' + filename + '\"',
        file = sys.stderr
      )

  # ~ def get_all_hardware(self):
    # ~ jobs = []
    # ~ for host, hash in self.hosts:
      # ~ jobs.append([self.__get_single_hardware, host, hash])
    # ~ self.hardware = []
    # ~ idx = -1
    # ~ results = multi_threaded_execution(jobs, 256)
    # ~ for result in results:
      # ~ idx += 1
      # ~ print(
        # ~ 'host: ' + self.hosts[idx][0] + ', hardware: ' + str(result != None),
        # ~ file = sys.stderr
      # ~ )
      # ~ self.hardware.append(results[idx])

  def get_all_hostname(self):
    jobs = []
    for ip, v in self.info.items():
      if 'loopback' in v and v['loopback'] == True:
        jobs.append([self.__get_single_hostname, ip])
        results = multi_threaded_execution(jobs)
        for result, job in zip(results, jobs):
          self.info[job[1]]['hostname'] = result

  def get_all_loopback(self):
    jobs = []
    for ip, v in self.info.items():
      if 'os' in v and v['os'] != -1:
        jobs.append([self.__get_single_loopback, ip, v['os']])
    results = multi_threaded_execution(jobs)
    for result, job in zip(results, jobs):
      self.info[job[1]]['loopback'] = (job[1] == result)

  def get_all_os(self):
    jobs = []
    for ip, v in self.info.items():
      if 'ping' in v and v['ping'] == True:
        jobs.append([self.__get_single_os, ip])
    results = multi_threaded_execution(jobs)
    for result, job in zip(results, jobs):
      self.info[job[1]]['os'] = result

  def get_all_ping(self):
    jobs = []
    for ip in self.info:
      jobs.append([self.__get_single_ping, ip])
    results = multi_threaded_execution(jobs)
    for result, job in zip(results, jobs):
      self.info[job[1]]['ping'] = result

  def print(self):
    for ip, v in self.info.items():
      print('ip: ' + ip)
      print(' ' + str(v))

def local_access_run(command):
  return subprocess.run(
    args = command,
    stdout = subprocess.PIPE,
    stderr = subprocess.STDOUT,
  )

def main():
  equipments = servers_structure(input())
  equipments.get_all_ping()
  equipments.get_all_os()
  equipments.get_all_loopback()
  equipments.get_all_hostname()
  # equipments.get_all_hardware()
  equipments.print()

def multi_threaded_execution(jobs, workers = 256):
  ans = []
  threads = []
  with ThreadPoolExecutor(max_workers = workers) as executor:
    for parameters in jobs:
      threads.append(
        executor.submit(
          parameters[0],
          *parameters[1:]
        )
      )
  for thread in threads:
    ans.append(thread.result())
  return ans

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
          ans.append(line)
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