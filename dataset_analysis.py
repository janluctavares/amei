import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




data = pd.read_csv(".\habitacao-dataset.txt") #reads file 


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

# Plotting value counts of 'TITULO' column
plt.figure(figsize=(8, 6))
data['TITULO'].value_counts().plot(kind='bar')
plt.title('Distribution of TITULO')
plt.xlabel('TITULO')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Plotting value counts of 'OFERTA' column
plt.figure(figsize=(6, 4))
data['OFERTA'].value_counts().plot(kind='bar')
plt.title('Distribution of OFERTA')
plt.xlabel('OFERTA')
plt.ylabel('Count')
plt.show()

# Summary statistics for 'VALORES' and 'VALORES_PROMO'
print(data[['VALORES', 'VALORES_PROMO']].describe())

# Plotting histogram of 'METRAGEM'
plt.figure(figsize=(8, 6))
plt.hist(data['METRAGEM'], bins=30, edgecolor='k',range=(data['METRAGEM'].quantile(0.015), data['METRAGEM'].quantile(0.95)))
plt.title('Histogram of METRAGEM')
plt.xlabel('METRAGEM')
plt.ylabel('Frequency')
plt.show()

# Plotting histograms of 'QUARTO', 'GARAGEM', and 'BANHEIRO'
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.hist(data['QUARTO'], bins=np.arange(7), edgecolor='k')
plt.title('QUARTO')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Frequency')

plt.subplot(1, 3, 2)
plt.hist(data['GARAGEM'], bins=np.arange(6), edgecolor='k')
plt.title('GARAGEM')
plt.xlabel('Number of Garages')
plt.ylabel('Frequency')

plt.subplot(1, 3, 3)
plt.hist(data['BANHEIRO'], bins=np.arange(6), edgecolor='k')
plt.title('BANHEIRO')
plt.xlabel('Number of Bathrooms')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

