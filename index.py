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
    games = []
    opc = 0

    while opc != '5':
        opc = menu()

        if opc == '1':
            clear()
            get_page()
        elif opc == '2':
            clear()
            extrair_jogos()
        elif opc == '3':
            clear()
            tamnho_sub = int_input_validado("Digite o quanto de memoria deseja utilizar: (EM MBs)")
            games = merge_sort_externo(r"txts/games.txt", tamnho_sub, r"txts/games-ordenados.txt")
            print("Dados ordenados! ")

        elif opc == '4':
            clear()
            if games:
                caminho_arquivo = os.path.join('jogos_ordenados.txt')
                with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                    for game in games:
                        linha = f"Jogo: {game['nome']}, Preço: R${game['preco']}, Data de lançamento: {game['lancamento']}\n"
                        print(linha)
                        arquivo.write(linha)
            else:
                print("[ERRO] Nenhum dado extraído ainda!")
                print("Você extraíu os dados do Scrap?")
        elif opc == '5':
            print("Até breve!")

main()