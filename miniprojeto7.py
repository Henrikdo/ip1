import os
import csv 
import json
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

categorias = []
pessoas = []
empresas = []

percentuais = [
    0.35,  # Moradia
    0.25,  # Alimentação
    0.10,  # Transporte
    0.10,  # Saúde
    0.10,  # Educação
]

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

def simular_pessoa(pessoa, empresas, categorias, percentuais):
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

def simular_mercado(pessoas, empresas, categorias, percentuais):
    # Atualização das empresas e produtos
    for empresa in empresas:
        simular_empresa(empresa)

    # Atualização das pessoas e seus patrimônios
    for pessoa in pessoas:
        simular_pessoa(pessoa, empresas, categorias, percentuais)        

def print_pessoas(pessoas,categorias):
    print()
    print("[PESSOAS]")

    # Imprimir em uma linha os percentuais dedicados à cada categoria
    print(f"{i}Divisão da renda mensal ", end="")
    for categoria, percentual in zip(categorias, percentuais):
        print(f"| {categoria} ", end="")
        print(f"{Y}{percentual * 100:3.1f}%{r}{i} ", end="")
    soma = sum(percentuais)
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


# Parte 3, simulação de mercado
# Enquanto não for digitado "sair", simular o mercado


def main():
    simular = True
    pessoas = ler_pessoas() 
    empresas = ler_empresas()
    categorias = ler_categorias()
    while simular:
        clear()
        print("[SIMULADOR DE RELAÇÕES DE MERCADO]")
    
        print_pessoas(pessoas,categorias)        
        print_empresas(empresas)

        # Aperte enter para avançar em 1 mês, digite um número para avançar N meses ou "sair" para encerrar
        resposta = input("\nDigite um número para avançar N meses, 'enter' para avançar 1 mês ou 'sair' para encerrar: ").strip().lower()
        
        if resposta.isdigit():
            meses = int(resposta)
            for _ in range(meses):
                simular_mercado(pessoas, empresas, categorias, percentuais)

        elif resposta == "":
            simular_mercado(pessoas, empresas, categorias, percentuais)

        elif resposta == "sair":
            simular = False

# Iniciar a simulação
if __name__ == "__main__":
    main()

