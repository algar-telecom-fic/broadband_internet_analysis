from process import ProcessFile
from datetime import datetime
from insert_cto import insert_cto
from insert_city import insert_city
from Database import Database
from math import ceil
import os


def gera_relatorio(cto_data, city_data, hoje):
    with open(os.path.abspath("../gpon/ports/piloto/data/Portas_CTO_") + hoje.strftime("%d-%m-%Y") + ".csv", "w") as f:
        f.write("Localidade;Estação;CTO;Possibilidade de vendas;Portas CTO - Ocupada;Portas CTO - Disponível;Portas CTO - Instalada\n")
        for cto in sorted(cto_data.items(), key= lambda kv:(kv[1], kv[0])):#ordenar dicionario pelos items e nao pelas chaves
            f.write(str(cto[1]) + '\n')

    with open(os.path.abspath("../gpon/ports/piloto/data/Taxa_crescimento_") + hoje.strftime("%d-%m-%Y") + ".csv", "w") as f:
        f.write("Localidade;Ocupação Atual;Ocupação Anterior;Tx Crescimento Mensal;Capacidade Atual;Expectativa de Esgotamento em Meses;Visão de Capacidade\n")
        for city in sorted(city_data.items()):
            f.write(str(city[1]))
            if city[1].expectativa_esgotamento_meses < 0:
                f.write("Decrescimento")
            elif city[1].expectativa_esgotamento_meses == 0:
                f.write("Esgotado")
            elif city[1].expectativa_esgotamento_meses == 999999999:
                f.write("Estavel")
            elif city[1].expectativa_esgotamento_meses >= 10:
                f.write("Esgota em mais de 10 meses")
            else:
                f.write(f"Esgota em até {int(ceil(city[1].expectativa_esgotamento_meses))} meses")
            f.write('\n')


def calcula_crescimento(city_data, hoje):

    query = """select localidade, ocupacao_atual, dia from Localidades where dia = (select MAX(dia) from Localidades);"""

    db = Database()
    old_cities = db.executaQuery(query)

    _, _, data_anterior = old_cities[0]


    old_ocupacao = {}
    for register in old_cities:
        localidade, ocupacao_anterior, _ = register
        old_ocupacao[localidade] = ocupacao_anterior

    date_difference = float((hoje - data_anterior).days)

    for city in city_data:
        ocp_atual = city_data[city].ocupacao
        city_data[city].ocupacao_anterior = old_ocupacao.get(city, 0)
        city_data[city].tx_crescimento_mensal = ( 30.0 * (ocp_atual - old_ocupacao.get(city, 0) ) / date_difference)
        print(f"{city} deu tx_crescimento_mensal = {city_data[city].tx_crescimento_mensal}")
        try:
            city_data[city].expectativa_esgotamento_meses = city_data[city].capacidade / city_data[city].tx_crescimento_mensal
        except:
            print(f"erro no calc {city}")
            city_data[city].expectativa_esgotamento_meses = 999999999


def main(filename, hoje = datetime.now()):
    p = ProcessFile(filename)
    cto_data, city_data = p.run()

    calcula_crescimento(city_data, hoje)
    gera_relatorio(cto_data, city_data, hoje)
    insert_city(city_data, hoje)
    insert_cto(cto_data, hoje)

if __name__ == "__main__":
    main("/home/pediogo/broadband_internet_analysis/gpon/ports/piloto/data/Circuitos CTO-10-11.csv", datetime(2019, 10, 11))
