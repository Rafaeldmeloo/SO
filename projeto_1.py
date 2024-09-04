import math

class Processo:
    def __init__(self, id, chegada, duracao):
        self.id = id
        self.chegada = float(chegada)
        self.duracao = float(duracao)
        self.duracao_variavel = float(duracao)

# Função para processar a entrada a partir do arquivo 'entrada.txt'
def process_input(arquivo):
    processos = []  # Lista para armazenar os processos
    id = 1

    try:
        # Abrir o arquivo especificado para leitura
        with open(arquivo, 'r') as file:
            # Ler linha por linha do arquivo
            for line in file:
                # Separar os números de cada linha
                chegada, duracao = map(int, line.split())
                # Criar um objeto Processo e adicioná-lo à lista
                processo = Processo(id, chegada, duracao)
                id += 1
                processos.append(processo)
    
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado.")
    
    # Retorna a lista de processos
    return processos

# Função para calcular os tempos médios usando First Come First Send
def FCFS(processos):
    fila_processos = []
    n = len(processos)
    tempo = 0

    tempos_retorno = 0
    tempos_resposta = 0
    tempos_espera = 0

    for processo in processos:
        if len(fila_processos) == 0:
            fila_processos.append(processo)
            tempos_retorno += processo.duracao
            tempo += processo.duracao
        else:
            tempos_retorno += processo.duracao + tempo - processo.chegada
            tempos_resposta += tempo - processo.chegada
            tempos_espera += tempo - processo.chegada
            tempo += processo.duracao

    media_retorno = tempos_retorno/ n
    media_resposta = tempos_resposta / n
    media_espera = tempos_espera / n

    return media_retorno, media_resposta, media_espera

# Função para calcular os tempos médios usando Round Robin
def RR(processos, quantum):
    fila_prontos = []
    processos_terminados = 0
    n = len(processos)
    fila_processamento = []
    tempo = 0
    tempo_processo = 0

    while(n != processos_terminados):
        for i, processo in enumerate(processos):
            if(tempo == processo.chegada):
                fila_prontos.append(processo)

        if fila_prontos != 0:
            if tempo == 0:       
                fila_processamento.append(fila_prontos[0].id)
                # print(f'{fila_processamento[-1]} no tempo {tempo}')

            elif tempo_processo == quantum:
                fila_prontos[0].duracao_variavel -= 1
                primeiro_elemento = fila_prontos.pop(0)
                if(primeiro_elemento.duracao_variavel != 0):
                    fila_prontos.append(primeiro_elemento)
                else:
                    processos_terminados += 1
                if len(fila_prontos) == 0:
                    break
                fila_processamento.append(fila_prontos[0].id)
                # print(f'{fila_processamento[-1]} no tempo {tempo}')
                
                tempo_processo = 0
            else:    
                fila_prontos[0].duracao_variavel -= 1
                if(fila_prontos[0].duracao_variavel == 0):
                    fila_prontos.pop(0)
                    if len(fila_prontos) == 0:
                        break
                    fila_processamento.append(fila_prontos[0].id)
                    tempo_processo = 0
                    processos_terminados += 1

            

        tempo_processo += 1
        tempo += 1
    print(fila_processamento)
    for processo in fila_prontos:
        print(processo.id)

    return fila_processamento

def calcular_tempos_medios_rr(processos, fila_processamento, quantum):
    tempos_retorno = 0
    tempos_resposta = 0
    tempos_espera = 0

    # Iterar sobre cada processo
    for processo in processos:
        execucoes = math.ceil(processo.duracao / quantum)  # Quantas vezes o processo será executado
        execucoes_contadas = 0  # Contador de execuções
        i = 0

        # Iterar sobre a fila de processamento
        for idx in fila_processamento:
            
            if execucoes_contadas < execucoes :
                if idx == processo.id:
                    execucoes_contadas += 1
                    tempos_retorno+= quantum

                    # Verifica se é a primeira execução (para calcular o tempo de resposta)
                    if execucoes_contadas == 1:
                        print(i*quantum - processo.chegada)
                        tempos_resposta += i * quantum - processo.chegada
                        tempos_retorno -= i * quantum - processo.chegada
                        tempos_espera -= i * quantum - processo.chegada


                    # Se é a última execução, ajuste o tempo de retorno
                    if execucoes_contadas == execucoes:
                        break

                else:
                    tempos_retorno+= quantum
                    tempos_espera += quantum
                    i += 1
            else:
                break

    # Calculando as médias
    print(tempos_resposta)
    media_retorno = tempos_retorno/ len(processos)
    media_resposta = tempos_resposta / len(processos)
    media_espera = tempos_espera / len(processos)

    return media_retorno, media_resposta, media_espera

# Executa a função process_input e passa a lista de processos como parâmetro
processos = process_input('entrada.txt')

fila_processamento = RR(processos, quantum=2)

# Calcular tempos médios
media_retorno_FCFS, media_resposta_FCFS, media_espera_FCFS = FCFS(processos)
media_retorno_rr, media_resposta_rr, media_espera_rr = calcular_tempos_medios_rr(processos, fila_processamento, quantum=2)
# # Calcula os tempos médios usando Round Robin com quantum = 2
# media_retorno, media_resposta, media_espera = calcular_tempos_medios(processos, quantum=2)

# Exibir resultados
print(f"FCFS {media_retorno_FCFS:.1f} {media_resposta_FCFS:.1f} {media_espera_FCFS:.1f}")
print(f"RR {media_retorno_rr:.1f} {media_resposta_rr:.1f} {media_espera_rr:.1f}")

