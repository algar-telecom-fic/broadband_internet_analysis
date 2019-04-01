from CTO import CTO
from UI import UIManager
from Cidades import Cidades
from CTO import CTO

class Main:
    def __init__(self):
        cidade_filename, dados_filename = UIManager().get_filenames()

        self.cidades = Cidades(cidade_filename)
        self.processaCSV(dados_filename)
        self.printaExpansao()

    def processaCSV(self, filename):
        with open(filename, 'r', encoding='ISO-8859-1') as input_file:

            self.concessao = []
            self.expansao  = []
            for line in input_file.readlines():
                attributes = line.split(';')

                localidade = str(attributes[14])
                estacao    = str(attributes[15])
                cto        = str(attributes[1])
                status     = str(attributes[13])

                cto = CTO(localidade, estacao, cto)
                if localidade in self.cidades.concessao:
                    if cto in self.concessao:
                        for i in range(len(self.concessao)-1, -1, -1):
                            if self.concessao[i] == cto:
                                self.concessao[i].addLeitura(status)
                                break
                    else:
                        self.concessao.append(cto)
                        self.concessao[-1].addLeitura(status)

                elif localidade in self.cidades.expansao:
                    if cto in self.expansao:
                        for i in range(len(self.expansao)-1, -1, -1):
                            if self.expansao[i] == cto:
                                self.expansao[i].addLeitura(status)
                                break
                    else:
                        self.expansao.append(cto)
                        self.expansao[-1].addLeitura(status)

    def printaExpansao(self):
        cont = 1
        for cto in self.expansao:
            print(f"{cont}: ", end="")
            for key, value in cto.dict.items():
                print(f"{value}, ", end="")
            print()
            cont+=1
