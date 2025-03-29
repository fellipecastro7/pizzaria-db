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
        print("9. Sair")
        
        escolha = input("Escolha uma opção: ").strip()
        
        cardapioVazio = len(banco.consultarCardapio()) == 0
        pedidosVazio = len(banco.consultarTodosPedidos()) == 0

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
            if cardapioVazio:
                print("Não há itens no cardápio para criar um pedido.")
            else:
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

                print(banco.criarPedido(pedido, total))

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
                    print(f"ID: {pedido['id']} - Status: {pedido['status']} - Total: R$ {pedido['valorTotal']} - Data: {formatar_data_hora()}")

        elif escolha == "8":
            if cardapioVazio:
                print("O cardápio está vazio.")
            else:
                cardapio = banco.consultarCardapio()
                print("\nCardápio Atual:")
                for item in cardapio:
                    print(f"{item['id']}: {item['nome']} ({item['tamanho']}) - R$ {item['preco']}")

        elif escolha == "9":
            banco.fechar_conexao()
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


menu()