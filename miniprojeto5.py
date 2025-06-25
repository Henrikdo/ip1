
from math import floor
import os

AZUL = "\033[94m"
VERDE = "\033[92m"
ROXO = "\033[95m"
AMARELO = "\033[93m"
RESET = "\033[0m"
VERMELHO = "\033[91m"

class Pessoa:
    def __init__(self, patrimonio, salario):
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



pessoas = []
empresas = []


categorias = [
    "Moradia",
    "Alimentação",
    "Transporte",
    "Saúde",
    "Educação"
]

percentuais = [
    0.35,  # Moradia
    0.25,  # Alimentação
    0.10,  # Transporte
    0.10,  # Saúde
    0.10   # Educação
]



def add_pessoas(num_pessoas, patrimonio, salario, variacao = (0,)):
    for i in range(num_pessoas):
        pessoas.append(Pessoa(patrimonio + i * variacao, salario + i * variacao))


add_pessoas(5, patrimonio=2000000, salario=0, variacao=0)       # Herdeiros milionários
add_pessoas(10, patrimonio=200000, salario=100000, variacao=-5000)  # Supersalários
add_pessoas(25, patrimonio=100000, salario=30000, variacao=-1000)   # Faixa salarial média-alta
add_pessoas(50, patrimonio=10000, salario=5000, variacao=-50)       # Faixa salarial baixa
add_pessoas(70, patrimonio=10000, salario=1518, variacao=0)         # Salário mínimo

empresas.append(Empresa("Moradia",     "    República A", "Aluguel, Várzea", 300.0,  qualidade=3))
empresas.append(Empresa("Moradia",     "    República B", "Aluguel, Várzea", 300.0,  qualidade=3))
empresas.append(Empresa("Moradia",     "CTI Imobiliária", "Aluguel, Centro", 1500.0, qualidade=7))
empresas.append(Empresa("Moradia",     "Orla Smart Live", "Aluguel, Boa V.", 3000.0, qualidade=9))
empresas.append(Empresa("Alimentação", "          CEASA", "Feira do Mês   ", 200.0,  qualidade=3))
empresas.append(Empresa("Alimentação", "    Mix Matheus", "Feira do Mês   ", 900.0,  qualidade=5))
empresas.append(Empresa("Alimentação", "  Pão de Açúcar", "Feira do Mês   ", 1500.0, qualidade=7))
empresas.append(Empresa("Alimentação", "      Home Chef", "Chef em Casa   ", 6000.0, qualidade=9))
empresas.append(Empresa("Transporte",  "  Grande Recife", "VEM  Ônibus    ", 150.0,  qualidade=3))
empresas.append(Empresa("Transporte",  "           UBER", "Uber Moto      ", 200.0,  qualidade=4))
empresas.append(Empresa("Transporte",  "             99", "99 Moto        ", 200.0,  qualidade=4))
empresas.append(Empresa("Transporte",  "            BYD", "BYD Dolphin    ", 3000.0, qualidade=8))
empresas.append(Empresa("Saúde",       "    Health Coop", "Plano de Saúde ", 200.0,  qualidade=2))
empresas.append(Empresa("Saúde",       "        HapVida", "Plano de Saúde ", 650.0,  qualidade=5))
empresas.append(Empresa("Saúde",       " Bradesco Saúde", "Plano de Saúde ", 800.0,  qualidade=5))
empresas.append(Empresa("Saúde",       "     Sulamérica", "Plano de Saúde ", 850.0,  qualidade=5))
empresas.append(Empresa("Educação",    "      Escolinha", "Mensalidade    ", 100.0,  qualidade=1))
empresas.append(Empresa("Educação",    "     Mazzarello", "Mensalidade    ", 1200.0, qualidade=6))
empresas.append(Empresa("Educação",    "      Arco Íris", "Mensalidade    ", 1800.0, qualidade=8))
empresas.append(Empresa("Educação",    "Escola do Porto", "Mensalidade    ", 5000.0, qualidade=9))



