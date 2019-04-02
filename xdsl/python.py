import PyMySQL

def main():
  db = PyMySQL.connect(
    'localhost',
    'peduardo',
    'pe',
    'kappacidade'
  )
  return 0

main()