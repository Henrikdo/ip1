import os
import csv 
import json
import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# Códigos das cores de texto em Python
R = '\033[31m' # vermelho
G = '\033[32m' # verde
B = '\033[34m' # azul
Y = '\033[33m' # amarelo
P = '\033[35m' # roxo
C = '\033[36m' # ciano
W = '\033[37m' # branco
i = '\033[3m'  # itálico
n = '\033[7m'  # negativo
r = '\033[0m'  # resetar
p = "\033[F"   # mover o cursor para o começo da linha anterior
u = "\033[A"   # mover o cursor para cima uma linha

interface = {}
meses_simulados = 0
# Parte 1, classe pessoa
class Pessoa:
    def __init__(self,nome, patrimonio, salario):
        self.nome = nome
        self.patrimonio = patrimonio
        self.conforto = 0.0
        self.salario = salario

class Empresa:
    def __init__(self, categoria, nome, produto, custo, qualidade):
        self.nome = nome
        self.categoria = categoria
        self.produto = produto
        self.custo = custo
        self.qualidade = qualidade
        self.margem = 0.05
        self.oferta = 0
        self.reposicao = 10
        self.vendas = 0



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ler_pessoas(caminho='pessoas.txt'):
    pessoas = []
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()[1:]  # Ignora a primeira linha
        for linha in linhas:
            partes = [parte.strip() for parte in linha.strip().split(',')]
            if len(partes) == 3:
                nome, patrimonio, salario = partes
                pessoas.append(Pessoa(nome, float(patrimonio), float(salario)))
    return pessoas


def ler_empresas(caminho='empresas.csv'):
    empresas = []
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)
        for linha in leitor:
            partes = [p.strip() for p in linha]
            if len(partes) == 5:
                categoria, nome, produto, custo, qualidade = partes
                empresas.append(Empresa(categoria, nome, produto, float(custo), int(qualidade)))
    return empresas




# Função para ler categorias e percentuais de um arquivo .json
def ler_categorias(caminho='categorias.json'):
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        categorias = json.load(arquivo)
    return categorias




def calc_preco(empresa):
    return empresa.custo * (1 + empresa.margem)

def calc_disponibilidade(empresa):
    if empresa.oferta > 0:
        return True
    else:
        return False

def calc_preco(empresa):
    return empresa.custo * (1 + empresa.margem)

def calc_disponibilidade(empresa):
    if empresa.oferta > 0:
        return True
    else:
        return False

def comprar(pessoa, empresa):
    empresa.vendas += 1
    empresa.oferta -= 1
    pessoa.patrimonio -= calc_preco(empresa)
    pessoa.conforto += empresa.qualidade

# Pesquisar melhor produto de uma categoria 
def escolher_melhor(categoria, empresas, orcamento):
    melhor_empresa = None
    for empresa in empresas:
        if empresa.categoria == categoria and empresa.oferta > 0:
            preco = calc_preco(empresa)
            if preco <= orcamento:
                if melhor_empresa is None or empresa.qualidade > melhor_empresa.qualidade:
                    melhor_empresa = empresa
                elif empresa.qualidade == melhor_empresa.qualidade:
                    if calc_preco(empresa) < calc_preco(melhor_empresa):
                        melhor_empresa = empresa

    return melhor_empresa

# Pesquisar produto mais barato de uma categoria 
def escolher_barato(categoria, empresas, orcamento):
    melhor_empresa = None
    for empresa in empresas:
        if empresa.categoria == categoria and empresa.oferta > 0:
            preco = calc_preco(empresa)
            if preco <= orcamento:
                if melhor_empresa is None or preco < calc_preco(melhor_empresa):
                    melhor_empresa = empresa

    return melhor_empresa

# Calcular a renda mensal total da pessoa, incluindo renda passiva
def calc_renda_mensal(pessoa):
    return pessoa.salario + (pessoa.patrimonio * 0.005)

