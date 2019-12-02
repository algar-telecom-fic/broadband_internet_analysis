class City:
    def __init__(self, loc=""):
        self.localidade = loc
        self.ocupacao = 0
        self.capacidade = 0
        self.ocupacao_anterior = 0
        self.tx_crescimento_mensal = -1.0
        self.expectativa_esgotamento_meses = -1

    def add(self, status):
        if status == 'VAGO':
            self.capacidade += 1
        elif status == 'OCUPADO':
            self.ocupacao += 1

    def __repr__(self):
        s = f"{self.localidade};{self.ocupacao};{self.ocupacao_anterior};{self.tx_crescimento_mensal};{self.capacidade};"
        if self.expectativa_esgotamento_meses != 999999999:
            s += str(self.expectativa_esgotamento_meses)
        else:
            s += "Estavel"

        s+=";"

        return s

    def as_a_tuple(self):
        return (
            self.localidade,
            self.ocupacao,
            self.ocupacao_anterior,
            self.capacidade,
            self.tx_crescimento_mensal,
            self.expectativa_esgotamento_meses,
        )
