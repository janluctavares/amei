import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv(".\Dataset_AP_Comprar.txt") #reads file 

data.head()
data.keys()

print("# Características Gerais do Dataset")

print("O conjunto de dados possui {} linhas e {} colunas".format(data.shape[0], data.shape[1]))

data.info()

print("Exemplos de entradas:")
for key in data.keys():
    print("Coluna ", key)
    print(data[key].head())

print(data.VALORES.head())

# Valores e Valores_promo deveriam ser int

# Function to extract integers from strings
def extract_integer_from_string(s):
    try:
        a = int(''.join(filter(str.isdigit, str(s))))
    except:
        a = -1
    return a

def filtra_apartamento(s):
    if not isinstance(s, str):
        s = "nulo"
    if 'Apartamento' in s or "Flat" in s:
        s = 'Apartamento'
    elif "Casa" in s:
        s="Casa"
    elif "Sala" in s or "Loja" in s or "Comercial" in s:
        s="Sala"
    elif "Chácara" in s:
        s="Chácara"
    elif "Pavilhão" in s:
        s = "Pavilhão"
    elif "Cobertura" in s:
        s = "Cobertura"
    return s



# Extract integers from 'VALORES' and 'VALORES_PROMO' columns
data['VALORES'] = data['VALORES'].apply(extract_integer_from_string)
data['VALORES_PROMO'] = data['VALORES_PROMO'].apply(extract_integer_from_string)
data['TITULO'] = data['TITULO'].apply(filtra_apartamento)

resto = data[data["TITULO"]!="Apartamento"]
resto = resto[resto["TITULO"]!="Casa"]
resto = resto[resto["TITULO"]!="Sala"]
print(resto)

# Plotando contagens por titulo
plt.figure(figsize=(8, 6))
data['TITULO'].value_counts().plot(kind='bar')
plt.title('Distribuição de tipos de imóvel')
plt.xlabel('TITULO')
plt.ylabel('Contagem')
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(6, 4))
data['OFERTA'].value_counts().plot(kind='bar')
plt.title('Tipos de OFERTA')
plt.xlabel('OFERTA')
plt.ylabel('Contagem')
plt.show()

# Resumo de estatísticas de Valores e Valores Promo
pd.options.display.float_format = '{:,.0f}'.format
print(data[['VALORES', 'VALORES_PROMO']].describe())

'''

# DEMORA DEMAIS PRA EXECUTAR
# Ordenar 'VALORES' e 'VALORES_PROMO'
sorted_data = data[['VALORES', 'VALORES_PROMO']].sort_values(by=['VALORES', 'VALORES_PROMO'])

sorted_data = sorted_data.iloc[0:1000]

# Plot de 'VALORES' e 'VALORES_PROMO'
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.bar(np.arange(len(sorted_data)), sorted_data['VALORES'], align='center', alpha=0.7)
plt.xticks(np.arange(len(sorted_data)), sorted_data.index, rotation=45)
plt.xlabel('Índice')
plt.ylabel('VALORES')
plt.title('VALORES ordenados')

plt.subplot(1, 2, 2)
plt.bar(np.arange(len(sorted_data)), sorted_data['VALORES_PROMO'], align='center', alpha=0.7)
plt.xticks(np.arange(len(sorted_data)), sorted_data.index, rotation=45)
plt.xlabel('Índice')
plt.ylabel('VALORES_PROMO')
plt.title('VALORES_PROMO ordenados')

plt.tight_layout()
plt.show()
'''

# Histograma de 'METRAGEM'
plt.figure(figsize=(8, 6))
plt.hist(data['METRAGEM'], bins=30, edgecolor='k',range=(data['METRAGEM'].quantile(0.015), data['METRAGEM'].quantile(0.95)))
plt.title('Histogramas das "metragens"')
plt.xlabel('METRAGEM')
plt.ylabel('Frequência')
plt.show()

# Histogramas de 'QUARTO', 'GARAGEM' e 'BANHEIRO'
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.hist(data['QUARTO'], bins=np.arange(7)-0.5, edgecolor='k')
plt.title('QUARTO')
plt.xlabel('Número de Quartos')
plt.ylabel('Frequência')

plt.subplot(1, 3, 2)
plt.hist(data['GARAGEM'], bins=np.arange(6)-0.5, edgecolor='k')
plt.title('GARAGEM')
plt.xlabel('Número de garagens')
plt.ylabel('Frequência')

plt.subplot(1, 3, 3)
plt.hist(data['BANHEIRO'], bins=np.arange(6)-0.5, edgecolor='k')
plt.title('BANHEIRO')
plt.xlabel('Número de Banheiros')
plt.ylabel('Frequência')

plt.tight_layout()
plt.show()