from CTO import CTO
from UI import UIManager
from Cidades import Cidades
from Database import Database
from datetime import datetime

class Main:

    def __init__(self):
        cidade_filename, dados_filename = UIManager().get_filenames()

        self.cidades = Cidades(cidade_filename)
        self.processaCSV(dados_filename)
        self.printaExpansao()
        self.insereDados()

    def processaCSV(self, filename):
        with open(filename, 'r', encoding='ISO-8859-1') as input_file:

            self.concessao = {}
            self.expansao  = {}
            for line in input_file.readlines():
                attributes = line.split(';')

                localidade = str(attributes[14])
                estacao    = str(attributes[15])
                cto        = str(attributes[1])
                status     = str(attributes[13])

                if localidade in self.cidades.concessao:
                    if cto in self.concessao:
                        self.concessao[cto].addLeitura(status)
                    else:
                        self.concessao[cto] = CTO(localidade, estacao, cto)
                        self.concessao[cto].addLeitura(status)

                elif localidade in self.cidades.expansao:
                    if cto in self.expansao:
                        self.expansao[cto].addLeitura(status)
                    else:
                        self.expansao[cto] = CTO(localidade, estacao, cto)
                        self.expansao[cto].addLeitura(status)

    def printaExpansao(self):
        cont = 1
        for nome, cto in self.expansao.items():
            print(f"{cont}: ", end="")
            for key, value in cto.dict.items():
                print(f"{value}, ", end="")
            print()
            cont+=1

    def insereDados(self):
        argsCn = []
        for nome, cto in self.concessao.items():
            argsCn.append(
                (datetime.utcnow(),) + cto.as_a_tuple()
            )

        argsEx = []
        for nome, cto in self.expansao.items():
            argsEx.append(
                (datetime.utcnow(),) + cto.as_a_tuple()
            )

        db = Database('dbconfigs.env')

        query = """INSERT INTO concessao (dia, local, estacao, cto, defeito, designado, reservado, ocupado, vago, total)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        db.executaQuery(query, argsCn)

        query = """INSERT INTO expansao (dia, local, estacao, cto, defeito, designado, reservado, ocupado, vago, total)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        db.executaQuery(query, argsEx)
