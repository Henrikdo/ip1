
AZUL = "\033[94m"
ROSA = "\033[95m"
VERDE = "\033[92m"
ITALICO = "\033[3m"
RESET = "\033[0m"


CDI = 14.65
POUPANCA = 6.00
INFLACAO = 5.53
CDB_A = 100
CDB_B = 110
CDB_C = 120
LCA = 95


def calcular_ir(meses):
    if meses <= 6:
        return 22.5
    elif meses <= 12:
        return 20.0
    elif meses <= 24:
        return 17.5
    else:
        return 15.0
def perguntar_opcao():
    while True:
        opcao = input("Qual opção de investimento você escolhe? (A, B, C ou D): ").strip().upper()
        if opcao in ['A', 'B', 'C', 'D']:
            return opcao
        else:
            print("Opção inválida. Por favor escolha A, B, C ou D.")

def show_cdb_msg():
    print(f"{RESET}Como você escolheu um CDB vou te Lembrar as taxas regressivas de IR:{RESET}")
    print(f"{RESET}Até 6 meses:...... {ROSA}{calcular_ir(6):.2f}%{RESET}")
    print(f"{RESET}Até 12 meses:..... {ROSA}{calcular_ir(12):.2f}%{RESET}")
    print(f"{RESET}Até 24 meses:..... {ROSA}{calcular_ir(24):.2f}%{RESET}")
    print(f"{RESET}Acima de 24 meses: {ROSA}{calcular_ir(30):.2f}%{RESET}")
    
    

print(f"SIMULADOR DE INVESTIMENTOS")
print(f"{ITALICO}Olá, vou te ajudar a simular as possibilidades de investimentos{RESET}\n")


print("Pra começar, quero te dizer que as taxas anuais que estou utilizando são:")
print(f"{AZUL}IPCA {RESET}(inflação): {ROSA}{INFLACAO:.2f}%{RESET}")
print(f"{AZUL}CDI {RESET}(juros):...... {ROSA}{CDI:.2f}%{RESET}")
print(f"{AZUL}Poupança{RESET}:........ {ROSA}{POUPANCA:.2f}%{RESET}\n")


valor = float(input(f"Agora me informa o valor em reais que você quer investir {VERDE}R$ "))
print(f"{RESET}{ITALICO}Ok, registrei o valor de seu investimento.{RESET}\n")


print("Essas são as opções de investimento que tenho disponíveis para você:")
print(f"[A] {AZUL}CDB{RESET} valendo 100% do CDI, taxa final de {ROSA}{CDI:.2f}%{RESET}")
print(f"[B] {AZUL}CDB{RESET} valendo 110% do CDI, taxa final de {ROSA}{CDI * 1.10:.2f}%{RESET}")
print(f"[C] {AZUL}CDB{RESET} valendo 120% do CDI, taxa final de {ROSA}{CDI * 1.20:.2f}%{RESET}")
print(f"[D] {AZUL}LCA{RESET} valendo  95% do CDI, taxa final de {ROSA}{CDI * 0.95:.2f}%{RESET}")
print(f"{ITALICO}Obs.: Lembre que o CDB retém IR na fonte, enquanto a LCA não.{RESET}\n")

opcao = perguntar_opcao()
print(f"{ITALICO}Ok, registrei sua opção de investimento.{RESET}\n")
if opcao in ['A', 'B', 'C']:
    show_cdb_msg()

if opcao == 'A':
    taxa_anual = CDI * 1.00
elif opcao == 'B':
    taxa_anual = CDI * 1.10
elif opcao == 'C':
    taxa_anual = CDI * 1.20
elif opcao == 'D':
    taxa_anual = CDI * 0.95



tempo = int(input("Quanto tempo você gostaria de esperar para resgatar esse investimento? (em meses) "))
print(f"{ITALICO}Ok, registrei o tempo para o resgate.{RESET}\n")




taxa_ir = calcular_ir(tempo) if opcao in ['A', 'B', 'C'] else 0

