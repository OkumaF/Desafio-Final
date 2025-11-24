import json
from datetime import datetime

ARQUIVO = "transacoes.json"

def carregar_dados():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_dados(transacoes):
    with open(ARQUIVO, "w") as f:
        json.dump(transacoes, f, indent=4)

def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except:
        return False

def adicionar_transacao(data, tipo, categoria, descricao, valor_str):
    if not validar_data(data):
        return "Erro: Data inválida! Use o formato dd/mm/aaaa."

    tipo = tipo.lower()
    if tipo not in ["entrada", "saida"]:
        return "Erro: Tipo inválido! Use 'entrada' ou 'saida'."

    try:
        valor = float(valor_str)
    except ValueError:
        return "Erro: Valor inválido. Digite um número."

    transacoes = carregar_dados()

    transacoes.append({"data": data,"tipo": tipo,"categoria": categoria,"descricao": descricao,"valor": valor})

    salvar_dados(transacoes)
    return "Transação salva e adicionada com sucesso!"

def remover_transacao(idx):
    transacoes = carregar_dados()

    try:
        idx = int(idx)
    except ValueError:
        return "Erro: Índice inválido. Digite um número."

    if 0 <= idx < len(transacoes):
        transacoes.pop(idx)
        salvar_dados(transacoes)
        return "Transação removida!"
    else:
        return "Erro: Índice inválido."

def listar_todas():
    transacoes = carregar_dados()
    if not transacoes:
        return "Nenhuma transação encontrada."

    resultado = "Segue todas as transações:\n\n"
    for i, t in enumerate(transacoes):
        resultado += f"{i} - {t['data']} | {t['tipo']} | {t['categoria']} | R$ {t['valor']:.2f} | {t['descricao']}\n"
    return resultado

def listar_por_categoria(cat):
    transacoes = carregar_dados()
    resultado = f"Transações da Categoria: {cat}\n\n"
    encontradas = [t for t in transacoes if t["categoria"].lower() == cat.lower()]

    if not encontradas:
        return f"Nenhuma transação encontrada para a categoria '{cat}'."

    for t in encontradas:
        resultado += f"Data: {t['data']} | Tipo: {t['tipo']} | Valor: R$ {t['valor']:.2f} | Descrição: {t['descricao']}\n"

    return resultado

def listar_por_periodo(inicio, fim):
    transacoes = carregar_dados()

    if not validar_data(inicio) or not validar_data(fim):
        return "Erro: Data de início ou fim inválida! Use o formato dd/mm/aaaa."

    try:
        di = datetime.strptime(inicio, "%d/%m/%Y")
        df = datetime.strptime(fim, "%d/%m/%Y")
    except ValueError:
        return "Erro: Formato de data incorreto."

    if di > df:
        return "Erro: Data de início não pode ser posterior à data final."

    resultado = f"Transações entre {inicio} e {fim}\n\n"
    encontradas = []

    for t in transacoes:
        try:
            data_t = datetime.strptime(t["data"], "%d/%m/%Y")
            if di <= data_t <= df:
                encontradas.append(t)
        except:
            pass

    if not encontradas:
        return "Nenhuma transação encontrada neste período."

    for t in encontradas:
        resultado += f"Data: {t['data']} | Tipo: {t['tipo']} | Categoria: {t['categoria']} | Valor: R$ {t['valor']:.2f}\n"

    return resultado


def saldo_por_periodo(inicio, fim):
    transacoes = carregar_dados()

    if not validar_data(inicio) or not validar_data(fim):
        return "Erro: Data de início ou fim inválida! Use o formato dd/mm/aaaa."

    try:
        di = datetime.strptime(inicio, "%d/%m/%Y")
        df = datetime.strptime(fim, "%d/%m/%Y")
    except ValueError:
        return "Erro: Formato de data incorreto."

    if di > df:
        return "Erro: Data de início não pode ser posterior à data final."

    saldo = 0
    for t in transacoes:
        try:
            data_t = datetime.strptime(t["data"], "%d/%m/%Y")
            if di <= data_t <= df:
                if t["tipo"] == "entrada":
                    saldo += t["valor"]
                else:
                    saldo -= t["valor"]
        except:
            pass

    return f"Saldo no período ({inicio} a {fim}): R$ {saldo:.2f}"