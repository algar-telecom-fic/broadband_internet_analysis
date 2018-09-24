import plotly.offline, openpyxl, datetime

tasks = []
input_path = 'input/'
output_path = 'output/'
people, squads = {}, {}
excel_file, first_date, last_date, limit = 0, 0, 0, 0

class node:
	def __init__(self, lo, hi):
		self.lo = lo
		self.hi = hi
		self.lazy = 0
		self.value = 0
		self.left = None
		self.right = None
		if self.lo == self.hi:
			return
		mid = (self.lo + self.hi) >> 1
		self.left = node(self.lo, mid)
		self.right = node(mid + 1, self.hi)
	def propagate(self):
		if self.lazy > 0:
			self.value += (self.hi - self.lo + 1) * self.lazy
			if self.lo != self.hi:
				self.left.lazy += self.lazy
				self.right.lazy += self.lazy
			self.lazy = 0
	def update(self, lo, hi, value):
		self.propagate()
		if self.lo > hi or self.hi < lo:
			return
		if self.lo >= lo and self.hi <= hi:
			self.lazy = value
			self.propagate()
			return
		self.left.update(lo, hi, value)
		self.right.update(lo, hi, value)
		self.value = self.left.value + self.right.value
	def query(self, lo, hi):
		self.propagate()
		if self.lo > hi or self.hi < lo:
			return 0
		if self.lo >= lo and self.hi <= hi:
			return self.value
		left = self.left.query(lo, hi)
		right = self.right.query(lo, hi)
		return left + right

def build_graph():
	global excel_file, output_path, first_date, limit
	sheet = excel_file.worksheets[0]
	graphs = {}
	for person in people:
		for task_idx in range(len(people[person]['tasks'])):
			i = people[person]['tasks'][task_idx]
			start = get_date(sheet.cell(row = i, column = 5).value)
			finish = get_date(sheet.cell(row = i, column = 6).value)
			current_date = start - datetime.timedelta(days = start.weekday())
			line = str(sheet.cell(row = i, column = 3).value).strip()
			project = str(sheet.cell(row = i, column = 2).value).strip()
			description = str(sheet.cell(row = i, column = 4).value).strip()
			info = ''
			if line != 'None':
				info += '(' + line + ')'
			if project != 'None':
				if len(info) > 0:
					info += ' '
				info += project
			if description != 'None':
				if len(info) > 0:
					info += ' '
				info += description
			info = info[0: min(len(info), 60)]
			while current_date < finish:
				x = current_date
				y = current_date + datetime.timedelta(days = 4)
				name = x.strftime('%d/%m/%Y') + ' - ' + y.strftime('%d/%m/%Y')
				if name not in graphs:
					graphs[name] = []
				graphs[name].append(plotly.graph_objs.Bar({
					'hoverinfo': 'x+name',
					'name': info,
					'opacity': 0.9,
					'orientation': 'v',
					'showlegend': True,
					'x': [person],
					'y': [1]
				}))
				current_date += datetime.timedelta(days = 7)
	for week in graphs:
		layout = plotly.graph_objs.Layout({
			'barmode': 'stack',
			'dragmode': 'pan',
			'font': {'color': 'black', 'family': 'Arial', 'size': 18},
			'legend': {'orientation': 'v'},
			'hovermode': 'closest',
			'hoverlabel': {'bgcolor': 'black', 'bordercolor': 'black', 'namelength': -1, 'font': {'color': 'white', 'family': 'Arial', 'size': 18}},
			'showlegend': False,
			'title': 'CTT Transporte (' + week + ')',
			'yaxis': {'title': 'Demandas'}
		})
		filename = ''
		qtd = (datetime.datetime.strptime(week[0:10], "%d/%m/%Y") - first_date).days + limit
		for c in week:
			if c == '/':
				filename += '-'
			else:
				filename += c
		plotly.offline.plot(plotly.graph_objs.Figure(data = graphs[week], layout = layout), filename = output_path + '(' + str(qtd) + ') ' + filename + '.html', auto_open = False)

