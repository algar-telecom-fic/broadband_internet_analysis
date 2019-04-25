#filename = 'datasheets/faixa_minimizado.csv'
filename = 'datasheets/FAIXA_STFC_20190406_2988_GERAL.txt'


database = {}

with open(filename, 'r', encoding='ISO-8859-1') as input_file:

    encountered_yet = False

    for line in input_file.readlines():
        attributes = line.split(';')
        nomePrestadora = attributes[0];

        if nomePrestadora == 'ALGAR TELECOM S/A':
            encountered_yet = True

            ddd          = attributes[2]
            prefixo      = attributes[3]
            faixaInicial = attributes[4]
            faixaFinal   = attributes[5]
            cidade       = attributes[8]

            if cidade not in database:
                database[cidade] = 0

            diff = int(faixaFinal) - int(faixaInicial) + 1

            database[cidade]+=diff
            #print(f"{nomePrestadora}\t{ddd}\t{prefixo}\t{faixaInicial}\t{faixaFinal}")
        elif encountered_yet:
            break


for chave, item in database.items():
    print("" + chave + ", " + str(item))
