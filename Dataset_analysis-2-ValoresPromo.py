# -*- coding: utf-8 -*-
"""
Created on Fri Aug 03 17:59:50 2023

Este programa gera os gráficos básicos dos arquivos do dataset.

@author: Jan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from preproc import le_arquivos, extract_integer_from_string


def filtra_apartamento(s):
    if not isinstance(s, str):
        s = "nulo"
    if 'APARTAMENTO' in s or "FLAT" in s:
        s = 'APARTAMENTO'
    elif "CASA" in s:
        s="CASA"
    elif "LOTE" in s:
        s="LOTE"
    elif "SALA" in s or "LOJA" in s:
        s="SALA"
    elif "CHACARA" in s:
        s="CHACARA"
    elif "PAVILHAO" in s:
        s = "PAVILHAO"
    elif "COBERTURA" in s:
        s = "COBERTURA"
    elif "KITNET" in s:
        s = "KITNET"
    elif "BOX" in s:
        s = "BOX"
    return s


tipoCategoria = "AR"
interesse = "VALORES_PROMO"


codigo_to_tipo_categoria = {
    'AC': ('Aluguel', 'Comerciais'),
    'AR': ('Aluguel', 'Residenciais'),
    'CC': ('Compra', 'Comerciais'),
    'CR': ('Compra', 'Residenciais')
}
tipo = codigo_to_tipo_categoria[tipoCategoria][0]
categoria = codigo_to_tipo_categoria[tipoCategoria][1]

data = le_arquivos("casa")
data = data.loc()[tipoCategoria]

# Garante que as colunas VALORES  e VALORES_PROMO são inteiros. Também, simplifica alguns tipos de imovel.
data['VALORES'] = data['VALORES'].apply(extract_integer_from_string)
data['VALORES_PROMO'] = data['VALORES_PROMO'].apply(extract_integer_from_string)
data['TIPO'] = data['TIPO'].apply(filtra_apartamento)



# Fazendo os gráficos relacionando Valores_promo com outras variáveis:

plt.rcParams.update({
    'font.size': 16,        # Main text font size
    'axes.titlesize': 22,   # Title font size
    'axes.labelsize': 24,   # Axes labels font size
    'xtick.labelsize': 14,  # X-axis tick labels font size
    'ytick.labelsize': 26   # Y-axis tick labels font size
})

fig = plt.figure(figsize=(16, 32))
gs = gridspec.GridSpec(4, 2, figure=fig)

# Título geral
fig.suptitle('{} de imóveis {}'.format(tipo, categoria), fontsize=40)


# Plotting the boxplot for 'VALORES_PROMO' grouped by 'TIPO' with outliers
ax1 = fig.add_subplot(gs[0, 0])
titulo_counts = data['TIPO'].value_counts().sort_values(ascending=False)
sns.boxplot(x='TIPO', y=interesse , data=data, order=titulo_counts.index, ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
ax1.set_xlabel('Tipo')
ax1.set_ylabel(interesse+ "(R$)")
ax1.set_title('{} para cada tipo'.format(interesse))

# Plotting the boxplot for 'VALORES_PROMO' grouped by 'TIPO' without outliers
ax2 = fig.add_subplot(gs[0, 1])
sns.boxplot(x='TIPO', y=interesse, data=data, order=titulo_counts.index, ax=ax2, showfliers=False)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
ax2.set_xlabel('Tipo')
ax2.set_ylabel(interesse+"(R$)")
ax2.set_title('{} X tipo (sem outliers)'.format(interesse))

# Plotting the boxplot for 'VALORES_PROMO' grouped by 'LOCATION' ordered by counts
ax3 = fig.add_subplot(gs[1, 0])
location_counts = data['LOCATION'].value_counts().sort_values(ascending=False)
top_locations = location_counts.head(20).index
top_data = data[data['LOCATION'].isin(top_locations)]

sns.boxplot(x='LOCATION', y=interesse, data=top_data, order=location_counts.index[:19], ax=ax3, showfliers=False)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)
ax3.set_xlabel('Bairro')
ax3.set_ylabel(interesse +"(R$)")
ax3.set_title('{} - top20 bairros (so)'.format(interesse))

# Plotting the boxplot for the top 20 neighborhoods by counts and mean 'VALORES_PROMO'

location_order_by_mean = top_data.groupby('LOCATION')[interesse].mean().sort_values().index
ax4 = fig.add_subplot(gs[1, 1])
sns.boxplot(x='LOCATION', y=interesse, data=top_data, order=location_order_by_mean, ax=ax4, showfliers=False)
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=90)
ax4.set_xlabel('Bairro')
ax4.set_ylabel(interesse+"(R$)")
ax4.set_title('{} top20 por média'.format(interesse))

# Creating the scatter plot for 'AREA' versus 'interesse' (restricted to top 95%)
ax5 = fig.add_subplot(gs[2, :])
sorted_data = data[['AREA', interesse]].sort_values(by='AREA')
top_percent_area = int(sorted_data.shape[0] * 0.99)
top_percent_interesse = np.percentile(sorted_data[interesse], 99)  # Calculate the 95th percentile of 'interesse'

filtered_data = sorted_data[(sorted_data['AREA'] <= sorted_data.iloc[top_percent_area - 1]['AREA']) &
                            (sorted_data[interesse] <= top_percent_interesse)]

sns.scatterplot(x='AREA', y=interesse, data=filtered_data, ax=ax5)
ax5.set_xlabel('Área (m2)')
ax5.set_ylabel(interesse+"(R$)")
ax5.set_title('Área versus {} (Top 99% cada)'.format(interesse))


# Adjust layout
fig.tight_layout()
plt.subplots_adjust(top=0.93)  # Espaço extra para o título geral

#plt.savefig("./Imagens/{}_{}_{}.png".format(interesse, tipo, categoria))
plt.show()






