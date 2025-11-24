from funções import ( adicionar_transacao,remover_transacao,listar_todas,listar_por_categoria,listar_por_periodo,saldo_por_periodo)

def menu():
    while True:
        print("------ MENU ------")
        print("1 - Adicionar transação")
        print("2 - Remover transação")
        print("3 - Listar por categoria")
        print("4 - Listar por período")
        print("5 - Saldo por período")
        print("6 - Listar todas")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            adicionar_transacao()
        elif op == "2":
            remover_transacao()
        elif op == "3":
            listar_por_categoria()
        elif op == "4":
            listar_por_periodo()
        elif op == "5":
            saldo_por_periodo()
        elif op == "6":
            listar_todas()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.\n")

menu()

