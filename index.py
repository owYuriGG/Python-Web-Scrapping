import json
import os
from scrap_module import get_page
from sort_module import merge_sort_externo
from extract_module import get_game_data
from extract_module import get_game_name
from extract_module import get_game_price
from extract_module import extrair_jogos
from utilities_module import clear
from utilities_module import menu
from utilities_module import int_input_validado

def main():
    extraido = False
    ordenado = False
    opc = 0

    while opc != '5':
        opc = menu()

        if opc == '1':
            clear()
            get_page()
        elif opc == '2':
            clear()
            extraido = extrair_jogos()
        elif opc == '3':
            clear()
            if extraido:
                tamnho_sub = int_input_validado("Digite o quanto de memoria deseja utilizar: (EM MBs)")
                merge_sort_externo(r"txts/games.txt", tamnho_sub, r"txts/games-ordenados.txt")
                ordenado = True
                print("Dados ordenados! ")
            else:
                print("[ERRO] Você já extraiu os dados? ")

        elif opc == '4':
            clear()
            if ordenado:
                caminho_arquivo = os.path.join('txts/games-ordenados.txt')
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    for linha in arquivo:
                        game = json.loads(linha)
                        formatted_line = f"Jogo: {game['nome']}, Preço: R${game['preco']}, Data de lançamento: {game['lancamento']} \n"
                        print(formatted_line)
            elif extraido:
                caminho_arquivo = os.path.join('txts/games.txt')
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    for linha in arquivo:
                        game = json.loads(linha)
                        formatted_line = f"Jogo: {game['nome']}, Preço: R${game['preco']}, Data de lançamento: {game['lancamento']} \n"
                        print(formatted_line)
            else:
                print("[ERRO] Você extraiu ou ordenou os dados?")
        elif opc == '5':
            print("Até breve!")

main()