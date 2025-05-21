
class Data:
    def __init__(self, dia, mes, ano):
        self.dia = dia
        self.mes = mes
        self.ano = ano

    def __str__(self):
        return f"{self.dia}/{self.mes}/{self.ano}"

class Gastos:
    def __init__(self, aluguel, feira, comida, transporte, outros):
        self.aluguel = aluguel
        self.feira = feira
        self.comida = comida
        self.transporte = transporte
        self.outros = outros

    def total(self):
        return self.aluguel + self.feira + self.comida + self.transporte + self.outros

class Financas:
    def __init__(self, salario, patrimonio, gastos: Gastos):
        self.salario = salario
        self.patrimonio = patrimonio
        self.gastos = gastos
        self.saldo = salario - gastos.total()
        self.investimento = 100 if self.saldo >= 100 else self.saldo

class Pessoa:
    def __init__(self, nome, data: Data, financas: Financas):
        self.nome = nome
        self.nasc = data
        self.financas = financas


print("Oi, pode me chamar de \033[36mDin\033[0m!")
print("Sou um assistente financeiro")
print("e vou tentar te ajudar com as \033[36mcontas\033[0m e os \033[36mobjetivos\033[0m.\n")

print("[DADOS PESSOAIS]\n")

nome = input("Primeiro, preciso de algumas informações\nMe diz teu \033[33mnome\033[0m: ")
dia = int(input("O \033[33mdia\033[0m em que tu nasceu: "))
mes = int(input("Agora o \033[35mmês\033[0m: "))
ano = int(input("E o \033[33mano\033[0m: "))

data_nascimento = Data(dia, mes, ano)

print("\n---\n")
print("Muito bem, então conferindo seus dados, estou registrando aqui.")
print(f"\033[32m{nome}\033[0m, nascimento em \033[32m{data_nascimento}\033[0m\n")

print("[DADOS FINANCEIROS]\n")

patrimonio = float(input("Agora me informa por favor alguns dados financeiros\n"
                         "Se você somar o dinheiro que tem guardado, me diz o total desse \033[33mpatrimônio\033[0m: R$ "))
salario = float(input("Me diz teu \033[33msalário\033[0m: R$ "))

print("\nSobre os seus gastos, me informa por partes por favor.")
aluguel = float(input("Quanto custa teu \033[33maluguel\033[0m, (incluindo condomínio e outras taxas): R$ "))
feira = float(input("Mais ou menos o quanto você gasta fazendo \033[33mfeira\033[0m todo mês: R$ "))
comida = float(input("E com \033[33mcomida\033[0m fora de casa, em média dá quanto: R$ "))
transporte = float(input("Na mobilidade, quanto que gasta com \033[33mtransporte\033[0m (ônibus, uber, gasolina, etc): R$ "))
outros = float(input("Pra terminar, quanto você gasta com \033[33moutros\033[0m (lazer, roupas, etc): R$ "))

gastos = Gastos(aluguel, feira, comida, transporte, outros)
financas = Financas(salario, patrimonio, gastos)
pessoa = Pessoa(nome, data_nascimento, financas)

print("\n---\n")
print(f"Obrigado \033[32m{pessoa.nome}\033[0m, resumindo as informações financeiras até agora.")
print("Os seus gastos discriminados são:")
print(f"\033[32mAluguel:\033[0m R$ {gastos.aluguel:.2f}")
print(f"\033[32mFeira:\033[0m R$ {gastos.feira:.2f}")
print(f"\033[32mComida:\033[0m R$ {gastos.comida:.2f}")
print(f"\033[32mTransporte:\033[0m R$ {gastos.transporte:.2f}")
print(f"\033[32mOutros:\033[0m R$ {gastos.outros:.2f}")
print(f"\033[32mGASTOS TOTAIS:\033[0m R$ {gastos.total():.2f}")

print("\n---\n")
print("Pra terminar, calculando o seu saldo mensal, com base em todos os gastos")
print(f"e no teu salário, o valor resultante é de \033[32mR$ {financas.saldo:.2f}\033[0m")
print("Desse valor, considerando que qualquer investimento é válido,")
print(f"o quanto você conseguiria \033[33minvestir\033[0m todo mês: R$ {financas.investimento:.2f}")
print(f"Ok, anotado, o valor do investimento mensal é \033[32mR$ {financas.investimento:.2f}\033[0m")
print("Acredito que coletei todas as informações necessárias")

nascimento = Data(dia,mes,ano)
gastos =  Gastos(aluguel,feira,comida,transporte,outros)
financas  = Financas(salario,patrimonio,gastos)
antonieta = Pessoa(nome,nascimento,financas)    


gastos_totais = (
    antonieta.financas.gastos.aluguel +
    antonieta.financas.gastos.feira +
    antonieta.financas.gastos.comida +
    antonieta.financas.gastos.transporte +
    antonieta.financas.gastos.outros    
)


print(f'\n---\n')

print('Agora organizei todos os seus dados de forma concentrada aqui no meu sistema')
print('Vou te mostrar como ficou:')
print(f'{antonieta.nome}, nascimento em {antonieta.nasc.dia}/{antonieta.nasc.mes}/{antonieta.nasc.ano}')
print(f'{antonieta.nome} tem {antonieta.financas.patrimonio} de patrimônio')
print(f'{antonieta.nome} tem {antonieta.financas.salario} de salário')
print(f'{antonieta.nome} tem {gastos_totais} de gastos')
print(f'{antonieta.nome} tem {antonieta.financas.investimento} de investimento')

print('\nAgora sim, vamos pensar no futuro! Você temum próximo objetivo financeiro?')
print('Um desejo de adquirir ou realizar algo que você quer e que precisa de investimento?')
print('Exemplos de objetivos assim são:')
print('Comprar uma moto ou um carro, fazer uma viagem, comprar uma casa, fazer um curso, etc.')
objetivo_nome = input('Qual seria esse seu próximo objetivo financeiro: ')
objetivo_valor = float(input('Qual o valor do \033[33mobjetivo\033[0m financeiro: R$ '))

print(f'\nEm uma conta simples que fiz aqui, sem considerar rendimentos ou inflação,')
print(f'com base na sua capacidade de investimento mensal de \033[1;32mR$ {antonieta.financas.investimento:.2f}\033[0m')
print(f'e o seu patrimônio atual de \033[32mR$ {antonieta.financas.patrimonio:.2f}\033[0m')

investimento_total = antonieta.financas.patrimonio
mensal = antonieta.financas.investimento
meses_necessarios = (objetivo_valor - investimento_total) / mensal
anos_necessarios = meses_necessarios / 12

print(f'Você conseguiria atingir o valor de \033[32mR$ {objetivo_valor:.2f}\033[0m em:')
print(f'{meses_necessarios:.2f} meses')
print(f'Ou {anos_necessarios:.2f} anos')

print('Por hora, é isso que tenho para te ajudar')
print('Espero que tenha sido útil')




