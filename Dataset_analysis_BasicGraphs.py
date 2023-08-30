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


tipoCategoria = "CC"

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



# Fazendo os gráficos básicos:

plt.rcParams.update({
    'font.size': 16,        # Main text font size
    'axes.titlesize': 28,   # Title font size
    'axes.labelsize': 30,   # Axes labels font size
    'xtick.labelsize': 22,  # X-axis tick labels font size
    'ytick.labelsize': 26   # Y-axis tick labels font size
})

fig = plt.figure(figsize=(20, 32))
gs = gridspec.GridSpec(4, 2, figure=fig)

# Título geral
fig.suptitle('{} de imóveis {}'.format(tipo, categoria), fontsize=40)

# Plotando contagens por tipo de imóvel
ax0 = fig.add_subplot(gs[0, :])  # Primeira linha, todas as colunas
data['TIPO'].value_counts().plot(kind='bar', ax=ax0)
ax0.set_title('Distribuição de tipos de imóvel')
ax0.set_xlabel('TIPO')
ax0.set_ylabel('Contagem')
ax0.set_xticklabels(ax0.get_xticklabels(), rotation=45)

# Histograma de 'METRAGEM'
ax1 = fig.add_subplot(gs[1, 0])  # Segunda linha, primeira coluna
ax1.hist(data['AREA'], bins=30, edgecolor='k', range=(data['AREA'].quantile(0.00), data['AREA'].quantile(0.90)))
ax1.set_title('Área Construída')
ax1.set_xlabel('Área (m²)')
ax1.set_ylabel('Frequência')

# Histogramas de 'QUARTO', 'BANHEIRO' e 'GARAGEM'
ax2 = fig.add_subplot(gs[1, 1])  # Segunda linha, segunda coluna
ax2.hist(data['QUARTO'], bins=np.arange(7)-0.5, edgecolor='k')
ax2.set_title('Número de Quartos')
ax2.set_xlabel('Número de Quartos')
ax2.set_ylabel('Frequência')

ax3 = fig.add_subplot(gs[2, 0])  # Terceira linha, primeira coluna
ax3.hist(data['BANHEIRO'], bins=np.arange(6)-0.5, edgecolor='k')
ax3.set_title('Número de Banheiros')
ax3.set_xlabel('Número de Banheiros')
ax3.set_ylabel('Frequência')

ax4 = fig.add_subplot(gs[2, 1])  # Terceira linha, segunda coluna
ax4.hist(data['GARAGEM'], bins=np.arange(6)-0.5, edgecolor='k')
ax4.set_title('Número de Vagas de Estacionamento')
ax4.set_xlabel('Número de vagas')
ax4.set_ylabel('Frequência')

# Ajustar layout
fig.tight_layout()
plt.subplots_adjust(top=0.9)  # Espaço extra para o título geral

plt.show()






