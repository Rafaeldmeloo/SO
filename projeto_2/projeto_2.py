# Rafael de Melo Oliveira - 20200013481
# Virgílio Schettini de Oliveira Neto - 20200013848

def ler_arquivo(arquivo):
    with open(arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    quadros = int(linhas[0].strip())
    paginas = [int(linha.strip()) for linha in linhas[1:]]
    
    return quadros, paginas

def FIFO(quadros, paginas):
    memoria = []
    faltas_paginas = 0

    for pagina in paginas:
        # verifica se ainda há espaço nos quadros
        if len(memoria) < quadros:
            faltas_paginas += 1
            memoria.append(pagina)

        else:
            # verifica se há falta de páginas
            if pagina not in memoria:
                faltas_paginas += 1
                memoria.pop(0)
                memoria.append(pagina)

    return faltas_paginas

def LRU(quadros, paginas):
    memoria = []
    faltas_paginas = 0

    for pagina in paginas:
        # verifica se ainda há espaço nos quadros
        if len(memoria) < quadros:
            faltas_paginas += 1
            memoria.append(pagina)

        else:
            # se a página já estiver na memória, deixar na última posição
            if pagina in memoria:
                indice = memoria.index(pagina)
                memoria.pop(indice)
                memoria.append(pagina)

            # retira a página menos recentemente usada
            else:
                faltas_paginas += 1
                memoria.pop(0)
                memoria.append(pagina)
            
    return faltas_paginas

def OTIMO(quadros, paginas):
    memoria = []
    faltas_paginas = 0

    for i in range(len(paginas)):
        pagina = paginas[i]
        
        if pagina in memoria:
            continue
        
        # verifica se ainda há espaço nos quadros
        if len(memoria) < quadros:
            memoria.append(pagina)
            faltas_paginas += 1

        else:
            paginas_futuras = paginas[i+1:]
            indices = []
            
            # encontra o índice da próxima aparição do quadro na memória
            for quadro in memoria:
                if quadro in paginas_futuras:
                    indices.append(paginas_futuras.index(quadro))

                else:
                    indices.append(float('inf'))  
            
            # substitui a página que não será usada por mais tempo
            memoria.pop(indices.index(max(indices)))
            memoria.append(pagina)
            faltas_paginas += 1

    return faltas_paginas


if __name__ == "__main__":
    quadros, paginas = ler_arquivo('entrada.txt')
    
    faltas_paginas_fifo  = FIFO(quadros, paginas)
    faltas_paginas_otimo = OTIMO(quadros, paginas)
    faltas_paginas_lru   = LRU(quadros, paginas)

    print(f"FIFO {faltas_paginas_fifo}")    
    print(f"OTM {faltas_paginas_otimo}")
    print(f"LRU {faltas_paginas_lru}")
