import funçõesat as fn
from datetime import datetime
import matplotlib.pyplot as plt

try:
    plt.switch_backend('Agg')
except ImportError:
    pass

def _filtrar_transacoes_por_data(transacoes, inicio, fim):
    """Função interna para filtrar transações entre duas datas (inclusivas)."""
    if not fn.validar_data(inicio) or not fn.validar_data(fim):
        return None, "Erro: Data de início ou fim inválida! Use o formato dd/mm/aaaa."

    try:
        di = datetime.strptime(inicio, "%d/%m/%Y")
        df = datetime.strptime(fim, "%d/%m/%Y")
    except ValueError:
        return None, "Erro: Formato de data incorreto."

    if di > df:
        return None, "Erro: Data de início não pode ser posterior à data final."

    filtradas = []
    for t in transacoes:
        try:
            data_t = datetime.strptime(t["data"], "%d/%m/%Y")
            if di <= data_t <= df:
                filtradas.append(t)
        except:
            continue

    return filtradas, None

def total_receita_despesa_por_periodo(inicio, fim):
    """
    Calcula a receita total e a despesa total em um período.
    Retorna uma tupla (receita_total, despesa_total) ou string de erro.
    """
    transacoes = fn.carregar_dados()
    filtradas, erro = _filtrar_transacoes_por_data(transacoes, inicio, fim)

    if erro:
        return erro

    receita = sum(t['valor'] for t in filtradas if t['tipo'] == 'entrada')
    despesa = sum(t['valor'] for t in filtradas if t['tipo'] == 'saida')

    return (receita, despesa)

def media_gastos_por_categoria():
    """
    Calcula a média de gastos (saídas) por categoria.
    Retorna um dicionário {categoria: media} ou string de erro.
    """
    transacoes = fn.carregar_dados()
    despesas_por_categoria = {}

    if not transacoes:
        return "Nenhuma transação encontrada para calcular a média."

    for t in transacoes:
        if t['tipo'] == 'saida':
            cat = t['categoria'].lower()
            valor = t['valor']
            if cat not in despesas_por_categoria:
                despesas_por_categoria[cat] = {'total': 0, 'count': 0}

            despesas_por_categoria[cat]['total'] += valor
            despesas_por_categoria[cat]['count'] += 1

    if not despesas_por_categoria:
        return "Nenhuma despesa (saída) encontrada."

    medias = {
        cat: data['total'] / data['count']
        for cat, data in despesas_por_categoria.items()
    }

    return medias

def saldo_mensal_acumulado():
    """
    Calcula o saldo acumulado ao longo dos meses.
    Retorna um dicionário ordenado {mes_ano: saldo_acumulado}.
    """
    transacoes = fn.carregar_dados()
    if not transacoes:
        return "Nenhuma transação encontrada."

    transacoes_processadas = []
    for t in transacoes:
        try:
            data_obj = datetime.strptime(t["data"], "%d/%m/%Y")
            transacoes_processadas.append({
                "data": data_obj,
                "mes_ano": data_obj.strftime("%Y-%m"),  # Chave de ordenação
                "valor": t["valor"] if t["tipo"] == "entrada" else -t["valor"]
            })
        except:
            continue

    transacoes_processadas.sort(key=lambda x: x["data"])

    saldo_mensal = {}
    for t in transacoes_processadas:
        mes_ano = t["mes_ano"]
        if mes_ano not in saldo_mensal:
            saldo_mensal[mes_ano] = 0
        saldo_mensal[mes_ano] += t["valor"]

    saldo_acumulado = 0
    saldo_acumulado_mensal = {}

    for mes_ano, saldo in saldo_mensal.items():
        saldo_acumulado += saldo
        saldo_acumulado_mensal[mes_ano] = saldo_acumulado

    return saldo_acumulado_mensal

def gerar_grafico_pizza_gastos():
    """
    Gera um gráfico de pizza da proporção de gastos por categoria e salva como PNG.
    Retorna o nome do arquivo ou string de erro.
    """
    transacoes = fn.carregar_dados()
    despesas_por_categoria = {}

    for t in transacoes:
        if t['tipo'] == 'saida':
            cat = t['categoria'].capitalize()
            despesas_por_categoria[cat] = despesas_por_categoria.get(cat, 0) + t['valor']

    if not despesas_por_categoria:
        return "Nenhuma despesa (saída) encontrada para gerar o gráfico."

    categorias = list(despesas_por_categoria.keys())
    valores = list(despesas_por_categoria.values())

    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
    plt.title('Proporção de Gastos por Categoria')
    plt.axis('equal')

    nome_arquivo = 'grafico_pizza_gastos.png'
    try:
        plt.savefig(nome_arquivo)
        plt.close()
        return nome_arquivo
    except Exception as e:
        return f"Erro ao salvar o gráfico: {e}"

def gerar_grafico_linha_saldo():
    """
    Gera um gráfico de linha do saldo acumulado ao longo do tempo e salva como PNG.
    Retorna o nome do arquivo ou string de erro.
    """
    saldo_mensal = saldo_mensal_acumulado()

    if isinstance(saldo_mensal, str):  # Se for uma string de erro
        return saldo_mensal

    if not saldo_mensal:
        return "Dados insuficientes para gerar o gráfico de saldo acumulado."

    meses_str = [datetime.strptime(m, "%Y-%m").strftime("%m/%Y") for m in saldo_mensal.keys()]
    saldos = list(saldo_mensal.values())

    plt.figure(figsize=(10, 6))
    plt.plot(meses_str, saldos, marker='o', linestyle='-', color='b')
    plt.title('Saldo Acumulado ao Longo do Tempo')
    plt.xlabel('Mês/Ano')
    plt.ylabel('Saldo Acumulado (R$)')
    plt.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    nome_arquivo = 'grafico_linha_saldo.png'
    try:
        plt.savefig(nome_arquivo)
        plt.close()
        return nome_arquivo
    except Exception as e:
        return f"Erro ao salvar o gráfico: {e}"