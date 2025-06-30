from sqlalchemy import create_engine
import pandas as pd
import time
from datetime import date
from credenciais import db_config

inicio = time.time()
#Configurações banco de dados

# Estabelecendo a conexão com o banco de dados
db_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
engine = create_engine(db_url)
print("Conexão com o banco de dados estabelecida com sucesso!")

with open("consulta.sql", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
    
# Consulta SQL
sql_query = str(conteudo)

try:
    # Executando a consulta e exportando para um DataFrame
    print("executando consulta...")
    df = pd.read_sql_query(sql_query, engine)
    print("=== Consulta Finalizada ===")
    
    # reordenando colunas da tabela
    nova_ordem = [
    "FILIAL SB", "Produtoid", "Status", "Codigo Produto", "Embalagemid", "Codbarras",
    "Descricao", "Grupo Principal", "Nome", "Customedio", "Curvavalor",
    "Curvaquantidade", "VALOR ESTOQUE", "Estoque", "QTDE ESTOQUE", "Precovenda"
    ]
    print("Ajustando DataFrame ...")
    # Reorganizar as colunas
    df = df[nova_ordem]

    print("exportando Dataframe para excel...")

    # Nome do arquivo Excel
    data = str(date.today()).translate({ord('-'): None})
    nome_excel = f"estoque_{data}.xlsx"
    
    df.to_excel(nome_excel, index=False, engine="openpyxl")
    print("==== arquivo exportado com sucesso ==== ")

except Exception as e:
    print(f"Erro: {e}")

fim = time.time()
tempo_total = fim - inicio
print(f" Tempo: {tempo_total:.2f} segundos")

#====== SUBINDO OS ARQUIVOS EM OUTRO BANCO DE DADOS =====================
#========================================================================

inicio = time.time()
#conectando ao banco 'automatizacao_sql'
db_config = {
    'username': 'LeviUser',
    'password': 'levi123',
    'host': '127.0.0.1',  
    'port': '5432',
    'database': 'automatizacao_sql' 
}

db_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
engine = create_engine(db_url)

print("Conexão estabelecida com sucesso! (automatizacao_sql)")
print("Importando tabela...")

# Importar o DataFrame para o PostgreSQL
nome_tabela = nome_excel.split(".")[0]
df.to_sql(nome_excel, engine, if_exists='replace', index=False)

print(f"Tabela '{nome_excel}' importada com sucesso!")
fim = time.time()
print(f"Temp: {tempo_total:.2f} segundos")