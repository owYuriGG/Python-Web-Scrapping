import os

def clear():
    os.system("cls")

def menu():
    print("----- Python Web Scrapping -----")
    print("1 - Realizar Scrapping (baixar html da página)")
    print("2 - Extraír dados do scrap")
    print("3 - Ordenar dados")
    print("4 - Mostrar situação atual dos dados")
    print("5 - Sair")
    opc = str(input("Selecione uma opção: "))
    return opc