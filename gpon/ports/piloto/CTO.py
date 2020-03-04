class CTO:
    def __init__(self, loc="", est="", n=""):
        self.localidade = loc
        self.estacao = est
        self.nome = n

        self.quant = {
            "AUDITORIA": 0,
            "DEFEITO": 0,
            "DESIGNADO": 0,
            "OCUPADO": 0,
            "RESERVADO": 0,
            "VAGO": 0,
            "INSTALADAS": 0,
        }

    def __hash__(self):
        return hash(self.nome)

    def __lt__(self, other):
        if self.localidade != other.localidade:
            return self.localidade < other.localidade
        return self.nome < other.nome

    def __repr__(self):
        if self.quant["VAGO"] == 0:
            possibilidade_vendas = "Nao - Indisponibilidade de Portas na CTOE"
        else:
            possibilidade_vendas = "Sim - " + str(self.quant["VAGO"])

        return ';'.join([self.localidade, self.estacao, self.nome, possibilidade_vendas, str(self.quant["OCUPADO"]), str(self.quant["VAGO"]), str(self.quant["INSTALADAS"])])

    def add(self, status):
        try:
            self.quant[status] += 1
            self.quant["INSTALADAS"] += 1
        except KeyError:
            pass
            # print(f"status \"{status}\" not find")

    def as_a_tuple(self):
        return (
            self.localidade,
            self.estacao,
            self.nome,
            self.quant["AUDITORIA"],
            self.quant["DEFEITO"],
            self.quant["DESIGNADO"],
            self.quant["OCUPADO"],
            self.quant["RESERVADO"],
            self.quant["VAGO"],
            self.quant["INSTALADAS"],
        )
