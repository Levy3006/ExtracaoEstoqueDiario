import pandas as pd
import os
import time
import warnings

# Ignorar avisos de UserWarning do openpyxl 
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Medir o tempo de execução
start_time = time.time()

planilhao = pd.DataFrame()
diaInicial = 5
diaFinal = 26

# Loop para processar os arquivos
for a in range(diaInicial, diaFinal + 1):
    nomePlanilha = f'estoque_202501{str(a).zfill(2)}.xlsx'
    
    if not os.path.exists(nomePlanilha):
        print(f"{nomePlanilha} não encontrado. Pulando...")
        continue
    
    try:
        print(f"Lendo planilha {nomePlanilha}")
        df = pd.read_excel(nomePlanilha)
        df['Data'] = f'{str(a).zfill(2)}/01/2025'  # Adicionando a coluna Data
        print(f"Adicionando campo Data a {nomePlanilha}")
        planilhao = pd.concat([planilhao, df], ignore_index=True)
    except Exception as e:
        print(f"Erro ao processar {nomePlanilha}: {e}")

# Nome do arquivo final em formato CSV
nomePlanilhao = f'planilhão_Dia{diaInicial}ao{diaFinal}.csv'

print("Finalizando planilhão no formato CSV...")
planilhao.to_csv(nomePlanilhao, index=False, sep=';', encoding='utf-8')  # Salvar CSV, se necessário

print(f"====== {nomePlanilhao} finalizado com sucesso! =======")
print(f"Tempo total de execução: {time.time() - start_time:.2f} segundos")