def print_pessoas(pessoas):
    print(f"\n[PESSOAS]")
    print("Divisão da renda mensal | Moradia 35.0% | Alimentação 25.0% | Transporte 10.0% | Saúde 10.0% | Educação 10.0% | Totalizando 90.0% da renda mensal total.")
    print("Gráfico de Barras | Legenda: " + AZUL + "Conforto" + RESET + ", " + VERDE + "Salário" + RESET + ", " + ROXO + "Rendimentos" + RESET + " | Cada traço = R$1000.00")

    count_barras_rendimentos = 0
    rendimento_bars_string = ""
    conforto_bars_string = ""
    for pessoa in pessoas:
        renda_salario = pessoa.salario
        renda_rendimento = pessoa.patrimonio * 0.05
        total = renda_salario + renda_rendimento

        conforto_barras = floor(pessoa.conforto * len(categorias))  # de 0 a 10
        salario_barras = floor(renda_salario // 1000)
        rendimento_barras = floor(renda_rendimento // 1000)

    

        conforto_str = "|" * conforto_barras
        salario_str = VERDE + "|" * salario_barras + RESET
        rendimento_str = ROXO + "|" * rendimento_barras + RESET

        if renda_rendimento <= 10000 and count_barras_rendimentos < 10:
            count_barras_rendimentos += 1
            if rendimento_bars_string == "":
                rendimento_bars_string = "-" * floor(total//1000) + "\n"
            rendimento_bars_string += rendimento_str + salario_str + "\n"
            conforto_bars_string += AZUL + conforto_str + RESET + "\n"
        

        
    print(conforto_bars_string)
    print(rendimento_bars_string)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def escolher_melhor(categoria, empresas, orcamento):
    melhor_empresa = None
    for empresa in empresas:
        if empresa.categoria == categoria and empresa.oferta > 0:
            preco = empresa.custo * (1 + empresa.margem)
            if preco <= orcamento:
                if melhor_empresa is None or empresa.qualidade > melhor_empresa.qualidade:
                    melhor_empresa = empresa
    return melhor_empresa


def escolher_barato(categoria, empresas, patrimonio):
    mais_barato = None
    for empresa in empresas:
        if empresa.categoria == categoria and empresa.oferta > 0:
            preco = empresa.custo * (1 + empresa.margem)
            if preco <= patrimonio:
                if mais_barato is None or preco < mais_barato.custo * (1 + mais_barato.margem):
                    mais_barato = empresa
    return mais_barato

def print_empresas(empresas):
    print(f"\n[EMPRESAS]")
    for emp in empresas:
        preco = emp.custo * (1 + emp.margem)
        lucro_unitario = preco - emp.custo
        lucro_total = lucro_unitario * emp.vendas

        vendas_barra = "$" * floor(emp.vendas/5)
        categoria_fmt = f"[{emp.categoria}]{' ' * max(0, 12 - len(emp.categoria))}"

        print(f"{categoria_fmt} {emp.nome:<20} {emp.produto:<15} {AZUL}Q={emp.qualidade:<1}{RESET} "
      f"Margem: {AMARELO}{int(emp.margem*100)}%{RESET}  "
      f"Custo: {VERMELHO}R$ {emp.custo:<7.2f}{RESET}  "
      f"Preço: {VERDE}R$ {preco:<7.2f}{RESET}  "
      f"Lucro T.: {VERDE}R$ {lucro_total:<7.2f}{RESET}  "
      f"Vendas: {VERDE}{vendas_barra}{RESET}")


def simular_pessoa(pessoa, empresas, categorias, percentuais):
    pessoa.conforto = 0
    rendimento_mensal = pessoa.salario + pessoa.patrimonio * 0.05
    pessoa.patrimonio += rendimento_mensal  # atualiza com rendimento mensal

    for i in range(len(categorias)):
        categoria = categorias[i]
        percentual = percentuais[i]
        orcamento = rendimento_mensal * percentual

        empresa = escolher_melhor(categoria, empresas, orcamento)

        if empresa is None:
            empresa = escolher_barato(categoria, empresas, pessoa.patrimonio*percentual)

        if empresa:
            preco = empresa.custo * (1 + empresa.margem)
            if preco <= pessoa.patrimonio:
                empresa.vendas += 1
                empresa.oferta -= 1
                pessoa.patrimonio -= preco
                pessoa.conforto += empresa.qualidade / 10  # conforto vai de 0 a 1 por categoria

def simular_empresa(empresa):
    if empresa.oferta == 0:
        empresa.reposicao += 1
        empresa.margem += 0.01
    elif empresa.oferta > 10:
        empresa.reposicao = max(0, empresa.reposicao - 1)

    if empresa.margem > 0.01:
        empresa.margem -= 0.01

    empresa.oferta += empresa.reposicao
    empresa.vendas = 0
              


def simular_mercado(pessoas, empresas, categorias, percentuais):

    for empresa in empresas:
        simular_empresa(empresa)


    for pessoa in pessoas:
        simular_pessoa(pessoa, empresas, categorias, percentuais)

    return None

def main():
    simular = True
    while simular:
        clear()
        print("[SIMULADOR DE RELAÇÕES DE MERCADO]")
        print_pessoas(pessoas)        
        print_empresas(empresas)

        resposta = input("\nDigite um número para avançar N meses, 'enter' para avançar 1 mês ou 'sair' para encerrar: ")
        if resposta.isdigit():
            meses = int(resposta)
            for _ in range(meses):
                simular_mercado(pessoas, empresas, categorias, percentuais)
        elif resposta == "":
            simular_mercado(pessoas, empresas, categorias, percentuais)
        elif resposta == "sair":
            simular = False

if __name__ == "__main__":
    main()
