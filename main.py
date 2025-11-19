import json

ARQ = "transacoes.json"

def lerx():
    try:
        a = open(ARQ, "r", encoding="utf-8")
        d = json.load(a)
        a.close()
        return d
    except:
        return []

def salvarx(d):
    a = open(ARQ, "w", encoding="utf-8")
    json.dump(d, a, indent=4, ensure_ascii=False)
    a.close()

def adicionar():
    print("\n--- Adicionar Transação ---")
    datax = input("Data (xxxx-xx-xx) (ano, mes e dia): ")
    tipox = input("Tipo (entrada/saida): ")
    catex = input("Categoria: ")
    descx = input("Descrição: ")
    valorx = float(input("Valor: "))

    d = lerx()
    d.append({"data": datax,"tipo": tipox,"categoria": catex,"descricao": descx,"valor": valorx })
    salvarx(d)
    print("Transação salva.\n")

def remover():
    listar()
    d = lerx()
    num = int(input("Número da transação para remover: "))
    if 0 <= num < len(d):
        d.pop(num)
        salvarx(d)
        print("Removida.\n")
    else:
        print("Número inválido.\n")

def listar():
    print("\n--- Lista de Transações ---")
    d = lerx()
    if len(d) == 0:
        print("Nenhuma transação ainda.\n")
        return
    for i, t in enumerate(d):
        print(i, t)
    print()

def listar_cat():
    catex = input("\nCategoria: ")
    d = lerx()
    print("\n--- Transações da Categoria ---")
    for t in d:
        if t["categoria"] == catex:
            print(t)
    print()

def listar_periodo():
    inix = input("Data inicial: ")
    finax = input("Data final: ")
    d = lerx()
    print("\n--- Transações no período ---")
    for t in d:
        if inix <= t["data"] <= finax:
            print(t)
    print()

def saldo_periodo():
    inix = input("Data inicial: ")
    finax = input("Data final: ")
    d = lerx()
    entrx = 0
    saidx = 0
    for t in d:
        if inix <= t["data"] <= finax:
            if t["tipo"] == "entrada":
                entrx += t["valor"]
            else:
                saidx += t["valor"]
    print("\nSaldo do período:", entrx - saidx, "\n")

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
        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar()
        elif opcao == "2":
            remover()
        elif opcao == "3":
            listar_cat()
        elif opcao == "4":
            listar_periodo()
        elif opcao == "5":
            saldo_periodo()
        elif opcao == "6":
            listar()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.\n")

menu()
