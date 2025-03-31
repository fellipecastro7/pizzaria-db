from models.db import PizzariaDB
from utils.validacoes import validar_preco, validar_nome, validar_categoria
from utils.helpers import formatar_data_hora

def menu():
    banco = PizzariaDB()

    while True:
        print("\n1. Adicionar Item ao Cardápio")
        print("2. Remover Item do Cardápio")
        print("3. Criar Pedido")
        print("4. Atualizar Status do Pedido")
        print("5. Consultar Pedido")
        print("6. Remover Pedido")
        print("7. Ver Todos os Pedidos")
        print("8. Ver Cardápio")
        print("9. Adicionar cliente")
        print("10. Consultar pedidos de um cliente")
        print("11. Sair")
        
        escolha = input("Escolha uma opção: ").strip()
        
        cardapioVazio = len(banco.consultarCardapio()) == 0
        pedidosVazio = len(banco.consultarTodosPedidos()) == 0
        clienteVazio = len(banco.consultarTodosClientes()) == 0

        if escolha == "1":
            nome = input("Digite o nome do item: ").strip()
            validacao_nome = validar_nome(nome)
            if validacao_nome:
                print(validacao_nome)
                continue

            categoria = input("Digite a categoria (pizza ou bebida): ").strip()
            validacao_categoria = validar_categoria(categoria)
            if validacao_categoria:
                print(validacao_categoria)
                continue

            tamanho = None
            if categoria == "pizza":
                tamanho = input("Digite o tamanho (Pequena, Média, Grande ou Família): ").strip()
                if not tamanho:
                    print("O tamanho da pizza deve ser especificado.")
                    continue

            preco = input("Digite o preço do item: ").strip()
            validacao_preco = validar_preco(preco)
            if validacao_preco:
                print(validacao_preco)
                continue
            preco = float(preco)

            print(banco.adicionarItemCardapio(nome, categoria, tamanho, preco))

        elif escolha == "2":
            if cardapioVazio:
                print("Não há itens no cardápio para remover.")
            else:
                cardapio = banco.consultarCardapio()
                print("\nCardápio Atual:")
                for item in cardapio:
                    print(f"{item['id']}: {item['nome']} ({item['tamanho']}) - R$ {item['preco']}")

                item_id = input("Digite o ID do item que deseja remover: ").strip()
                if not item_id.isdigit():
                    print("ID inválido!")
                    continue
                print(banco.removerItemCardapio(int(item_id)))

        elif escolha == "3":
            if cardapioVazio or clienteVazio:
                print("Não há itens no cardápio para criar um pedido ou sem clientes cadastrados.")
            else:
                clientes = banco.consultarTodosClientes()
                #print("Digite o id de um cliente para seleciona-lo")
                for cliente in clientes:
                    print(f"Id: {cliente['id']} Nome: {cliente['nome']} CPF {cliente['cpf']}")

                cliente_id = int(input("Digite o id de um cliente para seleciona-lo como dono da compra "))

                cardapio = banco.consultarCardapio()
                print("\nCardápio:")
                for item in cardapio:
                    print(f"{item['id']}: {item['nome']} ({item['tamanho']}) - R$ {item['preco']}")

                pedido = []
                total = 0
                while True:
                    item_id = input("Digite o ID do item (ou 'fim' para finalizar o pedido): ").strip()
                    if item_id.lower() == 'fim':
                        break
                    if not item_id.isdigit():
                        print("Entrada inválida! Digite um número válido.")
                        continue
                    item_id = int(item_id)
                    item = banco.obterItemCardapio(item_id)
                    if item != "Item não encontrado no cardápio.":
                        pedido.append(item["nome"])
                        total += item["preco"]
                        print(f"Item '{item['nome']}' adicionado ao pedido.")
                    else:
                        print("Item não encontrado no cardápio.")

                print(banco.criarPedido(pedido, total, cliente_id))

        elif escolha == "4":
            if pedidosVazio:
                print("Não há pedidos para atualizar.")
            else:
                pedidos = banco.consultarTodosPedidos()
                print("\nPedidos Atuais:")
                for pedido in pedidos:
                    print(f"ID: {pedido['id']} - Status: {pedido['status']} - Total: R$ {pedido['valorTotal']} - Data: {formatar_data_hora()}")

                pedidoID = input("Digite o ID do pedido: ").strip()
                if not pedidoID.isdigit():
                    print("ID inválido!")
                    continue
                pedidoID = int(pedidoID)
                novoStatus = input("Digite o novo status (preparando/pronto/entregue): ").lower()
                if novoStatus not in ["preparando", "pronto", "entregue"]:
                    print("Status inválido. Escolha entre: 'preparando', 'pronto' ou 'entregue'.")
                    continue
                print(banco.atualizarStatus(pedidoID, novoStatus))

        elif escolha == "5":
            if pedidosVazio:
                print("Não há pedidos para consultar.")
            else:
                pedidos = banco.consultarTodosPedidos()
                print("\nPedidos Atuais:")
                for pedido in pedidos:
                    print(f"ID: {pedido['id']} - Status: {pedido['status']} - Total: R$ {pedido['valorTotal']} - Data: {formatar_data_hora()}")

                pedidoID = input("Digite o ID do pedido: ").strip()
                if not pedidoID.isdigit():
                    print("ID inválido!")
                    continue
                pedidoID = int(pedidoID)
                print(banco.consultarPedido(pedidoID))

        elif escolha == "6":
            if pedidosVazio:
                print("Não há pedidos para remover.")
            else:
                pedidos = banco.consultarTodosPedidos()
                print("\nPedidos Atuais:")
                for pedido in pedidos:
                    print(f"ID: {pedido['id']} - Status: {pedido['status']} - Total: R$ {pedido['valorTotal']} - Data: {formatar_data_hora()}")

                pedidoID = input("Digite o ID do pedido: ").strip()
                if not pedidoID.isdigit():
                    print("ID inválido!")
                    continue
                pedidoID = int(pedidoID)
                print(banco.removerPedido(pedidoID))

        elif escolha == "7":
            if pedidosVazio:
                print("Não há pedidos para exibir.")
            else:
                pedidos = banco.consultarTodosPedidos()
                print("\nPedidos Atuais:")
                for pedido in pedidos:
                    client = banco.selecionarClienteId(pedido['cliente_id'])
                    print(f"ID: {pedido['id']} - Status: {pedido['status']} - Total: R$ {pedido['valorTotal']} - Data: {formatar_data_hora()} - Cliente: {client['nome']}")

        elif escolha == "8":
            if cardapioVazio:
                print("O cardápio está vazio.")
            else:
                cardapio = banco.consultarCardapio()
                print("\nCardápio Atual:")
                for item in cardapio:
                    print(f"{item['id']}: {item['nome']} ({item['tamanho']}) - R$ {item['preco']}")

        elif escolha == "9":
            nome = str(input("Qual o nome do cliente?"))
            cpf = str(input("Qual o CPF do cliente? "))

            print(banco.adicionarCliente(nome, cpf))

        elif escolha == "10":
            clientes = banco.consultarTodosClientes()
            #print("Digite o id de um cliente para seleciona-lo")
            for cliente in clientes:
                print(f"Id: {cliente['id']} Nome: {cliente['nome']} CPF {cliente['cpf']}")
            id_cliente = input("Qual id do cliente: ")
            pedidos_cliente = banco.consultarPedidosCliente(id_cliente)
            print(f"Pedidos realizados pelo cliente: ")
            for pedido in pedidos_cliente:
                client = banco.selecionarClienteId(pedido['cliente_id'])
                print(f"ID: {pedido['id']} - Status: {pedido['status']} - Total: R$ {pedido['valorTotal']} - Data: {formatar_data_hora()} - Cliente: {client['nome']}")
        elif escolha == "11":
            banco.fechar_conexao()
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


menu()