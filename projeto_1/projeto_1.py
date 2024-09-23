# Rafael de Melo Oliveira - 20200013481
# Virgílio Schettini de Oliveira Neto - 20200013848

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
    id = 1          # Id para cada cada processo

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
    fila_processos = [] #Lista da fila de processos que forão processados
    n = len(processos)
    tempo = 0

    # soma dos tempos 
    tempos_retorno = 0
    tempos_resposta = 0
    tempos_espera = 0

    for processo in processos:
        if len(fila_processos) == 0:
            # Primeiro processo entra direto na fila
            fila_processos.append(processo)
            tempos_retorno += processo.duracao
            tempo += processo.duracao
        else:
            if tempo < processo.chegada:
                # Se o próximo processo chega depois do tempo atual, a CPU vai ficar "esperando"
                tempos_retorno += processo.duracao
                tempo += processo.duracao + processo.chegada - tempo
            else:
                # Calcula o tempo de retorno, resposta e espera
                tempos_retorno += processo.duracao + tempo - processo.chegada
                tempos_resposta += tempo - processo.chegada
                tempos_espera += tempo - processo.chegada
                tempo += processo.duracao

    # Calculando as médias
    media_retorno = tempos_retorno/ n
    media_resposta = tempos_resposta / n
    media_espera = tempos_espera / n

    return media_retorno, media_resposta, media_espera

def SJF(processos):
    processos_terminados = []
    processos_disponiveis = []
    n = len(processos)
    tempo = 0

    tempos_retorno = 0
    tempos_resposta = 0
    tempos_espera = 0

    while len(processos_terminados) != n:
        # Encontrar os processos que já chegaram
        for processo in processos:
            if processo.chegada <= tempo and processo not in processos_disponiveis and processo not in processos_terminados:
                processos_disponiveis.append(processo) 

        # Se não há nenhum processo disponível, avança o tempo
        if not processos_disponiveis:
            tempo += 1
            continue

        # Encontar o próximo processo a ser executado entre os disponíveis
        processo_atual = processos_disponiveis[0]
        for processo in processos_disponiveis:
            if processo.duracao < processo_atual.duracao:
                processo_atual = processo

        tempos_espera += tempo - processo_atual.chegada
        tempos_resposta += tempo - processo_atual.chegada
        tempos_retorno += tempo + processo_atual.duracao - processo_atual.chegada

        tempo += processo_atual.duracao

        
        processos_terminados.append(processo_atual)
        processos_disponiveis.remove(processo_atual)

    media_retorno = tempos_retorno / n
    media_resposta = tempos_resposta / n
    media_espera = tempos_espera / n

    return media_retorno, media_resposta, media_espera

# Função para conseguir a ordem de acontecimento dos processos até acabarem
def RR(processos, quantum):
    fila_prontos = []           # Fila para saber se o tempo do processo ja chegou
    processos_terminados = 0    # Contador de processos finalizados
    n = len(processos)
    fila_processamento = []     # Fila da ordem de acontecimentos
    tempo = 0                   # tempo total
    tempo_processo = 0          # Tempo para usado por cada instância de processo
    processo_parado = False     # Flag para quando não há nenhum processo em sendo processado no momento

    # Lógica funciona até que todos os processos tenham acabado
    while(n != processos_terminados):

        for processo in processos:
            # Verifica se algum processo está pronto para ser executado
            if(tempo == processo.chegada):
                fila_prontos.append(processo)

        # Verifica se há processos prontos para execução
        if len(fila_prontos) != 0:
             # Caso o tempo seja 0
            if tempo == 0:       
                fila_processamento.append(fila_prontos[0].id)
            
            # Se o processo já rodou o tempo do quantum, troca de processo
            elif tempo_processo == quantum:
                fila_prontos[0].duracao_variavel -= 1
                primeiro_elemento = fila_prontos.pop(0)
                if(primeiro_elemento.duracao_variavel > 0):
                    fila_prontos.append(primeiro_elemento) # Coloca o processo de volta na fila se ainda não acabou
                else:
                    primeiro_elemento.duracao_variavel = primeiro_elemento.duracao
                    processos_terminados += 1
                if len(fila_prontos) != 0:
                    fila_processamento.append(fila_prontos[0].id)
                
                # Reseta o tempo do processo
                tempo_processo = 0
            else:    
                if(processo_parado):
                    processo_parado = False
                    fila_processamento.append(fila_prontos[0].id)

                # Atualiza o tempo restante de execução do processo
                fila_prontos[0].duracao_variavel -= 1
                if(fila_prontos[0].duracao_variavel < 0):
                    fila_prontos[0].duracao_variavel = fila_prontos[0].duracao
                    fila_prontos.pop(0)
                    if len(fila_prontos) == 0:
                        break
                    fila_processamento.append(fila_prontos[0].id)
                    tempo_processo = 0
                    processos_terminados += 1

        # Se não há processos prontos, pula o tempo
        if len(fila_prontos) != 0:
            tempo_processo += 1
        else:
            tempo_processo = 1
            processo_parado = True
            fila_processamento.append(-1)
        tempo += 1
        
    return fila_processamento

# Função para calcular os tempos médios baseados na fila de processamento de Round Robin
def calcular_tempos_medios_rr(processos, fila_processamento, quantum):
    n = len(processos)
    tempos_retorno = [0] * n
    tempos_resposta = [0] * n
    tempos_espera = [0] * n
    tempo_processado = 0
    tempo = 0

    for idx in fila_processamento:
        if idx != -1:
            processos[idx - 1].duracao_variavel -= quantum
            if processos[idx - 1].duracao_variavel < 0:
                tempo_processado = processos[idx - 1].duracao_variavel + quantum # Processo acabou antes do quantum
                tempos_retorno[idx - 1] += tempo_processado
            else:
                tempo_processado = quantum
                tempos_retorno[idx - 1] += tempo_processado

            tempo += tempo_processado
        else:
            tempo += 1

        # Atualiza o tempo de espera para todos os outros processos que estão aguardando
        if idx != -1:
            for processo in processos:
                if processo.id != idx and processo.duracao_variavel > 0 and tempo > processo.chegada:
                    tempos_retorno[processo.id - 1] += tempo_processado
                    if processo.duracao == processo.duracao_variavel:
                        tempos_espera[processo.id - 1] = tempo - processo.chegada
                        tempos_resposta[processo.id - 1] = tempo - processo.chegada
                    else:
                        tempos_espera[processo.id - 1] += tempo_processado
    
    # Calcula as médias
    media_retorno = sum(tempos_retorno)/ n
    media_resposta = sum(tempos_resposta) / n
    media_espera = sum(tempos_espera) / n

    return media_retorno, media_resposta, media_espera

# Executa a função process_input e passa a lista de processos como parâmetro
processos = process_input('entrada.txt')

# Calcular tempos médios
media_retorno_FCFS, media_resposta_FCFS, media_espera_FCFS = FCFS(processos)

media_retorno_SJF, media_resposta_SJF, media_espera_SJF = SJF(processos)

fila_processamento = RR(processos, quantum=2)
media_retorno_rr, media_resposta_rr, media_espera_rr = calcular_tempos_medios_rr(processos, fila_processamento, quantum=2)

# Exibir resultados
print(f"FCFS {media_retorno_FCFS:.1f} {media_resposta_FCFS:.1f} {media_espera_FCFS:.1f}")
print(f"SJF {media_retorno_SJF:.1f} {media_resposta_SJF:.1f} {media_espera_SJF:.1f}")
print(f"RR {media_retorno_rr:.1f} {media_resposta_rr:.1f} {media_espera_rr:.1f}")

