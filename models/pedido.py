class Pedido:
    def __init__(self, id, itens, valor_total, status, data_hora):
        self.id = id
        self.itens = itens
        self.valor_total = valor_total
        self.status = status
        self.data_hora = data_hora