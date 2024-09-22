import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page():
    servico = Service('C:/msedgedriver.exe')
    driver = webdriver.Edge(service=servico)
    url = "https://store.steampowered.com/search/?filter=topsellers"
    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        html = driver.page_source

        caminho_arquivo = os.path.join('..', 'pagina_scrap.txt')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("O conteúdo do body da página foi salvo no arquivo 'pagina_scrap.txt'.")
    finally:
        driver.quit()

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
            game['preco'] = value
    return game

def separate_games():
    caminho_arquivo = os.path.join('..', 'pagina_scrap.txt')
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
    return games

def main():
    get_page()
    games = separate_games()

    for game in games:
        print(f'Jogo: {game['nome']}, Preço: R${game['preco']}, Data de lançamento: {game['lancamento']} \n')

main()