import mysql.connector

def main():
  db = mysql.connector.connect(
    host = 'localhost',
    user = 'peduardo',
    passwd = 'pe',
    database = 'kappacidade'
  )
  cmd = (
    'CREATE TABLE IF NOT EXISTS'
    + ' xdsl'
    + ' ('
      + 'task_id INT AUTO_INCREMENT,'
      + 'PRIMARY KEY'
      + ' ('
        + 'task_id'
      + ')'
    + ')'
  )
  print(cmd)
  cursor = db.cursor()
  cursor.execute(
    cmd
  )
  cursor.execute('SHOW TABLES')
  for i in cursor:
    print(i)

main()