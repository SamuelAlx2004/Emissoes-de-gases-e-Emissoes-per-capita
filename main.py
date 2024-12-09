import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Ler o arquivo com ajuste de linhas ignoradas (se necessário)
emissoes_gases = pd.read_excel('1-SEEG10_GERAL-BR_UF_2022.10.27-FINAL-SITE.xlsx', sheet_name = 'GEE Estados')


emissoes_gases = emissoes_gases[emissoes_gases['Emissão / Remoção / Bunker'] == 'Emissão']
emissoes_gases = emissoes_gases.drop(columns = 'Emissão / Remoção / Bunker')

#Chegou o momento de praticar! Vamos aplicar os conceitos aprendidos durante a aula a partir de
#algumas atividades. Solucione os problemas propostos através de códigos utilizando a base de dados
#disponibilizada no curso.

#Encontre os valores únicos das colunas "Nível 1 - Setor" e "Estado" para identificar as atividades
#econômicas presentes na base de dados e se todos os Estados do Brasil estão presentes no DataFrame.

emissoes_gases["Estado"].unique(),emissoes_gases['Nível 1 - Setor'].unique()

#Filtre o DataFrame somente com os dados dos Estados da região Sul do Brasil.

emissoes_gases.loc[emissoes_gases['Estado'].isin(['PR', 'SC', 'RS'])]

#Filtre o DataFrame para exibir apenas os registros em que o campo "Nível 1 - Setor" seja igual a
#"Mudança de Uso da Terra e Floresta" e o campo "Estado" seja igual a "AM" (sigla para o Estado do Amazonas).

emissoes_gases_AM = emissoes_gases.query('Estado == "AM"')
emissoes_gases_AM = emissoes_gases_AM.query('`Nível 1 - Setor` == "Mudança de Uso da Terra e Floresta"')


#Encontre o valor máximo de emissão do ano de 2021 para os dados de "Agropecuária" no Estado do Pará.

emissoes_gases_PA = emissoes_gases.query('Estado == "PA"')
emissoes_gases_PA = emissoes_gases_PA.query('`Nível 1 - Setor` == "Agropecuária"')
emissoes_gases_PA[2021].max()

#Mesma resposta com loc

emissoes_gases.loc[(emissoes_gases['Nível 1 - Setor'] == 'Agropecuária') & (emissoes_gases['Estado'] == 'PA'), 2021].max()

#Remodelando o DataFrame

colunas_info = list(emissoes_gases.loc[:,'Nível 1 - Setor':'Produto'])

colunas_emissao = list(emissoes_gases.loc[:,1970:2021].columns)

emissoes_por_ano = emissoes_gases.melt(id_vars = colunas_info, value_vars = colunas_emissao, var_name='Ano', value_name = 'Emissão')

#Groupyby,groups e get_group

emissoes_por_ano.groupby('Gás')
emissoes_gases.groupby('Gás').groups
emissoes_por_ano.groupby('Gás').get_group('CO2 (t)')

#analise dos gases

emissao_por_gas = emissoes_por_ano.groupby('Gás')[['Emissão']].sum().sort_values('Emissão', ascending = False)

emissao_por_gas.plot(kind='barh', figsize=(10, 6))

#print(f'A emissão de CO2 corresponde a {float((emissao_por_gas.iloc[0:9].sum()/emissao_por_gas.sum()).iloc[0])*100:.2f} % de emissão total de gases estufa no Brasil de 1970 a 2021.')

#1) Faça um agrupamento de dados com base na coluna "Nível 1 - Setor" para visualizar o dicionário
#contendo as chaves de grupos formados e a lista de índices de cada grupo.

emissoes_por_ano.groupby('Nível 1 - Setor').groups

#2) Faça um agrupamento de dados com base na coluna "Nível 1 - Setor" e localize os dados do grupo "Agropecuária".

emissoes_por_ano.groupby('Nível 1 - Setor').get_group("Agropecuária")

#3) Faça um agrupamento de dados com base na coluna "Nível 1 - Setor" para identificar a média de emissão de cada atividade econômica no ano de 2021.

emissoes_por_ano[emissoes_por_ano['Ano'] == 2021].groupby('Nível 1 - Setor')[['Emissão']].mean()

#4) Faça um agrupamento de dados com base na coluna "Nível 1 - Setor" para identificar a soma de emissão de cada atividade econômica. Ordene os dados da maior para menor emissão.

emissoes_por_ano.groupby('Nível 1 - Setor')[['Emissão']].sum().sort_values('Emissão', ascending= False)

