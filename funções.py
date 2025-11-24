import json

ARQ = "transacoes.json"

def ler_transacoes():
    try:
        with open(ARQ, "r", encoding="utf-8") as a:
            return json.load(a)
    except:
        return []

def salvar_transacoes(lista):
    with open(ARQ, "w", encoding="utf-8") as a:
        json.dump(lista, a, indent=4, ensure_ascii=False)

def adicionar_transacao():
    print("\n--- Adicionar Transação ---")
    datax = input("Data (xxxx-xx-xx) Ex:(2007/12/25): ")
    tipox = input("Tipo (entrada/saida): ")
    catex = input("Categoria: ")
    descx = input("Descrição: ")
    valorx = float(input("Valor: "))

    lista = ler_transacoes()
    lista.append({
        "data": datax,
        "tipo": tipox,
        "categoria": catex,
        "descricao": descx,
        "valor": valorx
    })
    salvar_transacoes(lista)
    print("Transação salva.\n")

def remover_transacao():
    listar_todas()
    lista = ler_transacoes()
    num = int(input("Número da transação para remover: "))
    if 0 <= num < len(lista):
        lista.pop(num)
        salvar_transacoes(lista)
        print("Removida.\n")
    else:
        print("Número inválido.\n")

def listar_todas():
    print("\n--- Lista de Transações ---")
    lista = ler_transacoes()
    if len(lista) == 0:
        print("Nenhuma transação ainda.\n")
        return
    for i, t in enumerate(lista):
        print(i, t)
    print()

def listar_por_categoria():
    catex = input("\nCategoria: ")
    lista = ler_transacoes()
    print("\n--- Transações da Categoria ---")
    for t in lista:
        if t["categoria"] == catex:
            print(t)
    print()

def listar_por_periodo():
    ini = input("Data inicial (yyyy-mm-dd): ")
    fim = input("Data final (yyyy-mm-dd): ")
    lista = ler_transacoes()

    print("\n--- Transações no período ---")
    for t in lista:
        if ini <= t["data"] <= fim:
            print(t)
    print()

def saldo_por_periodo():
    ini = input("Data inicial (yyyy-mm-dd): ")
    fim = input("Data final (yyyy-mm-dd): ")

    lista = ler_transacoes()
    entradas = 0
    saidas = 0

    for t in lista:
        if ini <= t["data"] <= fim:
            if t["tipo"] == "entrada":
                entradas += t["valor"]
            else:
                saidas += t["valor"]

    print("\nSaldo do período:", entradas - saidas, "\n")
