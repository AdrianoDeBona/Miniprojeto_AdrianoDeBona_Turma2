
# Importar as bibliotecas

import pandas as pd

import numpy as np

from datetime import datetime

# SCRIPT DE LIMPEZA DE DADOS
# Objetivo: Realizar a limpeza e padronização dos dados para análise

# Definindo o caminho do arquivo Excel

caminho = r"C:\Users\Cliente Especial\Aula_DADOS\Miniprojeto_AdrianoDeBona_Turma2\dados\Base_Varejo.csv"

# Lendo o arquivo Excel e armazenando em um DataFrame

df = pd.read_csv(caminho, sep=';')

# Exibindo o número de linhas do DataFrame antes da limpeza

linhas = len(df)

print(f"O número de linhas no DataFrame é: {linhas}")

print(df.head())  # Exibe as primeiras linhas do DataFrame

# Removendo colunas desnecessárias (colunas 'Unnamed: 10' a 'Unnamed: 13')

df.drop('Unnamed: 10', axis=1, inplace=True)
df.drop('Unnamed: 11', axis=1, inplace=True)
df.drop('Unnamed: 12', axis=1, inplace=True)
df.drop('Unnamed: 13', axis=1, inplace=True)

# Verificando e removendo linhas com valores nulos

df = df.dropna(how='all')  # Remove linhas onde todas as colunas são nulas

print(df.info()) # Exibe informações sobre o DataFrame, como tipos de dados e valores nulos
print(df.dtypes)  # Exibe os tipos de dados de cada coluna
print(df.columns)  # Exibe as colunas do DataFrame
print(df.shape)  # Exibe o número de linhas e colunas do DataFrame

# Convertendo a coluna 'DATA' para o tipo datetime e tratando erros de conversão

df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce') 
print(df)

# Convertendo as colunas de texto para o tipo string e substituindo 'NaN' por NaN real

coluna_texto = ['CO_ID','CL_ID', 'CL_EC', 'PR_ID','PR_CAT', 'PR_NOME']
for col in coluna_texto:
    df[col] = df[col].astype('str')  # Converte para string
    df[col] = df[col].replace('NaN', np.nan) # Substitui 'NaN' por NaN real

# Verificando os valores únicos nas colunas de texto para identificar possíveis inconsistências

print(df['DATA'].unique())
print(df['CO_ID'].unique())
print(df['CL_GENERO'].unique())
print(df['CL_EC'].unique())
print(df['CL_SEG'].unique())
print(df['PR_CAT'].unique())

# Verificadas inconsistências na coluna 8

print(df.loc[df['PR_CAT'] == '#N/D']) # Exibe as linhas onde a coluna 'PR_CAT' tem o valor '#N/D'

# Verifiquei inconsistências na coluna 9 também.
# Verifiquei que existem 3650 linhas com o valor '#N/D' na coluna 'PR_CAT' e 'PR_NOME', 
# o que indica se tratar do mesmo produto.
# Após verificar isso optei por mante-lo na base para garantir a integridade dos dados. 
# Substitui os valores por "Sem Categoria" para possibilitar análises futuras.

def substituir_nulos(cat):
    if cat == '#N/D':
        return 'Sem Categoria'
    else:
        return cat

df['PR_CAT'] = df['PR_CAT'].apply(substituir_nulos)
df['PR_NOME'] = df['PR_NOME'].apply(substituir_nulos)

print(df.info())  # Exibe informações sobre o DataFrame, como tipos de dados e valores nulos
print(df.describe())  # Exibe estatísticas descritivas para colunas numéricas
print(df)

# Calculando  a coluna CL_FHL.
media = df['CL_FHL'].mean() # Calcula a média da coluna 'CL_FHL' e armazena na variável 'media'
mediana = df['CL_FHL'].median() # Calcula a mediana da coluna 'CL_FHL' e armazena na variável 'mediana'
desvio_padrao = df['CL_FHL'].std() # Calcula o desvio padrão da coluna 'CL_FHL' e armazena na variável 'desvio_padrao'
moda = df['CL_FHL'].mode()[0]  # Obtém a moda (valor mais frequente) da coluna 'CL_FHL'
maximo = df['CL_FHL'].max() # Calcula o valor máximo da coluna 'CL_FHL' e armazena na variável 'maximo'
minimo = df['CL_FHL'].min() # Calcula o valor mínimo da coluna 'CL_FHL' e armazena na variável 'minimo'
contagem = df['CL_FHL'].count() # Conta o número de valores não nulos na coluna 'CL_FHL' e armazena na variável 'contagem'

print(f"Média: {media}")
print(f"Mediana: {mediana}")
print(f"Desvio Padrão: {desvio_padrao}")
print(f"Moda: {moda}")
print(f"Máximo: {maximo}")
print(f"Mínimo: {minimo}")
print(f"Contagem: {contagem}")

print(df.groupby('CL_GENERO')['CL_FHL'].size())  # Exibe a contagem de filhos de clientes por gênero
print(df.groupby('CL_GENERO')['PR_NOME'].size())  # Exibe a contagem de produtos por gênero
print(df.pivot_table(index='CL_GENERO', columns='PR_CAT', values='PR_NOME', aggfunc='count', fill_value=0))

print(df)

print("=" *50)
print("RELATÓRIO")
print("=" *50)
print(f"Número de linhas no DataFrame: {linhas}")
print(f"Número de linhas após a limpeza: {len(df)}")
print(f"Número de colunas no DataFrame: {len(df.columns)}")
print("=" *50)
print("Número de filhos dos clientes:")
print(f"Média: {media}")
print(f"Mediana: {mediana}")
print(f"Desvio Padrão: {desvio_padrao}")
print(f"Moda: {moda}")
print(f"Máximo: {maximo}")
print(f"Mínimo: {minimo}")
print("=" *50)
print("Contagem de produtos por gênero:")
print(df.groupby('CL_GENERO')['PR_NOME'].size())
print("=" *50)
print("Contagem de produtos por categoria e gênero:")
print(df.pivot_table(index='CL_GENERO', columns='PR_CAT', values='PR_NOME', aggfunc='count', fill_value=0))
print("=" *50)

pasta_clean = r"C:\Users\Cliente Especial\Aula_DADOS\Miniprojeto_AdrianoDeBona_Turma2\dados\Base_Varejo_Clean.csv"
df.to_csv(pasta_clean, index=False, sep=';')

