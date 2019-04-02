import mysql.connector

def main():
  db = mysql.connector.connect(
    host = 'localhost',
    user = 'peduardo',
    passwd = 'pe',
    database = 'kappacidade'
  )
  cursor = db.cursor()
  cursor.execute('SHOW TABLES')
  for i in cursor:
    print(i)

main()