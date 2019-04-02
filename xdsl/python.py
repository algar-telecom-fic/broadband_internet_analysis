import mysql.connector

def main():
  db = mysql.connector.connect(
    host = 'localhost',
    user = 'peduardo',
    passwd = 'pe',
    database = 'kappacidade'
  )
  cursor = db.cursor()
  cursor.execute(
    'CREATE TABLE IF NOT EXISTS'
    + ' xdsl'
    + ' ('
      + 'task_id INT AUTO_INCREMENT'
    + ')'
  )
  cursor.execute('SHOW TABLES')
  for i in cursor:
    print(i)

main()