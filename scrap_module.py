import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        caminho_arquivo = os.path.join('txts/pagina_scrap.txt')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Página extraída com sucesso! ")
        print("Salvando...")
    except BaseException as error:
        print(f"[ERRO] Um erro inesperado aconteceu: {error}")
    finally:
        driver.quit()