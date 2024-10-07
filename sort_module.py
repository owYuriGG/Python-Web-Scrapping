import json
import os
import heapq
import time

def bubble_sort(lst, key):
    for _ in range(len(lst)):
        changed = False
        for j in range(len(lst) - 1):
            if lst[j][key] > lst[j + 1][key]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                changed = True
        if not changed:
            return lst
    return lst

def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))

def divide_arquivo(arquivo, tamanho_subarquivo):
    subarquivos = []

    with open(arquivo, 'r') as arq:
        buffer = []
        while True:
            linha = arq.readline()
            if not linha:
                break

            try:
                buffer.append(json.loads(linha.strip()))
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar linha como JSON: {linha}")
                raise e

            if len(buffer) >= tamanho_subarquivo:
                for item in buffer:
                    item["preco"] = float(item["preco"])

                buffer_ordenado = bubble_sort(buffer, key="preco")

                # Escreve cada item do buffer ordenado em uma nova linha no subarquivo
                subarquivo_nome = f"subfile_{len(subarquivos)}.txt"
                subarquivos.append(subarquivo_nome)
                with open(subarquivo_nome, 'w') as subarq:
                    for item in buffer_ordenado:
                        subarq.write(json.dumps(item) + '\n')

                buffer = []

        if buffer:
            for item in buffer:
                item["preco"] = float(item["preco"])

            buffer_ordenado = bubble_sort(buffer, key="preco")
            subarquivo_nome = f"subfile_{len(subarquivos)}.txt"
            subarquivos.append(subarquivo_nome)
            with open(subarquivo_nome, 'w') as subarq:
                for item in buffer_ordenado:
                    subarq.write(json.dumps(item) + '\n')

    return subarquivos

def merge_subarquivos(subarquivos, arquivo_saida):
    min_heap = []

    arquivos_abertos = [open(sub, 'r') for sub in subarquivos]
    for i, arq in enumerate(arquivos_abertos):
        linha = arq.readline()
        if linha:
            dado = json.loads(linha.strip())
            heapq.heappush(min_heap, (dado["preco"], i, dado))

    with open(arquivo_saida, 'w+') as arq_saida:
        while min_heap:
            _, index, menor_dado = heapq.heappop(min_heap)
            arq_saida.write(json.dumps(menor_dado) + '\n')

            # Ler a próxima linha do arquivo que tinha o menor elemento
            linha = arquivos_abertos[index].readline()
            if linha:
                dado = json.loads(linha.strip())
                heapq.heappush(min_heap, (dado["preco"], index, dado))

    for arq in arquivos_abertos:
        arq.close()

    for subarquivo in subarquivos:
        os.remove(subarquivo)

def merge_sort_externo(arquivo_entrada, tamanho_subarquivo, arquivo_saida):

    tamanho_subarquivo = tamanho_subarquivo * 1024 * 1024  # Convertendo para bytes
    script_dir = get_script_dir()
    arquivo_entrada_path = os.path.join(script_dir, arquivo_entrada)
    arquivo_saida_path = os.path.join(script_dir, arquivo_saida)

    subarquivos = divide_arquivo(arquivo_entrada_path, 12)
    merge_subarquivos(subarquivos, arquivo_saida_path)
