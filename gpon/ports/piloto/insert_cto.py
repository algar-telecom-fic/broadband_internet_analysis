from Database import Database
from datetime import datetime


def insert_cto(cto_data, hoje = datetime.now()):


    cto_tuples = []
    for cto in cto_data:
        cto_tuples.append( cto_data[cto].as_a_tuple() + (hoje,) )

    query = """insert into Portas_CTO(localidade, estacao, nome_cto, auditoria, defeito, designado, ocupado, reservado, vago, total, dia)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    db = Database()
    db.executaQuery(query, cto_tuples)
