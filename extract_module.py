import json
import os

def get_game_name(linhas, game, i):
    gravar = False
    qtd = 0
    for j in linhas[i+2]:
        if gravar:
            if j == '<':
                gravar = False
        if gravar and qtd < 2:
            game['nome'] = game['nome'] + j

        if not gravar:
            if j == '>':
                gravar = True
                qtd += 1
    return game

def get_game_data(linhas, game, i):
    gravar = True
    for j in linhas[i+7]:
        if j == '<':
            gravar = False
        if j != '' and j != ' ' and gravar:
            game['lancamento'] = game['lancamento'] + j
    return game

def get_game_price(linhas, game, i):
    achou = False
    for j in range(i, len(linhas)):
        if 'discount_final_price' in linhas[j] and achou == False:
            linha = linhas[j].split('<')
            achou = True

    for sublinha in linha:
        if 'discount_final_price' in sublinha:
            subsublinha = sublinha.split('>')
            value = ''
            for i in range(2, len(subsublinha[1])):
                if subsublinha[1][i] == ',':
                    value = value + '.'
                else: 
                    value = value + subsublinha[1][i]
            if value != 'atuito':
                game['preco'] = value
            else:
                game['preco'] = 0.0
    return game

def extrair_jogos():
    try:
        caminho_arquivo = os.path.join('txts/pagina_scrap.txt')
        arquivo = open(caminho_arquivo, 'r', encoding='utf-8')
        linhas = arquivo.readlines()

        games = []

        for i in range(len(linhas)):
            initial_game = {'nome': '', 'preco' : 0.0, 'lancamento': ''}

            if "responsive_search_name_combined" in linhas[i]:
                initial_game = get_game_name(linhas, initial_game, i)
                initial_game = get_game_data(linhas, initial_game, i)
                initial_game = get_game_price(linhas, initial_game, i)
                
                games.append(initial_game)

                with open(os.path.join('txts/games.txt'), 'a') as f:
                    f.write(json.dumps(initial_game) + '\n')
                    
        print("Jogos extraídos com sucesso!")
    except BaseException as error:
        print(f"[ERRO] Um erro inesperado aconteceu: {error}")
        print("Você realizou o Scrapping antes?")
        return []