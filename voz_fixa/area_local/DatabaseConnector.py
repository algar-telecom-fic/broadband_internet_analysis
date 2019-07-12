import configparser
import mysql.connector

class DatabaseConnector:

    def configureDB(self, configFilename):
        self.config = configparser.ConfigParser()
        self.config.read(configFilename)
        print("meu config object: ")
        print(self.config)
        self.config = self.config['DB']
        
    def conectaBancodeDados(self):
        self.conn = mysql.connector.connect(host     = self.config['DB_HOST'],
                                            database = self.config['DB_NAME'],
                                            user     = self.config['DB_USER'],
                                            password = self.config['DB_PSWD'])

    def executaQuery(self, query, args=[]):
        self.conectaBancodeDados()
        cursor = self.conn.cursor()
        if args == []:
            cursor.execute(query)
        else:
            cursor.executemany(query, args)

        try:
            results = cursor.fetchall()
            self.conn.close()
            return results
        except:
            pass

        self.conn.commit()
        self.conn.close()
