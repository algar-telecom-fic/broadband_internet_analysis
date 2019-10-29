from Database import Database
from datetime import datetime

def insert_city(city_data,hoje = datetime.now()):

    city_tuples = []
    for city in city_data:
        city_tuples.append( city_data[city].as_a_tuple() + (hoje,) )

    query = """
            insert into Localidades(
                localidade,
                ocupacao_atual,
                ocupacao_anterior,
                capacidade_atual,
                tx_crescimento_mensal,
                expectativa_esgotamento_meses,
                dia
            )
            values (%s, %s, %s, %s, %s, %s, %s);
            """

    db = Database()
    db.executaQuery(query, city_tuples)
