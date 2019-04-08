import abc
import datetime

class XDSL(abc.ABC):
  date = datetime.datetime.utcnow()

  @abc.abstractmethod
  def add_port(self):
    pass

  @abc.abstractmethod
  def build_mongodb(self):
    pass