def simular_empresa(empresa):
    # Se a oferta zerou quer dizer que a empresa vendeu tudo
    if empresa.oferta == 0:
        empresa.reposicao += 1
        empresa.margem += 0.01

    # Se a oferta está alta, quer dizer que as vendas foram aquém
    elif empresa.oferta > 10:
        empresa.reposicao = max(0, empresa.reposicao - 1)
        if(empresa.margem > 0.01):
            empresa.margem -= 0.01

    # Repor o estoque de produtos
    empresa.oferta += empresa.reposicao  # Exemplo de reposição de estoque
    empresa.vendas = 0  # Resetar vendas após reposição

def simular_pessoa(pessoa, empresas, categorias):
    # Reinicializar conforto da pessoa
    pessoa.conforto = 0.0

    # Fazer compras dentro do orçamento para cada categoria
    # e atualizar o conforto da pessoa

    # Renda passiva
    # Aplicar o percentual de rendimento no patrimônio da pessoa como renda passiva
    renda_total = calc_renda_mensal(pessoa)

    pessoa.patrimonio += renda_total  # Atualizar patrimônio com a renda total

    for categoria,valor in categorias.items():
        # Comprar o produto de melhor qualidade 
        # que caiba no orçamento da pessoa para aquela categoria
        percentual = valor
        orcamento = renda_total * percentual
        patrimonio = pessoa.patrimonio
        empresa = escolher_melhor(categoria, empresas, orcamento)
        if empresa is None:
            empresa = escolher_barato(categoria, empresas, patrimonio)

        # Se encontrou um produto, comprar e atualizar o conforto
        if empresa is not None:
            comprar(pessoa, empresa)

def simular_mercado(pessoas, empresas,categorias):
    global meses_simulados
    # Atualização das empresas e produtos
    for empresa in empresas:
        simular_empresa(empresa)

    # Atualização das pessoas e seus patrimônios
    for pessoa in pessoas:
        simular_pessoa(pessoa, empresas, categorias)
    meses_simulados += 1
    if interface.get("tree_pessoas"):
        atualizar_interface(pessoas, empresas)
    print("Simulação concluída!")
def print_pessoas(pessoas,categorias):
    print()
    print("[PESSOAS]")

    # Imprimir em uma linha os percentuais dedicados à cada categoria
    print(f"{i}Divisão da renda mensal ", end="")
    for categoria, percentual in zip(categorias, categorias.values()):
        print(f"| {categoria} ", end="")
        print(f"{Y}{percentual * 100:3.1f}%{r}{i} ", end="")
    soma = sum(categorias.values())
    print(f"{i} | Totalizando {Y}{soma * 100:3.1f}%{r}{i} da renda mensal total.{r}")

    # Imprimir as pessoas e seus patrimônios
    max_renda_total = int(max(calc_renda_mensal(p) for p in pessoas))
    max_renda_total = 10000
    step = max_renda_total // 10

    print(f"{i}Gráfico de Barras | Legenda: {B}Conforto{r}{i}, {G}Salário{r}{i}, {P}Rendimentos{r}", end="")
    print(f"{i} | Cada traço = R${step:.2f}{r}{B}")

    for conforto in range(10, 1, -1):
        for pessoa in pessoas:
            char = " "
            if pessoa.conforto // len(categorias) >= conforto:
                char = "|"
            print(char, end="")
        print()

    print(f"{r}", end="")
    for pessoa in pessoas:
        print("-", end="")
    print()

    for renda_total in range(step, max_renda_total, step):
        for pessoa in pessoas:
            char = " "
            if calc_renda_mensal(pessoa) >= renda_total:
                if pessoa.salario >= renda_total:
                    char = f"{G}|{r}"
                else:
                    char = f"{P}|{r}"
            print(char, end="")
        print()
    print(f"{r}", end="")

