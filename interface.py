import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext
import funçõesat as fn
import funçõesest as fne
import os
import webbrowser

USUARIOS = {}


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controle Financeiro")
        self.geometry("450x450")
        self.iconify()
        self.after(50, self.deiconify)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (TelaLogin, TelaCadastro, TelaSistema):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TelaLogin")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def verificar_login(self, usuario, senha):
        if not USUARIOS:
            messagebox.showwarning("Atenção","Nenhum usuário cadastrado. Por favor, use o botão 'Criar Conta' para cadastrar o primeiro usuário.")
            return False

        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.show_frame("TelaSistema")
            return True
        else:
            messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")
            return False

    def adicionar_usuario(self, usuario, senha):
        if not usuario or not senha:
            messagebox.showerror("Erro de Cadastro", "Nome de usuário e senha não podem ser vazios.")
            return False

        if usuario in USUARIOS:
            messagebox.showerror("Erro de Cadastro", "Nome de usuário já existe.")
            return False

        USUARIOS[usuario] = senha
        messagebox.showinfo("Cadastro", f"Usuário '{usuario}' cadastrado com sucesso!")
        self.show_frame("TelaLogin")
        return True


class TelaLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_titulo = tk.Label(center_frame, text="Login", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=20)

        label_usuario = tk.Label(center_frame, text="Nome:")
        label_usuario.pack(pady=2)
        self.entrada_usuario = tk.Entry(center_frame, width=30, justify='center')
        self.entrada_usuario.pack(pady=2)

        label_senha = tk.Label(center_frame, text="Senha:")
        label_senha.pack(pady=2)
        self.entrada_senha = tk.Entry(center_frame, width=30, show="*", justify='center')
        self.entrada_senha.pack(pady=2)

        botao_entrar = tk.Button(center_frame, text="Entrar", command=self.acao_login, width=20)
        botao_entrar.pack(pady=10)

        botao_cadastrar = tk.Button(center_frame, text="Criar Conta (Cadastrar)",
                                    command=lambda: self.controller.show_frame("TelaCadastro"), width=20)
        botao_cadastrar.pack(pady=5)

    def acao_login(self):
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()
        self.controller.verificar_login(usuario, senha)


class TelaCadastro(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_titulo = tk.Label(center_frame, text="Cadastro de Usuário", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=20)

        label_usuario = tk.Label(center_frame, text="Nome de Usuário:")
        label_usuario.pack(pady=2)
        self.entrada_usuario = tk.Entry(center_frame, width=30, justify='center')
        self.entrada_usuario.pack(pady=2)

        label_senha = tk.Label(center_frame, text="Senha:")
        label_senha.pack(pady=2)
        self.entrada_senha = tk.Entry(center_frame, width=30, show="*", justify='center')
        self.entrada_senha.pack(pady=2)

        botao_registrar = tk.Button(center_frame, text="Registrar", command=self.acao_cadastro, width=25)
        botao_registrar.pack(pady=10)

    def acao_cadastro(self):
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()
        if self.controller.adicionar_usuario(usuario, senha):
            self.entrada_usuario.delete(0, tk.END)
            self.entrada_senha.delete(0, tk.END)


class AdicionarTransacaoPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Adicionar Nova Transação")
        self.geometry("300x350")
        self.transient(parent)
        self.grab_set()

        self.data_var = tk.StringVar()
        self.tipo_var = tk.StringVar(value="entrada")
        self.categoria_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        self.valor_var = tk.StringVar()

        tk.Label(self, text="Data (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.data_var, width=20).pack(pady=2)

        tk.Label(self, text="Tipo:").pack(pady=5)
        tk.Radiobutton(self, text="Entrada", variable=self.tipo_var, value="entrada").pack()
        tk.Radiobutton(self, text="Saída", variable=self.tipo_var, value="saida").pack()

        tk.Label(self, text="Categoria:").pack(pady=5)
        tk.Entry(self, textvariable=self.categoria_var, width=20).pack(pady=2)

        tk.Label(self, text="Descrição:").pack(pady=5)
        tk.Entry(self, textvariable=self.descricao_var, width=20).pack(pady=2)

        tk.Label(self, text="Valor:").pack(pady=5)
        tk.Entry(self, textvariable=self.valor_var, width=20).pack(pady=2)

        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=15)

    def salvar(self):
        resultado = fn.adicionar_transacao(self.data_var.get(), self.tipo_var.get(), self.categoria_var.get(),
                                           self.descricao_var.get(), self.valor_var.get())

        if resultado.startswith("Erro"):
            messagebox.showerror("Erro ao Salvar", resultado)
        else:
            messagebox.showinfo("Sucesso", resultado)
            self.destroy()


class ListarTodasPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Todas as Transações")
        self.geometry("600x400")

        resultado = fn.listar_todas()

        text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=20)
        text_area.insert(tk.INSERT, resultado)
        text_area.config(state=tk.DISABLED)
        text_area.pack(pady=10, padx=10)


class RemoverTransacaoPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("🗑Remover Transação")
        self.geometry("450x300")
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Transações Atuais:").pack(pady=5)

        lista_transacoes = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=5)
        lista_transacoes.insert(tk.INSERT, fn.listar_todas())
        lista_transacoes.config(state=tk.DISABLED)
        lista_transacoes.pack(pady=5, padx=10)

        self.idx_var = tk.StringVar()
        tk.Label(self, text="Digite o NÚMERO (Índice) da transação para remover:").pack(pady=10)
        tk.Entry(self, textvariable=self.idx_var, width=10).pack(pady=2)

        tk.Button(self, text="Remover", command=self.remover).pack(pady=15)

    def remover(self):
        resultado = fn.remover_transacao(self.idx_var.get())

        if resultado.startswith("Erro"):
            messagebox.showerror("Erro ao Remover", resultado)
        else:
            messagebox.showinfo("Sucesso", resultado)
            self.destroy()


class ListarPorCategoriaPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Listar por Categoria")
        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()

        self.cat_var = tk.StringVar()

        tk.Label(self, text="Digite a Categoria Desejada:").pack(pady=10)
        tk.Entry(self, textvariable=self.cat_var, width=20).pack(pady=5)

        tk.Button(self, text="Buscar", command=self.buscar).pack(pady=10)

        self.resultado_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=45, height=10)
        self.resultado_area.pack(pady=5, padx=10)

    def buscar(self):
        categoria = self.cat_var.get()
        resultado = fn.listar_por_categoria(categoria)

        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)
        self.resultado_area.insert(tk.INSERT, resultado)
        self.resultado_area.config(state=tk.DISABLED)


class ListarPorPeriodoPopup(Toplevel):
    def __init__(self, parent, modo="listar"):
        Toplevel.__init__(self, parent)
        self.modo = modo
        if modo == "listar":
            self.title("Listar por Período")
        else:
            self.title("Saldo por Período")

        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()

        self.inicio_var = tk.StringVar()
        self.fim_var = tk.StringVar()

        tk.Label(self, text="Data de Início (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.inicio_var, width=20).pack(pady=2)

        tk.Label(self, text="Data Final (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.fim_var, width=20).pack(pady=2)

        tk.Button(self, text="Processar", command=self.processar).pack(pady=10)

        self.resultado_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=45, height=10)
        self.resultado_area.pack(pady=5, padx=10)

    def processar(self):
        inicio = self.inicio_var.get()
        fim = self.fim_var.get()

        if self.modo == "listar":
            resultado = fn.listar_por_periodo(inicio, fim)
        else:
            resultado = fn.saldo_por_periodo(inicio, fim)

        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)
        self.resultado_area.insert(tk.INSERT, resultado)
        self.resultado_area.config(state=tk.DISABLED)


class ReceitaDespesaPeriodoPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Receita e Despesa por Período")
        self.geometry("400x280")
        self.transient(parent)
        self.grab_set()

        self.inicio_var = tk.StringVar()
        self.fim_var = tk.StringVar()

        tk.Label(self, text="Data de Início (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.inicio_var, width=20).pack(pady=2)

        tk.Label(self, text="Data Final (dd/mm/aaaa):").pack(pady=5)
        tk.Entry(self, textvariable=self.fim_var, width=20).pack(pady=2)

        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=10)

        self.resultado_label = tk.Label(self, text="", justify=tk.LEFT)
        self.resultado_label.pack(pady=10, padx=10)

    def calcular(self):
        inicio = self.inicio_var.get()
        fim = self.fim_var.get()

        resultado = fne.total_receita_despesa_por_periodo(inicio, fim)

        if isinstance(resultado, str):
            messagebox.showerror("Erro de Cálculo", resultado)
            self.resultado_label.config(text="")
            return

        receita, despesa = resultado

        texto_resultado = (
            f"Receita Total ({inicio} a {fim}): R$ {receita:.2f}\n"
            f"Despesa Total ({inicio} a {fim}): R$ {despesa:.2f}\n"
            f"Resultado Líquido: R$ {(receita - despesa):.2f}"
        )
        self.resultado_label.config(text=texto_resultado)


class MediaGastosPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Média de Gastos por Categoria")
        self.geometry("450x400")
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Média de Gastos (Saídas) por Categoria:", font=("Arial", 12, "bold")).pack(pady=10)

        self.resultado_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=15)
        self.resultado_area.pack(pady=5, padx=10)
        self.mostrar_medias()

    def mostrar_medias(self):
        medias = fne.media_gastos_por_categoria()

        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)

        if isinstance(medias, str):
            self.resultado_area.insert(tk.INSERT, medias)
        else:
            texto = "Categoria | Média Mensal (R$)\n"
            texto += "---------------------------------------\n"
            for cat, media in sorted(medias.items(), key=lambda item: item[1], reverse=True):
                texto += f"{cat.capitalize().ljust(15)} | R$ {media:.2f}\n"
            self.resultado_area.insert(tk.INSERT, texto)

        self.resultado_area.config(state=tk.DISABLED)


class SaldoAcumuladoPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Saldo Mensal Acumulado")
        self.geometry("450x400")
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Saldo Acumulado (Mês a Mês):", font=("Arial", 12, "bold")).pack(pady=10)

        self.resultado_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=15)
        self.resultado_area.pack(pady=5, padx=10)
        self.mostrar_saldo()

    def mostrar_saldo(self):
        saldos = fne.saldo_mensal_acumulado()

        self.resultado_area.config(state=tk.NORMAL)
        self.resultado_area.delete(1.0, tk.END)

        if isinstance(saldos, str):
            self.resultado_area.insert(tk.INSERT, saldos)
        else:
            texto = "Mês/Ano | Saldo Acumulado (R$)\n"
            texto += "---------------------------------------\n"
            for mes_ano, saldo in saldos.items():
                mes_display = f"{mes_ano[5:7]}/{mes_ano[0:4]}"
                texto += f"{mes_display.ljust(10)} | R$ {saldo:,.2f}\n"
            self.resultado_area.insert(tk.INSERT, texto.replace(",", "."))  # Ajusta formato de milhar para PT-BR

        self.resultado_area.config(state=tk.DISABLED)


class GeradorGraficosPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Gerar Gráficos")
        self.geometry("300x200")
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Selecione o Gráfico:", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(self, text="Gráfico de Pizza (Gastos)", command=self.gerar_pizza, width=30).pack(pady=5)
        tk.Button(self, text="Gráfico de Linha (Saldo Acumulado)", command=self.gerar_linha, width=30).pack(pady=5)

        tk.Label(self, text="Os gráficos serão salvos como PNG na pasta do script.").pack(pady=10)

    def abrir_arquivo(self, nome_arquivo):
        """Tenta abrir o arquivo PNG com o programa padrão do sistema."""
        if os.path.exists(nome_arquivo):
            try:
                # Usa webbrowser.open para tentar abrir o arquivo no sistema operacional
                webbrowser.open(f'file:///{os.path.abspath(nome_arquivo)}')
                messagebox.showinfo("Sucesso", f"Gráfico '{nome_arquivo}' salvo e aberto no visualizador padrão.")
            except Exception as e:
                messagebox.showinfo("Sucesso",
                                    f"Gráfico '{nome_arquivo}' salvo. Abra manualmente. Erro ao tentar abrir: {e}")
        else:
            messagebox.showerror("Erro", f"Arquivo de gráfico '{nome_arquivo}' não encontrado.")

    def gerar_pizza(self):
        nome_arquivo = fne.gerar_grafico_pizza_gastos()
        if isinstance(nome_arquivo, str) and nome_arquivo.startswith("Erro"):
            messagebox.showerror("Erro ao Gerar Gráfico", nome_arquivo)
        else:
            self.abrir_arquivo(nome_arquivo)

    def gerar_linha(self):
        nome_arquivo = fne.gerar_grafico_linha_saldo()
        if isinstance(nome_arquivo, str) and nome_arquivo.startswith("Erro"):
            messagebox.showerror("Erro ao Gerar Gráfico", nome_arquivo)
        else:
            self.abrir_arquivo(nome_arquivo)


class TelaSistema(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_titulo = tk.Label(center_frame, text="Sistema de Controle Financeiro", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=10)

        PAD_X = 50

        btn_adicionar = tk.Button(center_frame, text="1. Adicionar Transação",
                                  command=lambda: AdicionarTransacaoPopup(self.master))
        btn_adicionar.pack(pady=5, padx=PAD_X, fill='x')

        btn_remover = tk.Button(center_frame, text="2. Remover Transação",
                                command=lambda: RemoverTransacaoPopup(self.master))
        btn_remover.pack(pady=5, padx=PAD_X, fill='x')

        btn_listar_todas = tk.Button(center_frame, text="3. Listar Todas Transações",
                                     command=lambda: ListarTodasPopup(self.master))
        btn_listar_todas.pack(pady=5, padx=PAD_X, fill='x')

        btn_por_categoria = tk.Button(center_frame, text="4. Listar por Categoria",
                                      command=lambda: ListarPorCategoriaPopup(self.master))
        btn_por_categoria.pack(pady=5, padx=PAD_X, fill='x')

        btn_saldo = tk.Button(center_frame, text="5. Saldo Total por Período",
                              command=lambda: ListarPorPeriodoPopup(self.master, modo="saldo"))
        btn_saldo.pack(pady=5, padx=PAD_X, fill='x')

        btn_rec_desp = tk.Button(center_frame, text="6. Receita/Despesa no Período",
                                 command=lambda: ReceitaDespesaPeriodoPopup(self.master))
        btn_rec_desp.pack(pady=5, padx=PAD_X, fill='x')

        btn_media = tk.Button(center_frame, text="7. Média de Gastos por Categoria",
                              command=lambda: MediaGastosPopup(self.master))
        btn_media.pack(pady=5, padx=PAD_X, fill='x')

        btn_acumulado = tk.Button(center_frame, text="8. Saldo Mensal Acumulado (Tabela)",
                                  command=lambda: SaldoAcumuladoPopup(self.master))
        btn_acumulado.pack(pady=5, padx=PAD_X, fill='x')

        btn_graficos = tk.Button(center_frame, text="9. Gerar Gráficos (Pizza/Linha)",
                                 command=lambda: GeradorGraficosPopup(self.master))
        btn_graficos.pack(pady=10, padx=PAD_X, fill='x')

        btn_sair = tk.Button(center_frame, text="Sair / Logout", command=lambda: controller.show_frame("TelaLogin"))
        btn_sair.pack(pady=15, padx=PAD_X, fill='x')

def inicializar():
    app = Aplicacao()
    app.mainloop()

inicializar()