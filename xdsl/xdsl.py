import abc
import datetime
import sys
sys.path.append('/home/gardusi/github/broadband_internet_analysis/')
import mysql_gardusi

class XDSL(abc.ABC):
  database_name = 'kappacidade',
  date = datetime.datetime.utcnow(),
  host = '0.0.0.0',
  passwd = 'pe',
  primary_key = 'id',
  user = 'peduardo',

  @abc.abstractmethod
  def add_port(self):
    pass

  @abc.abstractmethod
  def build_documents(self):
    pass

  def insert_documents(self):
    db = mysql_gardusi.mySQL(
      self.host,
      self.user,
      self.passwd,
      self.database_name,
    )
    db.create_table(
      primary_key = self.primary_key,
      table_info = table_info,
      table_name = table_name,
    )
    db.insert_into(
      self.table_name,
      self.table_info,
      self.documents,
    )