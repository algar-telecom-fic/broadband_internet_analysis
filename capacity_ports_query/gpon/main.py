

#function to add the data from the file to the database
def add_port(concession_type, locale, station, cto, status):
    #using the global database
    global database
    
    #if any of these values is not in the dictionary yet, create the it's dictionary
    if locale not in database[concession_type]:
        database[concession_type][locale] = {}
    if station not in database[concession_type][locale]:
        database[concession_type][locale][station] = {}
        
    
    #the cto dictionary is where we're gonna count the registers by their status 
    if cto not in database[concession_type][locale][station]:
        database[concession_type][locale][station][cto] = {
            'DEFEITO':   0,
            'DESIGNADO': 0,
            'OCUPADO':   0,
            'RESERVADO': 0,
            'VAGO':      0,
            'AUDITORIA': 0,
            'total':     0,
        }
    
    #all lines add in the total
    database[concession_type][locale][station][cto]['total'] += 1
    
    #each line also adds in it's own status
    database[concession_type][locale][station][cto][status] += 1

#function to show everything in the database similarly to the spreadsheet
def generate_sheet(concession_type):
    global database

    if concession_type == 'concession':
        filename = 'datasheets/saidaCN.csv'
    else:
        filename = 'datasheets/saidaEX.csv'
    
    print(filename)
    v = []
    for locale in database[concession_type]:
        for station in database[concession_type][locale]:
            for cto in database[concession_type][locale][station]:              
                        v.append(
                            data(
                                locale,
                                station,
                                cto,
                                database[concession_type][locale][station][cto]['DEFEITO'],
                                database[concession_type][locale][station][cto]['DESIGNADO'],
                                database[concession_type][locale][station][cto]['OCUPADO'],
                                database[concession_type][locale][station][cto]['RESERVADO'],
                                database[concession_type][locale][station][cto]['VAGO'],
                                database[concession_type][locale][station][cto]['total'],         
                            )
                        )
    v.sort()
    
 
    out_file = open(filename, "w")
    out_file.write("Rótulos de Linha,ESTACAO,CTO,DEFEITO,DESIGNADO,OCUPADO,RESERVADO,VAGO,Total Geral\n")
    for reg in v:
        out_file.write(str(reg) + "\n")
                        
    out_file.close()
    
class data:
    def __init__(self, locale, station, cto, defeito, designado, ocupado, reservado, vago, total):
        self.locale = locale
        self.station = station
        self.cto = cto
        self.defeito = defeito
        self.designado = designado
        self.ocupado = ocupado
        self.reservado = reservado
        self.vago = vago
        self.total = total
        
    def __lt__(self, other):
        if self.locale != other.locale:
            return self.locale < other.locale
        if self.station != other.station:
            return self.station < other.station
        return self.cto < other.cto
    
    def __repr__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s,%s,"%(
            self.locale,
            self.station,
            self.cto,
            self.defeito,
            self.designado,
            self.ocupado,
            self.reservado,
            self.vago,
            self.total,
        )
  
#function for extrating the useful data from the file
def read_file(filename, concession, expansion):
    
    #declaring the database as global will help we use it across different functions 
    global database
    
    database['concession'] = {}
    database['expansion'] = {}
    
    #open the file
    with open(filename, 'r',  encoding = 'ISO-8859-1') as input_file:

        #iterate for all the lines
        for line in input_file.readlines():

            #split the csv by the semi-colon
            v = line.split(';')
            
            #take the cto status form the list
            status_cto = str(v[4]).strip()
            #we must consider only the existing CTO
            if status_cto == "EXISTENTE":
                #separate the important properties
                locale = str(v[14]).strip()
                station = str(v[15]).strip()
                cto = str(v[1]).strip()     
                status = str(v[13]).strip()    
                
                #printing in the screen just for debug purposes
                #print("%s %s %s %s" %(locale, station, cto, status))
                
                if locale in concession:
                    #add this line's data to the database
                    add_port('concession', locale, station, cto, status)
                elif locale in expansion:
                    add_port('expansion', locale, station, cto, status)
            


def read_concession_file(filename):
    from openpyxl import load_workbook

    wb = load_workbook(filename)
    ws = wb['todas_localidades_existentes']

    concession = []
    expansion  = []

    num_rows = ws.max_row
    for i in range(2, num_rows+1):
        locale = ws.cell(row=i, column=1).value
        locale_type = ws.cell(row=i, column=2).value 
        
        #print("%s %s"%(locale, locale_type))
        
        if locale_type == 'CONCESSÃO':
            concession.append(locale)
        else:
            expansion.append(locale)
    
    return (concession, expansion)


def main():
    global database
    database = {}

    concession_filename = 'datasheets/CNxEX_MOLDE.xlsx'
    concession_lists = read_concession_file(concession_filename)

    filename='datasheets/Circuitos CTO-01-25.csv'
    read_file(filename, concession_lists[0], concession_lists[1])

    generate_sheet('concession')
    generate_sheet('expansion')





main()




"""
PERGUNTAR SOBRE:
    AUDITORIA
    DIFERENÇA DE LINHAS ENTRE RELATORIO ATUAL E PORTA CTOE EXPANSAO
    PORTA CTOE: CTOE.ocupado = relatorio.ocupado + relatorio.designado
"""






