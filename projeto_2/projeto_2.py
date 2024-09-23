# Rafael de Melo Oliveira - 20200013481
# Virgílio Schettini de Oliveira Neto - 20200013848

def carregar_paginas_arquivo(arquivo):
    # Ler o conteúdo do arquivo
    with open(arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    # O primeiro número é a quantidade de quadros de memória
    quadros_memoria = int(linhas[0].strip())
    
    # Os números subsequentes são as referências às páginas
    referencias_paginas = [int(linha.strip()) for linha in linhas[1:]]
    
    return quadros_memoria, referencias_paginas

def algoritmo_fifo(quadros_memoria, referencias_paginas):
    memoria = []
    faltas_paginas = 0

    for pagina in referencias_paginas:
        if len(memoria) < quadros_memoria:
            # Ainda há espaço nos quadros
            faltas_paginas += 1
            memoria.append(pagina)
        else:
            if pagina not in memoria:
                faltas_paginas += 1
                memoria.pop(0)
                memoria.append(pagina)

    return faltas_paginas

def algoritmo_lru(quadros_memoria, referencias_paginas):
    memoria = []
    faltas_paginas = 0

    for pagina in referencias_paginas:
        if len(memoria) < quadros_memoria:
            # Ainda há espaço nos quadros
            faltas_paginas += 1
            memoria.append(pagina)
        else:
            if pagina in memoria:

                indice = memoria.index(pagina)
                memoria.pop(indice)
                memoria.append(pagina)

            else:
                faltas_paginas += 1
                memoria.pop(0)
                memoria.append(pagina)
            
    
    return faltas_paginas

def algoritmo_otimo(quadros_memoria, referencias_paginas):
    memoria = []
    faltas_paginas = 0

    for i, pagina in enumerate(referencias_paginas):
        if pagina not in memoria:
            # Page fault: página não está na memória
            faltas_paginas += 1
            if len(memoria) < quadros_memoria:
                # Ainda há espaço nos quadros
                memoria.append(pagina)
            else:
                # Substituir a página que será usada mais tarde ou não será mais usada
                distancias_futuras = {}
                for pagina_memoria in memoria:
                    try:
                        distancias_futuras[pagina_memoria] = referencias_paginas[i+1:].index(pagina_memoria)
                    except ValueError:
                        distancias_futuras[pagina_memoria] = float('inf')  # Nunca será usada novamente
                
                pagina_substituir = max(distancias_futuras, key=distancias_futuras.get)
                memoria.remove(pagina_substituir)
                memoria.append(pagina)

    
    return faltas_paginas

# Função principal
if __name__ == "__main__":
    
    # Carregar quadros de memória e referências às páginas
    quadros_memoria, referencias_paginas = carregar_paginas_arquivo('entrada.txt')
    
    # Aplicar os algoritmos
    faltas_paginas_fifo = algoritmo_fifo(quadros_memoria, referencias_paginas)

    faltas_paginas_otimo = algoritmo_otimo(quadros_memoria, referencias_paginas)

    faltas_paginas_lru = algoritmo_lru(quadros_memoria, referencias_paginas)


    # Printar resultados
    print(f"FIFO {faltas_paginas_fifo}")    
    print(f"OTM {faltas_paginas_otimo}")
    print(f"LRU {faltas_paginas_lru}")
