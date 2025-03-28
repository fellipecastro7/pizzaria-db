from models.db import RestauranteDB

def menu():
    banco = RestauranteDB()
    
    while True:
        print("\n1. Criar Pedido\n2. Atualizar Status\n3. Consultar Pedido\n4. Remover Pedido\n5. Ver Todos os Pedidos\n6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            itens = input("Digite os itens do pedido separados por vírgula: ").split(", ")
            valorTotal = float(input("Digite o valor total: "))
            pedidoID = banco.criarPedido(itens, valorTotal)
            print(f"Pedido criado com ID {pedidoID}")

        elif escolha == "2":
            pedidoID = int(input("Digite o ID do pedido: "))
            while True:
                novoStatus = input("Digite o novo status (preparando/pronto/entregue): ").lower()
                mensagem = banco.atualizarStatus(pedidoID, novoStatus)
                if "Status inválido" in mensagem or "Pedido não encontrado" in mensagem:
                    print(mensagem)  
                else:
                    print(mensagem)  
                    break

        elif escolha == "3":
            pedidoID = int(input("Digite o ID do pedido: "))
            print(banco.consultarPedido(pedidoID))

        elif escolha == "4":
            pedidoID = int(input("Digite o ID do pedido: "))
            banco.removerPedido(pedidoID)
            print("Pedido removido.")

        elif escolha == "5":
            # Exibe todos os pedidos armazenados no banco em memória
            print("Todos os Pedidos:")
            pedidos = banco.consultarTodosPedidos()
            for pedido in pedidos:
                print(pedido)

        elif escolha == "6":
            banco.fechar_conexao()  # Fecha a conexão com o banco de dados
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
