import adsl
import os
import vdsl

def main():
  filepath = os.path.dirname(os.path.abspath(__file__))
  current_filepath, previous_filepath, date_difference = read_config_file(filepath + '/config.txt')
  current_adsl, current_vdsl = read_file(current_filepath)
  previous_adsl, previous_vdsl = read_file(previous_filepath)
  current_adsl.build_mongodb(previous_adsl, date_difference)
  current_vdsl.build_mongodb(previous_vdsl, date_difference)

def read_config_file(filepath):
  with open(filepath, 'r', encoding = 'ISO-8859-1') as config_file:
    v = config_file.readlines()
    current_file = v[0].split('=')[1].strip().split('"')[1].strip()
    previous_file = v[1].split('=')[1].strip().split('"')[1].strip()
    date_difference = int(v[2].split('=')[1].strip().split('"')[1].strip())
    return (current_file, previous_file, date_difference)

def read_file(filepath):
  technologies = (adsl.ADSL(), vdsl.VDSL())
  with open(filepath, 'r', encoding = 'ISO-8859-1') as input_file:
    for line in input_file.readlines():
      v = line.split(';')
      for technology in technologies:
        technology.add_port(v)
  return technologies

main()

# import sys
# sys.path.append('/home/gardusi/github/broadband_internet_analysis/')
# import sql