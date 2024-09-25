import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def clear():
    os.system("cls")

def selection_sort(games):
  for i in range(len(games)):
    menor_index = i
    for j in range(i+1, len(games)):
      if float(games[j]['preco']) < float(games[menor_index]['preco']):
        menor_index = j
    games[i], games[menor_index] = games[menor_index], games[i]

  return games

def get_page():
    caminho_driver = os.path.join('msedgedriver.exe')
    servico = Service(caminho_driver)
    driver = webdriver.Edge(service=servico)
    url = "https://store.steampowered.com/search/?filter=topsellers"

    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        html = driver.page_source

        caminho_arquivo = os.path.join('pagina_scrap.txt')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Página extraída com sucesso! ")
        print("Salvando...")
    except BaseException as error:
        print(f"[ERRO] Um erro inesperado aconteceu: {error}")
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
            if value != 'atuito':
                game['preco'] = value
            else:
                game['preco'] = 0.0
    return game

def extrair_jogos():
    try:
        caminho_arquivo = os.path.join('pagina_scrap.txt')
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
        print("Jogos extraídos com sucesso!")
        return games
    except BaseException as error:
        print(f"[ERRO] Um erro inesperado aconteceu: {error}")
        print("Você realizou o Scrapping antes?")
        return []

def menu():
    print("----- Python Web Scrapping -----")
    print("1 - Realizar Scrapping (baixar html da página)")
    print("2 - Extraír dados do scrap")
    print("3 - Ordenar dados")
    print("4 - Mostrar situação atual dos dados")
    print("5 - Sair")
    opc = str(input("Selecione uma opção: "))
    return opc

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
            games = extrair_jogos()
        elif opc == '3':
            clear()
            if games:
                games = selection_sort(games)
                print("Dados ordenados! ")
            else:
                print("[ERRO] Nenhum dado extraído ainda!")
                print("Você extraíu os dados do Scrap?")
        elif opc == '4':
            clear()
            if games:
                for game in games:
                    print(f'Jogo: {game['nome']}, Preço: R${game['preco']}, Data de lançamento: {game['lancamento']} \n')
            else:
                print("[ERRO] Nenhum dado extraído ainda!")
                print("Você extraíu os dados do Scrap?")
        elif opc == '5':
            print("Até breve!")

main()