# Agrupando multi-index

gas_por_setor = emissoes_por_ano.groupby(['Gás', 'Nível 1 - Setor'])[['Emissão']].sum()

gas_por_setor.xs('CO2 (t)', level=0)

gas_por_setor.xs(('CO2 (t)', 'Mudança de Uso da Terra e Floresta'), level = [0,1])

gas_por_setor.xs('CO2 (t)', level=0).max()

gas_por_setor.xs('CO2 (t)', level=0).idxmax()


valores_max = gas_por_setor.groupby(level = 0).max().values
tabela_sumarizada = gas_por_setor.groupby(level = 0).idxmax()
tabela_sumarizada.insert(1, 'Quantidade de emissão',valores_max)
gas_por_setor.swaplevel(0,1).groupby(level= 0).idxmax()

#Emissões por ano

emissoes_por_ano.groupby('Ano')[['Emissão']].mean().plot(figsize=(10,6))

emissoes_por_ano.groupby('Ano')[['Emissão']].mean().idxmax()

emissoes_por_ano.groupby(['Ano', 'Gás'])[['Emissão']].mean()

media_emissao_anual = emissoes_por_ano.groupby(['Ano', 'Gás'])[['Emissão']].mean().reset_index()

media_emissao_anual = media_emissao_anual.pivot_table(index='Ano', columns='Gás', values='Emissão')

media_emissao_anual.plot(subplots = True, figsize = (10, 40))

emissao_setores = emissoes_por_ano.pivot_table(values = 'Emissão', index = 'Ano', columns = 'Nível 1 - Setor', aggfunc = 'mean')


# 1) Faça um agrupamento de dados com as colunas "Estado" e "Nível 1 - Setor", obtendo a soma de emissão e armazenando o resultado em uma tabela.

emissoes_estados_setor = emissoes_por_ano.groupby(["Estado","Nível 1 - Setor"])[['Emissão']].sum()

# 2) Utilizando a tabela construída na atividade 1, selecione os dados referentes à "Energia" do índice "Nível 1 - Setor".

emissoes_estados_setor.xs('Energia', level= 1)

# 3) Utilizando a tabela construída na atividade 1, encontre a atividade econômica com valor máximo de emissão do Estado de Minas Gerais

emissoes_estados_setor.xs('MG', level=0).idxmax()

# 4) Obtenha uma tabela contendo a atividade econômica com máxima emissão para cada Estado.

emissoes_estados_setor.groupby(level = 0).idxmax()

# 5) Para conseguir o índice do Estado com emissão máxima para cada atividade econômica, devemos fazer um novo agrupamento de dados a partir do índice,
#indicando qual nível hierárquico e usando o método idxmax():

emissoes_estados_setor.groupby(level = 1).idxmax()

# Carrega o arquivo Excel, ignorando o rodapé desnecessário
populacao_estados = pd.read_excel('POP2022_Municipios.xls', header=1, skipfooter=34)

# Remove informações entre parênteses e pontos de separação de milhar
populacao_estados = populacao_estados.assign(
    populacao_sem_parenteses = populacao_estados['POPULAÇÃO'].replace('\(\d{1,2}\)', '', regex=True),
    populacao = lambda x: x['populacao_sem_parenteses'].replace('\.', '', regex=True)
)

# Converte a coluna 'populacao' para tipo inteiro
populacao_estados = populacao_estados.astype({'populacao': 'int64'})

# Agrupa por estado (UF) e soma as populações
populacao_estados.groupby('UF').sum(numeric_only=True).reset_index()

#Unindo Dataframes

emissao_estados = emissoes_por_ano[emissoes_por_ano['Ano'] == 2021].groupby('Estado')[['Emissão']].sum().reset_index()

dados_agrupados = pd.merge(emissao_estados, populacao_estados, left_on = 'Estado', right_on = 'UF')

dados_agrupados.plot(x = 'populacao', y= 'Emissão', kind = 'scatter', figsize=(8,6))

#Emissoes per capita

#px.scatter(data_frame = dados_agrupados, x = 'populacao', y = 'Emissão', text = 'Estado', opacity = 0)

dados_agrupados = dados_agrupados.assign(emissao_per_capita = dados_agrupados['Emissão']/dados_agrupados['populacao']).sort_values('emissao_per_capita', ascending = False)

px.scatter(data_frame = dados_agrupados, x = 'populacao', y = 'Emissão', text = 'Estado', size = 'emissao_per_capita')

