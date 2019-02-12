from abc import ABC
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from os import sys
import paramiko
# import pymongo
import subprocess
import threading

class Router(ABC):
  def __init__(self, ip):
    self.ip = ip

  def valid(self, ip, credentials, key):
    output = remote_access_run(ip, command, credentials)
    if output == None:
      return False
    for line in output:
      if line.find(key) != -1:
        return True
    return False

class Juniper(Router):
  def __init__(self, ip):
    super().__init__(ip)
    manufacturer = 'Juniper'

  def valid(self, ip, credentials):
    return super().valid(ip, credentials, 'JUNOS')

class Cisco_XR(Router):
  manufacturer = 'Cisco-XR'
  
class Cisco_XE(Router):
  manufacturer = 'Cisco-XE'

class Huawei(Router):
  manufacturer = 'Huawei'

def build(credentials_filepath):
  ip_prefixes = [
    '189.39.3.',
    '200.225.196.',
    '200.225.199.',
    '200.225.200.',
    '200.225.254.',
  ]
  ips = []
  jobs = []
  for prefix in ip_prefixes:
    for suffix in range(256):
      ip = prefix + str(suffix)
      ips.append(ip)
      jobs.append([guess, ip, credentials])
  results = multi_threaded_execution(jobs)
  for result in results:
    if result != None:
      print(result.os)

def guess(ip):
  pass

def main():
  build(input())
  pass

def local_access_run(command):
  return subprocess.run(
    args = command,
    stdout = subprocess.PIPE,
    stderr = subprocess.STDOUT,
  )

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