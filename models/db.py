import sqlite3
from datetime import datetime
from models.cardapio import CardapioItem
from models.pedido import Pedido

class PizzariaDB:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")


        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        cpf TEXT
    )
''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY,
                itens TEXT,
                valorTotal REAL,
                status TEXT,
                data_hora TEXT,
                cliente_id INTEGER,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cardapio (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                categoria TEXT,
                tamanho TEXT,
                preco REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hist_pedidos(
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        ''')


        self.conn.commit()


    def fechar_conexao(self):
        self.conn.close()


    def adicionarItemCardapio(self, nome, categoria, tamanho, preco):
        self.cursor.execute('''
            INSERT INTO cardapio (nome, categoria, tamanho, preco)
            VALUES (?, ?, ?, ?)
        ''', (nome, categoria, tamanho, preco))
        self.conn.commit()
        return f"Item '{nome}' adicionado ao cardápio."


    def consultarCardapio(self):
        self.cursor.execute('SELECT * FROM cardapio')
        items = self.cursor.fetchall()
        return [{"id": item[0], "nome": item[1], "categoria": item[2], "tamanho": item[3], "preco": item[4]} for item in items]


    def removerItemCardapio(self, item_id):
        self.cursor.execute('DELETE FROM cardapio WHERE id = ?', (item_id,))
        self.conn.commit()
        return f"Item {item_id} removido do cardápio."


    def obterItemCardapio(self, item_id):
        self.cursor.execute('SELECT * FROM cardapio WHERE id = ?', (item_id,))
        item = self.cursor.fetchone()
        if item:
            return {"id": item[0], "nome": item[1], "categoria": item[2], "tamanho": item[3], "preco": item[4]}
        return "Item não encontrado no cardápio."


    def criarPedido(self, itens, valor_total, cliente_id):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO pedidos (itens, valorTotal, status, data_hora, cliente_id)
            VALUES (?, ?, ?, ?,?)
        ''', (', '.join(itens), valor_total, "preparando", data_hora, cliente_id))
        self.conn.commit()
        return "Pedido criado com sucesso."


    def consultarPedido(self, pedido_id):
        self.cursor.execute('SELECT * FROM pedidos WHERE id = ?', (pedido_id,))
        pedido = self.cursor.fetchone()
        if pedido:
            return {"id": pedido[0], "itens": pedido[1], "valorTotal": pedido[2], "status": pedido[3], "data_hora": pedido[4]}
        return "Pedido não encontrado."


    def consultarTodosPedidos(self):
        self.cursor.execute('SELECT * FROM pedidos')
        pedidos = self.cursor.fetchall()
        return [{"id": pedido[0], "itens": pedido[1], "valorTotal": pedido[2], "status": pedido[3], "data_hora": pedido[4], "cliente_id": pedido[5]} for pedido in pedidos]


    def atualizarStatus(self, pedido_id, novo_status):
        self.cursor.execute('UPDATE pedidos SET status = ? WHERE id = ?', (novo_status, pedido_id))
        self.conn.commit()
        return f"Status do pedido {pedido_id} atualizado para '{novo_status}'."


    def removerPedido(self, pedido_id):
        self.cursor.execute('DELETE FROM pedidos WHERE id = ?', (pedido_id,))
        self.conn.commit()
        return f"Pedido {pedido_id} removido."
    
    def adicionarCliente(self, nome, cpf):
        self.cursor.execute("INSERt INTO clientes ( nome, cpf) values (?,?)", (nome, cpf))
        client_id = self.cursor.lastrowid

        self.cursor.execute("INSERT INTO hist_pedidos (cliente_id) VALUES (?)", (client_id,))

        self.conn.commit()

        return "Cliente cadastrado"
    
    def selecionarClienteNome(self, nome_cliente):
        self.cursor.execute('SELECT * FROM clientes WHERE nome = ?', (nome_cliente,))
        cliente = self.cursor.fetchone()
        return {"id": cliente[0], "nome": cliente[1], "cpf" : cliente[2]}
    
    def selecionarClienteId(self, id_cliente):
        self.cursor.execute('SELECT * FROM clientes WHERE id = ?', (id_cliente,))
        cliente = self.cursor.fetchone()
        return {"id": cliente[0], "nome": cliente[1], "cpf" : cliente[2]}
    
    
    def consultarTodosClientes(self,):
        self.cursor.execute('SELECT * FROM clientes')
        clientes = self.cursor.fetchall()
        return [{"id": cliente[0], "nome": cliente[1], "cpf": cliente[2]} for cliente in clientes]