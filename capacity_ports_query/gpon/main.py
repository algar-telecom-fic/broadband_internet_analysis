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
def build_database(concession_type):
    global database

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
    database[concession_type] = v
 

def build_excel_file(concession_type):
    global database, excel_file
    from openpyxl import Workbook
    

    excel_file = Workbook()
    
    build_styles()
    build_relatorioAtual(concession_type)
    excel_file.create_sheet()
    build_PortaCTOE(concession_type)
    
    if concession_type == 'concession':
        filename = 'datasheets/saidaCN.xlsx'
    else:
        filename = 'datasheets/saidaEX.xlsx'
        
    print(filename)
    excel_file.save(filename)


def build_styles():
    global excel_file
    from openpyxl.styles import NamedStyle, Font, PatternFill, Alignment, Border, Side

    alignment = Alignment(
        horizontal = 'center',
        vertical = 'center',
    )
    
    border = Border(
		left = Side(style = 'thin'),
		right = Side(style = 'thin'),
		top = Side(style = 'thin'),
		bottom = Side(style = 'thin'),
	)
    
    font = Font(
        bold = True,
        color = '000000',
        name = 'Calibri',
        size = 11,
    )
    
    top_style = NamedStyle('top_style')
    top_style.alignment = alignment
    top_style.font = font
    top_style.border = border
    excel_file.add_named_style(top_style)

    normal_style = NamedStyle('normal_style')
    normal_style.border = border
    excel_file.add_named_style(normal_style)
    
    center_style = NamedStyle('center_style')
    center_style.alignment = alignment
    center_style.border = border
    excel_file.add_named_style(center_style)

def build_relatorioAtual(concession_type):
    from openpyxl.styles import PatternFill
    sheet = excel_file.worksheets[-1]
    sheet.title = 'RelatórioAtual'
    
    num_columns = 9
    sheet.cell(row = 1, column = 1).value = 'LOCALIDADE'
    sheet.cell(row = 1, column = 2).value = 'ESTACAO'
    sheet.cell(row = 1, column = 3).value = 'CTO'
    sheet.cell(row = 1, column = 4).value = 'DEFEITO'
    sheet.cell(row = 1, column = 5).value = 'DESIGNADO'
    sheet.cell(row = 1, column = 6).value = 'OCUPADO'
    sheet.cell(row = 1, column = 7).value = 'RESERVADO'
    sheet.cell(row = 1, column = 8).value = 'VAGO'
    sheet.cell(row = 1, column = 9).value = 'Total Geral'
    
    #this is to change the color of the cells from the first row
    for i in range(1, num_columns+1):
        sheet.cell(row = 1, column = i).fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid') 
    
    current_row = 2
    for reg in database[concession_type]:
        sheet.cell(row = current_row, column = 1).value = reg.locale
        sheet.cell(row = current_row, column = 2).value = reg.station
        sheet.cell(row = current_row, column = 3).value = reg.cto
        sheet.cell(row = current_row, column = 4).value = reg.defeito
        sheet.cell(row = current_row, column = 5).value = reg.designado
        sheet.cell(row = current_row, column = 6).value = reg.ocupado
        sheet.cell(row = current_row, column = 7).value = reg.reservado
        sheet.cell(row = current_row, column = 8).value = reg.vago
        sheet.cell(row = current_row, column = 9).value = reg.total
        
        current_row+=1
    

