import os 
os.system('cls' if os.name == 'nt' else 'clear')
AZUL = "\033[94m"
ROSA = "\033[95m"
VERDE = "\033[92m"
AMARELO = "\033[33m"
ITALICO = "\033[3m"
RESET = "\033[0m"

CDI = 13.75
mes_atual = 0
meses = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho","agosto",
    "setembro", "outubro", "novembro", "dezembro"]

ano_base = 2025

class Investimento:
    def __init__(self, percentual: float, aporte_inicial: float, recorrente: bool):
        self.percentual = percentual
        self.aporte_inicial = aporte_inicial
        self.recorrente = recorrente
        self.total_investido = aporte_inicial
        self.resgate = 0.0

    def __str__(self):
        return (
            f"Investimento({self.percentual}% do CDI, "
            f"Aporte Inicial: R${self.aporte_inicial:.2f}, "
            f"Recorrente: {self.recorrente}, "
            f"Total Investido: R${self.total_investido:.2f}, "
            f"Resgate: R${self.resgate:.2f})"
        )

def calcular_rendimentos(investimentos):
    global mes_atual,ano_base,meses


    for inv in investimentos:
            cdi_mensal = CDI / 100 / 12
            rendimento = round(inv.total_investido * (inv.percentual / 100) * cdi_mensal,2)
            inv.resgate =  inv.total_investido + inv.resgate + rendimento

            cifroes = "\t"
            quantidade_de_cifroes = int(inv.resgate // 1000)

            for i in range(quantidade_de_cifroes):
                if i >= 50:
                    break
                cifroes += "$"
            
            tipo = "[R]" if inv.recorrente else "[U]"
            print(f"{tipo}[LCI de {inv.percentual:.2f} do CDI% "
                f"{AMARELO}R${inv.total_investido:.2f}{RESET}, "
                f"{VERDE}R${inv.resgate:.2f}{RESET}]{VERDE}{cifroes}{RESET}")
            if inv.recorrente:
                inv.total_investido += inv.aporte_inicial
            
    print(f"\n{ITALICO}resumo da simulação em {ROSA}{meses[mes_atual]} de {ano_base}{RESET}")
    mes_atual += 1

    if mes_atual % 11 == 0 and mes_atual > 0:
        ano_base += 1
        mes_atual = 0



       

def main():
    investimentos = []
    running = True
    print(f"[SIMULADOR DE INVESTIMENTOS RECORRENTES]\n")
    print(f"{ITALICO}Bem vindo, vamos simular também investimentos recorrentes!")
    print(f"{ITALICO}Neste exercício vamos usar somente LCIs, sem cálculo de IR dessa vez\n")
    print(f"{ITALICO}Iniciando as simulações...")
    
    while running:


        entrada = input(f"Digite {AZUL}[novo]{RESET} investimento, {AZUL}[sair]{RESET} ou aperte {AZUL}[enter]{RESET} para avançar em um mês: ")
        

        if entrada.lower() == 'novo':

            percentual = input(f"Qual o percentual? ({AZUL}% do CDI{RESET}) ")
            aporte = input(f"Qual o {AZUL}valor{RESET} do aporte de entrada? ")
            recorrente = input(f"Serão depósitos mensalmente recorrentes? ({AZUL}sim/não{RESET}) ")

            investimentos.append(
                Investimento(
                    percentual=float(percentual.strip('%')) if percentual else 0.0,
                    aporte_inicial=float(aporte) if aporte else 0.0,
                    recorrente=recorrente.lower() in ['sim', 's']
                )
            )

            print(f"\n{ITALICO}Investimento adicionado com sucesso!{RESET}")
        elif entrada.lower() == 'sair':
            break
        elif entrada.lower() == '':
            if len(investimentos) > 0:
                calcular_rendimentos(investimentos)



main()