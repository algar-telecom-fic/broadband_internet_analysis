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
      + 'id INT AUTO_INCREMENT'
      + ', PRIMARY KEY (id)'
    + ')'
  )
  cursor.execute(
    'CREATE TABLE IF NOT EXISTS'
    + ' adsl'
    + ' ('
      + 'id INT AUTO_INCREMENT'
      + ', PRIMARY KEY (id)'
    + ')'
  )
  cursor.execute('SHOW TABLES')
  for i in cursor:
    print(i)

main()