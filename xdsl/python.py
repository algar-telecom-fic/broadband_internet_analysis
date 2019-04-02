# import pymysql

# def main():
#   db = pymysql.connect(
#     'localhost',
#     'peduardo',
#     'pe',
#     'kappacidade'
#   )
#   return 0

# main()

import mysql.connector

def main():
  db = mysql.connector.connect(
    host = 'localhost',
    user = 'peduardo',
    passwd = 'pe',
    database = 'kappacidade'
  )

main()