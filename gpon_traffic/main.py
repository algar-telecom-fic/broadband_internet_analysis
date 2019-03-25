import datetime
import os
import pymongo

class GPON:
  database = {}

  def __init__(self, filepath):
    with open(filepath, 'r', encoding = 'ISO-8859-1') as config_file:
      v = config_file.readlines()
      self.filepath_ports = v[0].split('=')[1].strip().split('"')[1].strip()
      self.filepath_current = v[1].split('=')[1].strip().split('"')[1].strip()
      self.filepath_previous = v[2].split('=')[1].strip().split('"')[1].strip()
      self.date_difference = v[3].split('=')[1].strip().split('"')[1].strip()

  def read_ports(self):
    pass

def main():
  gpon = GPON(os.path.dirname(os.path.abspath(__file__)) + '/' + 'config.txt')
  gpon.read_ports()
  print(gpon.filepath_ports)
  print(gpon.filepath_current)
  print(gpon.filepath_previous)
  print(gpon.date_difference)

main()