def build_people():
	global excel_file, limit
	sheet = excel_file.worksheets[1]
	N_rows = sheet.max_row
	for i in range(2, N_rows + 1):
		name = sheet.cell(row = i, column = 1).value
		squad = sheet.cell(row = i, column = 2).value
		if name == None or squad == None:
			continue
		people[name] = {}
		people[name]['tasks'] = []
		people[name]['segtree'] = node(0, limit)
		if squad not in squads:
			squads[squad] = []
		squads[squad].append(name)

def get_date(s):
	if isinstance(s, str):
		start = 0
		finish = len(s)
		for i in range(len(s)):
			if (s[i] >= '0' and s[i] <= '9') or s[i] == '/':
				start = i
				break
		for i in range(start, len(s)):
			if s[i] != '/' and (s[i] < '0' or s[i] > '9'):
				finish = i - 1
				break
		s = s[start:finish]
		try:
			s = datetime.datetime.strptime(s, "%d/%m/%Y")
		except Exception:
			s = datetime.datetime.strptime(s, "%d/%m/%y")
	return s

def get_sheet_info():
	global excel_file, first_date, last_date, limit, input_path
	excel_file = openpyxl.load_workbook(input_path + 'input.xlsx')
	sheet = excel_file.worksheets[0]
	N_rows = sheet.max_row
	for i in range(1, N_rows + 1):
		start = sheet.cell(row = i, column = 5).value
		if isinstance(start, datetime.date):
			if first_date == 0:
				first_date = start
			else:
				first_date = min(first_date, start)
		finish = sheet.cell(row = i, column = 6).value
		if isinstance(finish, datetime.date):
			if last_date == 0:
				last_date = finish
			else:
				last_date = max(last_date, finish)
	limit = (last_date - first_date).days + 1

def read_sheet():
	global excel_file, first_date
	sheet = excel_file.worksheets[0]
	N_rows = sheet.max_row
	for i in range(2, N_rows + 1):
		if sheet.cell(row = i, column = 1).value == '*':
			continue
		if sheet.cell(row = i, column = 1).value == None:
			continue
		start = get_date(sheet.cell(row = i, column = 5).value)
		start = (start - first_date).days
		finish = get_date(sheet.cell(row = i, column = 6).value)
		finish = (finish - first_date).days
		value = sheet.cell(row = i, column = 8).value
		if value == '*':
			tasks.append((start, i))
		else:
			for person in value.split(','):
				person = person.strip()
				if person in people:
					people[person]['tasks'].append(i)
					people[person]['segtree'].update(start, finish, 1)

def solve():
	global excel_file, first_date, output_path
	sheet = excel_file.worksheets[0]
	N_rows = sheet.max_row
	tasks.sort()
	for task in range(len(tasks)):
		i = tasks[task][1]
		selected_people = []
		start = get_date(sheet.cell(row = i, column = 5).value)
		start = (start - first_date).days
		finish = get_date(sheet.cell(row = i, column = 6).value)
		finish = (finish - first_date).days
		for squad in sheet.cell(row = i, column = 1).value.split(','):
			squad = squad.strip()
			best_person = ''
			best_qtd = -1
			for person in squads[squad]:
				current = people[person]['segtree'].query(start, finish)
				if best_qtd == -1 or current < best_qtd:
					best_person = person
					best_qtd = current
			selected_people.append(best_person)
			people[best_person]['tasks'].append(i)
			people[best_person]['segtree'].update(start, finish, 1)
		professionals = ''
		for j in range(len(selected_people)):
			if j > 0:
				professionals += ' , '
			professionals += selected_people[j]
		sheet.cell(row = i, column = 8).value = professionals
	if not excel_file.views:
		excel_file.views.append(openpyxl.workbook.views.BookView())
	excel_file.save(output_path + 'output.xlsx')

def main():
	get_sheet_info()
	build_people()
	read_sheet()
	solve()
	build_graph()

main()