def print_empresas(empresas):
    print()
    print("[EMPRESAS]")

    for empresa in empresas:
        print(f"|{empresa.categoria}| \t"
              f"{empresa.nome}: {empresa.produto} "
              f"{C}Q={empresa.qualidade}{r} Margem: {Y}{empresa.margem * 100:3.1f}%{r}\t"
              f"Custo: {R}R$ {empresa.custo:.2f}{r}\t"
              f"Preço: {G}R$ {calc_preco(empresa):.2f}{r}\t"
              f"Lucro T.: {G}R$ {(empresa.vendas * empresa.custo * empresa.margem):.2f}{r}\t"
              f"Vendas: ", end="")
        
        for i in range(empresa.vendas // 5):
            print(f"{G}${r}", end="")

        print()


def simular_mercado_meses(pessoas, empresas,categorias, meses):
    for _ in range(meses):
                simular_mercado(pessoas, empresas,categorias)
    atualizar_interface(pessoas, empresas)

def atualizar_interface(pessoas,empresas):
    for item in interface["tree_pessoas"].get_children():
        interface["tree_pessoas"].delete(item)
    popular_treeview_pessoas(interface["tree_pessoas"], pessoas)

    for item in interface["tree_empresas"].get_children():
        interface["tree_empresas"].delete(item)
    popular_treeview_empresas(interface["tree_empresas"], empresas)

    for widget in interface["graficos_frame"].winfo_children():
        widget.destroy()
    criar_graficos(interface["graficos_frame"], pessoas)

    interface["meses_label"]["text"] = f"Meses simulados: {meses_simulados}"

def simulador_console():
    simular = True
    pessoas = ler_pessoas() 
    empresas = ler_empresas()
    categorias = ler_categorias()
    while simular:
        clear()
        print("[SIMULADOR DE RELAÇÕES DE MERCADO]")

        print_pessoas(pessoas)        
        print_empresas(empresas)

        resposta = input("\nDigite um número para avançar N meses, 'enter' para avançar 1 mês ou 'sair' para encerrar: ").strip().lower()
        
        if resposta.isdigit():
            meses = int(resposta)
            for _ in range(meses):
                simular_mercado(pessoas, empresas,categorias)

        elif resposta == "":
            simular_mercado(pessoas, empresas,categorias)

        elif resposta == "sair":
            simular = False
    
def criar_treeview_pessoas(frame):
    cols = ("Nome", "Patrimônio", "Salário", "Renda Mensal", "Conforto")
    tree = ttk.Treeview(frame, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        if col == "Nome":
            tree.column(col, width=200)
        else:
            tree.column(col, width=100, anchor=tk.E)
    tree.pack(fill=tk.BOTH, expand=True)
    return tree

def criar_treeview_empresas(frame):
    cols = ("Categoria", "Nome", "Produto", "Qualidade", "Margem", "Custo", "Preço", "Lucro Total", "Vendas")
    tree = ttk.Treeview(frame, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        if col in ("Categoria", "Nome", "Produto"):
            tree.column(col, width=130)
        else:
            tree.column(col, width=80, anchor=tk.E)
    tree.pack(fill=tk.BOTH, expand=True)
    return tree

def popular_treeview_pessoas(tree,pessoas):
    tree.delete(*tree.get_children())
    for i, p in enumerate(pessoas):
        renda = calc_renda_mensal(p)
        tree.insert("", tk.END, values=(
            f"{p.nome}",
            f"R$ {p.patrimonio:,.2f}",
            f"R$ {p.salario:,.2f}",
            f"R$ {renda:,.2f}",
            f"{p.conforto:.1f}"
        ))

def popular_treeview_empresas(tree,empresas):
    tree.delete(*tree.get_children())
    for e in empresas:
        preco = e.custo * (1 + e.margem)
        lucro_total = e.vendas * e.custo * e.margem
        tree.insert("", tk.END, values=(
            e.categoria,
            e.nome,
            e.produto,
            f"{e.qualidade:.1f}",
            f"{e.margem*100:.1f}%",
            f"R$ {e.custo:,.2f}",
            f"R$ {preco:,.2f}",
            f"R$ {lucro_total:,.2f}",
            e.vendas
        ))

def criar_graficos(frame,pessoas):
    fig, axs = plt.subplots(2, 1, figsize=(12,6), constrained_layout=True)

    salarios = [p.salario for p in pessoas]
    rendimentos = [p.patrimonio * 0.005 for p in pessoas]
    indices = range(len(pessoas))

    axs[0].bar(indices, salarios, label="Salário", color='green')
    axs[0].bar(indices, rendimentos, bottom=salarios, label="Rendimentos", color='magenta', alpha=0.6)
    axs[0].set_ylabel("R$")
    axs[0].legend()

    conforto = [p.conforto for p in pessoas]
    axs[1].bar(indices, conforto, label="Nível de Conforto", color='blue')
    axs[1].legend()
    for ax in axs:
        ax.set_xticks([])

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


pessoas = ler_pessoas() 
empresas = ler_empresas()
categorias = ler_categorias() 
def resetar_simulacao():
    global meses_simulados
    meses_simulados = 0

    # Recarrega os dados iniciais dos arquivos
    novas_pessoas = ler_pessoas()
    novas_empresas = ler_empresas()
    novas_categorias = ler_categorias()

    # Atualiza os dados nas estruturas e na interface
    pessoas.clear()
    pessoas.extend(novas_pessoas)

    empresas.clear()
    empresas.extend(novas_empresas)

    categorias.clear()
    categorias.update(novas_categorias)

    # Atualiza interface
    popular_treeview_pessoas(interface["tree_pessoas"], pessoas)
    popular_treeview_empresas(interface["tree_empresas"], empresas)
    criar_graficos(interface["graficos_frame"], pessoas)
    interface["meses_label"].config(text=f"Meses simulados: {meses_simulados}")
    
    
def simulador_tkinter():
    root = tk.Tk()
    root.title("Simulador de Relações de Mercado")
    root.geometry("1400x900")

    fonte_titulo = ("Arial", 20, "bold")
    fonte = ("Arial", 12)
    fonte_codigo = ("Courier New", 11)

    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Título
    titulo = ttk.Label(main_frame, text="SIMULADOR DE RELAÇÕES DE MERCADO",
                      font=fonte_titulo, foreground="#007acc")
    titulo.pack(pady=(0,10))

    # Controle simulação (Meses e botões)
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(fill=tk.X, pady=(0,10))

    ttk.Label(control_frame, text="Meses para simular:", font=fonte).pack(side=tk.LEFT, padx=(0,5))
    meses_entry = ttk.Entry(control_frame, width=5, font=fonte)
    meses_entry.pack(side=tk.LEFT, padx=(0,15))
    meses_entry.insert(0, "1")

    btn_simular = ttk.Button(control_frame, text="Simular",command= lambda:simular_mercado_meses(pessoas, empresas,categorias, int(meses_entry.get())))
    btn_simular.pack(side=tk.LEFT, padx=5)

    btn_simular_1 = ttk.Button(control_frame, text="Simular 1 Mês",command=lambda:simular_mercado(pessoas, empresas, categorias))
    btn_simular_1.pack(side=tk.LEFT, padx=5)

    btn_resetar = ttk.Button(control_frame, text="Resetar",command= lambda:resetar_simulacao())
    btn_resetar.pack(side=tk.LEFT, padx=5)

    meses_label = ttk.Label(control_frame, text=f"Meses simulados: {meses_simulados}", font=fonte)
    meses_label.pack(side=tk.RIGHT)

    # Notebook (abas)
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Aba Categorias
    categoria_frame = ttk.Frame(notebook)
    notebook.add(categoria_frame, text="Categorias")

    ttk.Label(categoria_frame, text="Divisão da Renda Mensal", font=fonte,
              foreground="#007acc").pack(pady=10)

    categoria_text = scrolledtext.ScrolledText(categoria_frame,
                                               font=fonte_codigo,
                                               bg="white",
                                               fg="black")
    categoria_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    texto_categorias = "CATEGORIAS\n\nDivisão da renda mensal:\n\n"
    
    total_renda = sum(categorias.values())
    for categoria, percentual in categorias.items():
        texto_categorias += f"{categoria}: {percentual * 100:.1f}%\n"

    texto_categorias += f"\nTotal: {total_renda * 100:.1f}% da renda mensal\n"
    
    categoria_text.insert(tk.END, texto_categorias)
    categoria_text.config(state=tk.DISABLED)

    pessoas_frame = ttk.Frame(notebook)
    notebook.add(pessoas_frame, text="Pessoas")

    label_pessoas = ttk.Label(pessoas_frame, text="Pessoas e Patrimônios",
                              font=fonte, foreground="#007acc")
    label_pessoas.pack(pady=10)

    tree_pessoas = criar_treeview_pessoas(pessoas_frame)
    popular_treeview_pessoas(tree_pessoas,pessoas)

    empresas_frame = ttk.Frame(notebook)
    notebook.add(empresas_frame, text="Empresas")

    label_empresas = ttk.Label(empresas_frame, text="Empresas e Produtos",
                               font=fonte, foreground="#007acc")
    label_empresas.pack(pady=10)

    tree_empresas = criar_treeview_empresas(empresas_frame)
    popular_treeview_empresas(tree_empresas,empresas)
    graficos_frame = ttk.Frame(notebook)
    notebook.add(graficos_frame, text="Gráficos")

    criar_graficos(graficos_frame,pessoas)

    interface["tree_pessoas"] = tree_pessoas
    interface["tree_empresas"] = tree_empresas
    interface["graficos_frame"] = graficos_frame
    interface["meses_label"] = meses_label
    root.mainloop()


def main():
    while True:
        print("Escolha o tipo de interface:")
        print("1 - Interface de Console (original)")
        print("2 - Interface Gráfica (tkinter)")
        escolha = input("Digite sua escolha (1 ou 2): ").strip()

        if escolha == "1":
            simulador_console()
            break
        elif escolha == "2":
            simulador_tkinter()
            break
        else:
            print("Escolha inválida. Tente novamente.\n")


# Iniciar a simulação
if __name__ == "__main__":
    main()
















# Desconsiderar daqui para baixo, é só um exemplo de código comentado

# # ----------------------------------------------

# # Parte 1, classes com métodos de impressão e atualização

# class Data:
#     def __init__(self, dia, mes, ano):
#         self.dia = dia
#         self.mes = mes
#         self.ano = ano
#         self.meses = ["janeiro",  "fevereiro", 
#                       "março",    "abril", 
#                       "maio",     "junho", 
#                       "julho",    "agosto", 
#                       "setembro", "outubro",
#                       "novembro", "dezembro"]
    
#     def __str__(self):
#         return f"{self. dia} de {self.meses[self.mes - 1]} de {self.ano}"

# data = Data(1, 5, 2025)
# print(data)  # Saída: 1 de maio de 2025


# # Coletar nome
# def coletar_nome():
#     nome = input("Digite seu nome: ")
#     return nome

# # Coletar data de nascimento
# def coletar_data_nascimento():
#     dia = int(input("Digite o dia do seu nascimento: "))
#     mes = int(input("Digite o mês do seu nascimento: "))
#     ano = int(input("Digite o ano do seu nascimento: "))
#     return Data(dia, mes, ano)

# # Coletar dados do usuário
# def coletar_dados():
#     nome = coletar_nome()
#     data_nascimento = coletar_data_nascimento()
#     return nome, data_nascimento

# class Investimento:
#     def __init__(self, 
#                  aporte, 
#                  percentual = 0.95, 
#                  recorrente = False):
#         self.tipo = "LCI"
#         self.indexador = "CDI"
#         self.percentual = percentual
#         self.aporte = aporte
#         self.investido = aporte
#         self.recorrente = recorrente
#         self.resgate = aporte

#     def __str__(self):
#         recorrente_str = 'U'
#         if self.recorrente:
#             recorrente_str = 'R'
#         return (f"[{recorrente_str}]"
#                 f"[{self.tipo} de "
#                 f"{self.percentual:.2f} do {self.indexador}% "
#                 f"{Y}R${self.investido:.2f}{r}, "
#                 f"{G}R${self.resgate:.2f}{r}]")

# # ----------------------------------------------

# # Parte 2, funções de controle do programa

# def clear():
#     os.system('cls' if os.name == 'nt' else 'clear')

# def intro():
#     clear()
#     print(f"[SIMULADOR DE INVESTIMENTOS RECORRENTES]"); time.sleep(delay_longo)
#     print()
#     print(f"{i}Bem vindo, vamos simular também investimentos recorrentes!{r}"); time.sleep(delay_curto)
#     print(f"{i}Neste exercício vamos usar somente LCIs, sem cálculo de IR dessa vez{r}"); time.sleep(delay_curto)
#     print()
#     time.sleep(delay_longo)
#     print(f"{i}Iniciando as simulações...{r}"); time.sleep(delay_longo)    
#     print()
#     time.sleep(delay_longo)

# def menu():
#     resposta = input(f"Digite [{B}novo{r}] investimento, [{B}sair{r}] ou aperte [{B}enter{r}] para avançar em um mês: ")
#     clear()

#     return resposta

# def avancar_mes(data):
#     data.mes += 1
#     if data.mes > 12:
#         data.mes = 1
#         data.ano += 1

# def add_investimento(investimentos):
#     print()
#     percentual = float(input(f"Qual o percentual? ({B}% do CDI{r}) "))
#     aporte = float(input(f"Qual o {B}valor{r} do aporte de entrada? "))
#     recorrente = input(f"Serão depósitos mensalmente recorrentes? ({B}sim/não{r}) ").strip().lower() == "sim"
    
#     inv = Investimento(aporte, percentual, recorrente)
#     investimentos.append(inv)

#     time.sleep(delay_curto)
#     print(f"\n{i}Investimento adicionado com sucesso!{r}")
#     time.sleep(delay_longo)
#     time.sleep(delay_longo)
#     clear()

# def print_data(data):
#     print(f"{i}resumo da simulação em {P}{data}{r}")
#     print("\n...\n")

# def print_investimento(inv, max_resgate):
#     print(inv, end ='  \t')            
#     print_barra(inv, max_resgate, char="$", color=G)

# def print_barra(inv, max_resgate, char="$", color=G):
#     unidades = 0
#     max_unidades = 50
#     valor_unidade = 1000

#     if max_resgate < max_unidades * valor_unidade:
#         unidades = int(inv.resgate // valor_unidade)
#     else:
#         unidades = int(50 * inv.resgate / max_resgate)

#     print(f"{color}", end="")
#     for _ in range(unidades):
#         print(char, end="")
#     print(f"{r}")

# def calc_taxa_mensal(inv, indexador):
#     taxa_mensal = (1 + (inv.percentual / 100.0) * indexador) ** (1/12)
#     return taxa_mensal

# def atualizar_investimento(inv, indexador):
#     taxa_mensal = calc_taxa_mensal(inv, indexador)
#     inv.resgate = inv.resgate * taxa_mensal
    
#     # Se for recorrente, adicionar o valor de entrada mensal
#     if inv.recorrente:
#         inv.investido += inv.aporte
#         inv.resgate += inv.aporte

# def encontrar_resgate_maximo(investimentos):
#     max_resgate = 0.0
#     for inv in investimentos:
#         if inv.resgate > max_resgate:
#             max_resgate = inv.resgate
#     return max_resgate

# def simular_mes(investimentos, data, indexador):
#     print("[SIMULAÇÃO]\n")

#     max_resgate = encontrar_resgate_maximo(investimentos)

#     for inv in investimentos:
#         print_investimento(inv, max_resgate)
#         atualizar_investimento(inv, indexador)

#     print_data(data)
#     avancar_mes(data)

# def sair():
#     time.sleep(delay_curto)
#     print(f"{i}Ok, finalizando a simulação.{r}")
#     time.sleep(delay_longo)
#     print()
#     clear()
#     return False

# # ----------------------------------------------

# # Parte 3, controle do fluxo do programa
# cdi  = 0.1465
# data = Data(1, 5, 2025)
# investimentos = []

# clear()
# intro()

# simular = True
# while simular:

#     resposta = menu()

#     if resposta == "novo":
#         add_investimento(investimentos)
        
#     elif resposta == "":
#         simular_mes(investimentos, data, cdi)

#     elif resposta == "sair":
#         simular = sair()