taxa_mensal = (1 + taxa_anual / 100) ** (1 / 12) - 1
montante = valor * (1 + taxa_mensal) ** tempo
rendimento = montante - valor
imposto = rendimento * (taxa_ir / 100)
resgate = montante - imposto
lucro = resgate - valor

print(f"TAXAS UTILIZADAS")
print(f"- Taxa de IR aplicada...... {ROSA}{taxa_ir:.2f}%{RESET}")
print(f"- Taxa de rendimento anual. {ROSA}{taxa_anual:.2f}%{RESET}")
print(f"- Taxa de rendimento mensal {ROSA}{taxa_mensal*100:.2f}%{RESET}\n")

# Mostrar resultado
print(f"RESULTADO")
print(f"Valor investido....... {VERDE}R$ {valor:.2f}{RESET}")
print(f"Rendendo pelo tempo de {AZUL}{tempo}{RESET} meses")
print(f"Dedução do IR de...... {ROSA}{taxa_ir:.2f}%{RESET}")
print(f"Valor deduzido é de... {VERDE}R$ {imposto:.2f}{RESET}")
print(f"O resgate será de..... {VERDE}R$ {resgate:.2f}{RESET}")
print(f"O lucro total será.... {VERDE}R$ {lucro:.2f}{RESET}\n")

ver_analises = input(f"{ITALICO}Você gostaria de ver algumas análises adicionais (sim/não)? ").strip().lower()

taxa_poup_mensal = (POUPANCA/12)/100
montante_poupanca = valor * (1 + taxa_poup_mensal) ** tempo
lucro_poup = montante_poupanca - valor
diferenca = resgate - montante_poupanca

inflacao_mensal = INFLACAO/12
inflacao_acumulada = (1 + inflacao_mensal/100) ** (tempo)
 
valor_corrigido = valor * inflacao_acumulada
desvalorizacao = valor/valor_corrigido

resgate_corrigido = resgate * desvalorizacao
poup_corrigida = montante_poupanca / inflacao_acumulada

if ver_analises == "sim":

    print(f"ANÁLISES POUPANÇA")
    print(f"Se você tivesse investido {VERDE}R$ {valor:.2f}{RESET}")
    print(f"na poupança, ao final dos {AZUL}{tempo}{RESET} meses")
    print(f"o valor resgatado seria.. {VERDE}R$ {montante_poupanca:.2f}{RESET}")
    print(f"e o lucro total.......... {VERDE}R$ {lucro_poup:.2f}{RESET}")
    print(f"A diferença de lucro é de {VERDE}R$ {diferenca:.2f}{RESET}\n")

    print(f"ANÁLISES INFLAÇÃO")
    print(f"A inflação acumulada foi de........................ {ROSA}{inflacao_acumulada*100:.2f}%{RESET}")
    print(f"resultando em uma desvalorização de................ {ROSA}{desvalorizacao*100:.2f}%{RESET}")
    print(f"Por exemplo, se você comprava algo por............. {VERDE}R$ {valor:.2f}{RESET}")
    print(f"O mesmo item custaria corrigido pela inflação será. {VERDE}R$ {valor_corrigido:.2f}{RESET}")
    print(f"O resgate proporcionalmente ao valor corrigido fica {VERDE}R$ {resgate_corrigido:.2f}{RESET}")
    print(f"Já na poupança o proporcional a essa correção seria {VERDE}R$ {poup_corrigida:.2f}{RESET}\n")


print(f"RESUMO")
print(f"Valor investido:......... {VERDE}R$ {valor:.2f}{RESET}")
print(f"Valor resgatado:......... {VERDE}R$ {resgate:.2f}{RESET}")
print(f"Se fosse na poupança:.... {VERDE}R$ {montante_poupanca:.2f}{RESET}")
print(f"Correção da inflação:.... {VERDE}R$ {valor_corrigido:.2f}{RESET}\n")
print(f"{ITALICO}Espero ter ajudado!{RESET}")
