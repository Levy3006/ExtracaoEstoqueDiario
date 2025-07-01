
Script python para obter fotos diárias dos valores de estoque . O script consiste em se conectar com o DB da empresa, fazer a consulta que retorna o valores de estoque, e após isso, subir essa tabela em outro DB, para que ao final do mes, gerar um planilhão e fazer uma análise detalhada dos estoques diários.

Aqui está o que o script principal Extrair_e_carregar.py faz:

1 - Conexão com o banco de dados via python ultilizando SQLAlchemy
2 - Fazer a consulta ultilizando pandas
3 - Tratamento básico para reorganizar colunas e salvar o arquivo em excel com a data do dia
4 - Subir o daataframe como tabela para outro banco de dados.