def build_PortaCTOE(concession_type):
    from openpyxl.styles import PatternFill
    sheet = excel_file.worksheets[-1]
    sheet.title = '1-Porta CTOE'
    
    num_columns = 7
    sheet.cell(row = 1, column = 1).value = 'LOCALIDADE'
    sheet.cell(row = 1, column = 2).value = 'ESTACAO'
    sheet.cell(row = 1, column = 3).value = 'CTO'
    sheet.cell(row = 1, column = 4).value = 'Possibilidade de Vendas'
    sheet.cell(row = 1, column = 5).value = 'Capacidade CTOE'

    sheet.cell(row = 2, column = 5).value = 'Ocupado'
    sheet.cell(row = 2, column = 6).value = 'Disponível'
    sheet.cell(row = 2, column = 7).value = 'Instalado'
    
    sheet.merge_cells('A1:A2')
    sheet.merge_cells('B1:B2')
    sheet.merge_cells('C1:C2')
    sheet.merge_cells('D1:D2')
    
    sheet.merge_cells('E1:G1')
    
    for i in range(1, num_columns+1):
        sheet.cell(row = 1, column = i).style = 'top_style'
        sheet.cell(row = 2, column = i).style = 'top_style'
        
    
    #blue cells
    sheet.cell(row = 1, column = 1).fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
    sheet.cell(row = 1, column = 2).fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
    
    #yellow cells
    sheet.cell(row = 1, column = 3).fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid') 
    sheet.cell(row = 1, column = 4).fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
    
    #green cells
    sheet.cell(row = 1, column = 5).fill = PatternFill(start_color='A9D08E', end_color='A9D08E', fill_type='solid')
    
    #~the forth collor~
    sheet.cell(row = 2, column = 5).fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
    sheet.cell(row = 2, column = 6).fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
    sheet.cell(row = 2, column = 7).fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
    
    
    current_row = 3
    for reg in database[concession_type]:
        sheet.cell(row = current_row, column = 1).value = reg.locale
        sheet.cell(row = current_row, column = 1).style = 'normal_style'
        
        sheet.cell(row = current_row, column = 2).value = reg.station
        sheet.cell(row = current_row, column = 2).style = 'normal_style'
        
        sheet.cell(row = current_row, column = 3).value = reg.cto
        sheet.cell(row = current_row, column = 3).style = 'normal_style'
        
        sheet.cell(row = current_row, column = 4).value = ("Sim - %s" % reg.vago) if (int(reg.vago) > 0) else "Não - Indisponibilidade CTOE"
        sheet.cell(row = current_row, column = 4).style = 'center_style'
        
        sheet.cell(row = current_row, column = 5).value = int(reg.designado) + int(reg.ocupado)
        sheet.cell(row = current_row, column = 5).style = 'center_style'
        
        sheet.cell(row = current_row, column = 6).value = reg.vago
        sheet.cell(row = current_row, column = 6).style = 'center_style'
        
        sheet.cell(row = current_row, column = 7).value = reg.total
        sheet.cell(row = current_row, column = 7).style = 'center_style'
        
        current_row+=1
        
    
#this class just wrap all the usefull information
#it serves mostly just to ordenate the results
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
            


#this file contains the relation between the cities and each concession type
def read_concession_file(filename):
    from openpyxl import load_workbook

    #loading the file from the disc
    wb = load_workbook(filename)
    #selectin the right sheet
    ws = wb['todas_localidades_existentes']

    #both lists start empty
    concession = []
    expansion  = []

    #getting the max number of rows
    num_rows = ws.max_row
    
    #iterating for all the rows of the sheet
    for i in range(2, num_rows+1):
        #separating the city and the concession type
        locale = ws.cell(row=i, column=1).value
        locale_type = ws.cell(row=i, column=2).value 
        
        #depending of the type, we append the locale to the right list
        if locale_type == 'CONCESSÃO':
            concession.append(locale)
        else:
            expansion.append(locale)
    
    #returning the two lists
    return (concession, expansion)


def main():
    global database
    database = {}

    concession_filename = 'datasheets/CNxEX_MOLDE.xlsx'
    concession_lists = read_concession_file(concession_filename)

    filename='datasheets/Circuitos CTO-01-25.csv'
    read_file(filename, concession_lists[0], concession_lists[1])

    build_database('concession')
    build_database('expansion')

    build_excel_file('concession')
    build_excel_file('expansion')



main()




"""
PERGUNTAR SOBRE:
    AUDITORIA
    DIFERENÇA DE LINHAS ENTRE RELATORIO ATUAL E PORTA CTOE EXPANSAO
    PORTA CTOE: CTOE.ocupado = relatorio.ocupado + relatorio.designado
"""






