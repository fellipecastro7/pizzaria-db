import sqlite3
from datetime import datetime

class RestauranteDB:
    def __init__(self):
        # Conecta ao banco de dados em memória (será apagado quando o programa terminar)
        self.conn = sqlite3.connect(":memory:")  # Usando o banco em memória
        self.cursor = self.conn.cursor()
        
        # Cria a tabela 'pedidos' no banco de dados em memória
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY,
                itens TEXT,
                valorTotal REAL,
                status TEXT,
                data_hora TEXT
            )
        ''')
        self.conn.commit()

    def criarPedido(self, itens, valorTotal):
        # Cria um novo pedido no banco de dados
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO pedidos (itens, valorTotal, status, data_hora)
            VALUES (?, ?, ?, ?)
        ''', (", ".join(itens), valorTotal, "preparando", data_hora))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna o ID do pedido criado

    def atualizarStatus(self, pedidoID, novoStatus):
        statusValidos = ["preparando", "pronto", "entregue"]  # Lista de status válidos
        if novoStatus.lower() not in statusValidos:
            return "Status inválido. Os status válidos são: 'preparando', 'pronto' ou 'entregue'."

        self.cursor.execute('''
            UPDATE pedidos SET status = ? WHERE id = ?
        ''', (novoStatus, pedidoID))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return f"Status do pedido {pedidoID} atualizado para '{novoStatus}'."
        else:
            return "Pedido não encontrado."

    def consultarPedido(self, pedidoID):
        self.cursor.execute('''
            SELECT * FROM pedidos WHERE id = ?
        ''', (pedidoID,))
        pedido = self.cursor.fetchone()
        if pedido:
            return {
                "id": pedido[0],
                "itens": pedido[1],
                "valorTotal": pedido[2],
                "status": pedido[3],
                "data_hora": pedido[4]
            }
        else:
            return "Pedido não encontrado"

    def removerPedido(self, pedidoID):
        self.cursor.execute('''
            DELETE FROM pedidos WHERE id = ?
        ''', (pedidoID,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return "Pedido removido."
        else:
            return "Pedido não encontrado."
        

    def consultarTodosPedidos(self):
        # Recupera todos os pedidos do banco de dados
        self.cursor.execute('SELECT * FROM pedidos')
        pedidos = self.cursor.fetchall()
        return [{
            "id": pedido[0],
            "itens": pedido[1],
            "valorTotal": pedido[2],
            "status": pedido[3],
            "data_hora": pedido[4]
        } for pedido in pedidos]


    def fechar_conexao(self):
        self.conn.close()  # Fecha a conexão com o banco de dados
    