"""from openpyxl import load_workbook

wb = load_workbook('datasheets/CNxEX_MOLDE.xlsx')
ws = wb['todas_localidades_existentes']

concession = []
expansion  = []

num_rows = ws.max_row
for i in range(2, num_rows):
    locale = ws.cell(row=i, column=1).value
    locale_type = ws.cell(row=i, column=2).value 
    
    #print("%s %s"%(locale, locale_type))
    
    if locale_type == 'CONCESSÃO':
        concession.append(locale)
    else:
        expansion.append(locale)

print(len(concession))
print(len(expansion))

"""

f = open('datasheets/saida.txt', 'w')
print(f)

