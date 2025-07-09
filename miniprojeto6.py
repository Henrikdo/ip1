import numpy as np
import os

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_menu():
    print("Menu:")
    print("1. Definir jogador X")
    print("2. Definir jogador O")
    print("3. Definir tamanho do tabuleiro")
    print("4. Definir tamanho da sequência")
    print("5. Mostrar placar")
    print("6. Iniciar novo jogo")
    print("7. Sair do jogo")

def mostrar_placar(placar):
    print("Placar:")
    for jogador, pontos in placar.items():
        print(f"{jogador}: {pontos}")
    input("Pressione Enter para continuar...")

def criar_tabuleiro(tamanho):
    return np.full((tamanho, tamanho), " ")

def mostrar_tabuleiro(tabuleiro):
    letras = [chr(ord('A') + i) for i in range(tabuleiro.shape[0])]
    print("  " + " ".join(str(i) for i in range(tabuleiro.shape[1])))
    for i, linha in enumerate(tabuleiro):
        print(" " + "-" * (tabuleiro.shape[1]*2))
        print(letras[i] + "|" + "|".join(linha) + "|")
    print(" " + "-" * (tabuleiro.shape[1]*2))

def obter_jogada(jogador, tamanho):
    entrada = input(f"{jogador}, escolha sua jogada (letra e número separados por espaço): ").strip().upper()
    letra, numero = entrada.split()

    linha = ord(letra) - ord('A')
    coluna = int(numero)

    if linha < 0 or linha >= tamanho or coluna < 0 or coluna >= tamanho:
        exit()

    return (linha, coluna)

def verificar_vitoria(tabuleiro, simbolo, sequencia):
    tamanho = tabuleiro.shape[0]

    for i in range(tamanho):
        for j in range(tamanho - sequencia + 1):
            if np.all(tabuleiro[i, j:j+sequencia] == simbolo):
                return True
            if np.all(tabuleiro[j:j+sequencia, i] == simbolo):
                return True

    for i in range(tamanho - sequencia + 1):
        for j in range(tamanho - sequencia + 1):
            if all(tabuleiro[i + k, j + k] == simbolo for k in range(sequencia)):
                return True
            if all(tabuleiro[i + k, j + sequencia - 1 - k] == simbolo for k in range(sequencia)):
                return True

    return False

def jogo_loop(jogador_x, jogador_o, tamanho, sequencia, placar):
    tabuleiro = criar_tabuleiro(tamanho)
    simbolos = {jogador_x: "X", jogador_o: "O"}
    jogadores = [jogador_x, jogador_o]
    turno = 0

    while True:
        limpar_tela()
        mostrar_tabuleiro(tabuleiro)
        jogador = jogadores[turno % 2]
        simbolo = simbolos[jogador]

        try:
            linha, coluna = obter_jogada(jogador, tamanho)
        except:
            exit()

        if tabuleiro[linha, coluna] != " ":
            continue

        tabuleiro[linha, coluna] = simbolo

        if verificar_vitoria(tabuleiro, simbolo, sequencia):
            limpar_tela()
            mostrar_tabuleiro(tabuleiro)
            print(f"{jogador} venceu!")
            placar[jogador] = placar.get(jogador, 0) + 1
            input("Pressione Enter para continuar...")
            break

        if np.all(tabuleiro != " "):
            print("Empate!")
            input("Pressione Enter para continuar...")
            break

        turno += 1

# === Inicialização ===

jogador_x = "Jogador X"
jogador_o = "Jogador O"
tamanho = 3
sequencia = 3
placar = {}

while True:
    limpar_tela()
    exibir_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        jogador_x = input("Digite o nome do jogador X: ")
    elif opcao == "2":
        jogador_o = input("Digite o nome do jogador O: ")
    elif opcao == "3":
        tamanho = int(input("Digite o tamanho do tabuleiro (3, 4, 5, ...):"))
    elif opcao == "4":
        sequencia = int(input("Digite o tamanho da sequência para vencer: "))
    elif opcao == "5":
        mostrar_placar(placar)
    elif opcao == "6":
        jogo_loop(jogador_x, jogador_o, tamanho, sequencia, placar)
    elif opcao == "7":
        print("Saindo do jogo...")
        break
    else:
        continue