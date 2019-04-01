class CTO:
    def __init__(self, l, e, c, df=0, ds=0, o=0, r=0, v=0, t=0):
        self.dict = {}
        self.dict['LOCALIDADE'] = l
        self.dict['ESTACAO']    = e
        self.dict['CTO']        = c
        self.dict['DEFEITO']    = df
        self.dict['DESIGNADO']  = ds
        self.dict['OCUPADO']    = o
        self.dict['RESERVADO']  = r
        self.dict['VAGO']       = v
        self.dict['TOTAL']      = t

    def __eq__(self, other):
        return self.dict['CTO'] == other.dict['CTO']

    def __getitem__(self, item):
        return self.dict[item]

    def __repr__(self):
        return f"< {self.dict['LOCALIDADE']}, {self.dict['ESTACAO']}, {self.dict['CTO']} >"

    def __lt__(self, other):
        return self.dict['CTO'] < other.dict['CTO']

    def addLeitura(self, status):
        self.dict[status]+=1
