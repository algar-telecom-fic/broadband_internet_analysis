import pymysql

def main():
  db = pymysql.connect(
    'localhost',
    'peduardo',
    'pe',
    'kappacidade'
  )
  return 0

main()