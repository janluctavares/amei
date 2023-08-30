# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 13:19:56 2023

@author: Jan

Este programa:
    * garante que valores e valores_promo são inteiros
    * Corta os outliers de valores e valores_promo utilizando o critério de intervalo_interquartil*1.5

"""


import pandas as pd

def le_arquivos(local):
    arqs = ["Dataset_AP_Alugar_Comercial.txt", "Dataset_AP_Comprar_Comercial.txt", "Dataset_AP_Alugar_Residencial.txt", "Dataset_AP_Comprar_Residencial.txt"]
    dataset = []
 
    if local=="casa":
        for arq in arqs:
            url="G:\Meu Drive\Computação - Mestrado\Machine Learning\Trabalho ML\{}".format(arq)
            dataset.append(pd.read_csv(url))
        dataset = pd.concat(dataset, keys=["AC", "CC", "AR", "CR"]) # c/a c/r de comprar/alugar e comercial/residencial
    elif local == "setor":
        for arq in arqs:
            url="/media/eletronica/Arquivos/Jan/Mestrado/Machine Learning/Trabalho ML/{}".format(arq)
            dataset.append(pd.read_csv(url))
        dataset = pd.concat(dataset, keys=["AC", "CC", "AR", "CR"]) # c/a c/r de comprar/alugar e comercial/residencial
    else:
        for arq in arqs:
            url= "{}/{}".format(local, arq)
            dataset.append(pd.read_csv(url))
        dataset = pd.concat(dataset, keys=["AC", "CC", "AR", "CR"]) # c/a c/r de comprar/alugar e comercial/residencial
        
    return dataset

def extract_integer_from_string(s):
    try:
        a = int(''.join(filter(str.isdigit, str(s))))
    except:
        a = -1
    return a

def filtra_apartamento_AR(s):
    if not isinstance(s, str):
        s = "nulo"
    if 'APARTAMENTO' in s or "FLAT" in s:
        s = 'APARTAMENTO'
    elif "CASA EM CONDOMINIO" in s:
        s= 'CASA EM CONDOMINIO'
    elif "CASA" in s or "SOBRADO" in s:
        s="CASA"
    elif "CHACARA" in s:
        s="CHACARA"
    elif "PAVILHAO" in s:
        s = "PAVILHAO"
    elif "COBERTURA" in s:
        s = "COBERTURA"
    return s

def filtra_apartamento_CR(s):
    if not isinstance(s, str):
        s = "nulo"
    if 'GARDEN' in s:
        s = "APARTAMENTO GARDEN"
    elif "COBERTURA" in s:
        s = "COBERTURA"
    elif "LOFT" in s:
        s = "LOFT"
    elif 'APARTAMENTO' in s or "FLAT" in s:
        s = 'APARTAMENTO'
    elif "CHACARA" in s:
        s="CHACARA"
    elif "PAVILHAO" in s:
        s = "PAVILHAO"
    elif "BOX" in s or "GARAGEM" in s or "ESTACIONAMENTO" in s:
        s = "BOX"

    return s

def filtra_apartamento_AC(s):
    if not isinstance(s, str):
        s = "nulo"
    if 'CASA' in s:
        s = "CASA COMERCIAL"
    elif "PAVILHAO" in s:
        s = "PAVILHAO"

    return s


def filtra_apartamento_CC(s):
    if not isinstance(s, str):
        s = "nulo"
    if 'SOBRADO' in s:
        s = "CASA COMERCIAL"
    elif "PAVILHAO" in s:
        s = "PAVILHAO"
    elif "KITNET" in s or "COBERTURA" in s:
        s = 'APARTAMENTO'
    elif "BOX" in s or "GARAGEM" in s or "ESTACIONAMENTO" in s:
        s = "BOX"
    
    return s


codigo_to_tipo_categoria = {
    'AC': ('Aluguel', 'Comerciais'),
    'AR': ('Aluguel', 'Residenciais'),
    'CC': ('Compra', 'Comerciais'),
    'CR': ('Compra', 'Residenciais')
}

local = "/media/eletronica/Arquivos/Jan/Mestrado/Machine Learning/Trabalho ML" # Insira seu diretorio de trabalho
tipoCategoria = "CR" # Informe o codigo correspondente ao tipo e categoria de seu interesse.
'''
Q1_m2 = data['AREA'].quantile(0.25)
Q3_m2 = data['AREA'].quantile(0.75)
IQR_m2 = Q3_m2 - Q1_m2
'''



for tipoCategoria in codigo_to_tipo_categoria.keys():
    tipo = codigo_to_tipo_categoria[tipoCategoria][0]
    categoria = codigo_to_tipo_categoria[tipoCategoria][1]
    
    data = le_arquivos(local)
    data = data.loc()[tipoCategoria]
    tamanho_dataset = len(data)
    

    
    if tipoCategoria == "AR":
        data['TIPO'] = data['TIPO'].apply(filtra_apartamento_AR)
        mantem_tipos= ["APARTAMENTO",
                        "CASA EM CONDOMINIO",
                        "CASA",
                        "COBERTURA",
                        "KITNET/JK",
                        "LOFT",
                        "OUTROS"]
        
    if tipoCategoria == "CR":
        data['TIPO'] = data['TIPO'].apply(filtra_apartamento_CR)
        #remove_tipos = ["PAVILHAO", "CHACARA", "PREDIO", "LOJA", "BOX", "CASA COMERCIAL", "IMOVEL COMERCIAL", "AREA", "ESTACIONAMENTO"]  # Lista das entradas que você deseja remover
        #data = data[~data['TIPO'].isin(remove_tipos)]
        mantem_tipos = ["COBERTURA",
                        "APARTAMENTO",
                        "KITNET/JK",
                        "CASA",
                        "LOTE/TERRENO",
                        "CASA EM CONDOMINIO",
                        "APARTAMENTO GARDEN",
                        "SOBRADO",
                        "LOFT",
                        "SALA/CONJUNTO COMERCIAL",
                        "OUTROS"]
        
    
    if tipoCategoria == "AC":
        data['TIPO'] = data['TIPO'].apply(filtra_apartamento_AC)
        mantem_tipos = [
                        "LOJA",
                        "SALA/CONJUNTO COMERCIAL",
                        "CASA COMERCIAL",
                        "PAVILHAO",
                        "PREDIO",
                        "ANDAR",
                        "LOTE/TERRENO",
                        "OUTROS"]
    if tipoCategoria == "CC":
        data['TIPO'] = data['TIPO'].apply(filtra_apartamento_CC)
        mantem_tipos =[ "APARTAMENTO",
                        "PREDIO",
                        "CASA COMERCIAL",
                        "SALA/CONJUNTO COMERCIAL",
                        "LOJA",
                        "PAVILHAO",
                        "LOTE/TERRENO",
                        "BOX",
                        "ANDAR",
                        "OUTROS"
                    ]
    data.loc[~data['TIPO'].isin(mantem_tipos), 'TIPO'] = "OUTROS"  # Substitui valores não na lista por "OUTRO"
    data = data[data['TIPO'].isin(mantem_tipos)]
    
    # Garante que as colunas VALORES  e VALORES_PROMO são inteiros.
    data['VALORES'] = data['VALORES'].apply(extract_integer_from_string)
    data['VALORES_PROMO'] = data['VALORES_PROMO'].apply(extract_integer_from_string)
    
    Q1_valores = data['VALORES'].quantile(0.25)
    Q3_valores = data['VALORES'].quantile(0.75)
    IQR_valores = Q3_valores - Q1_valores
    
    
    
    Q1_valores_promo = data['VALORES_PROMO'].quantile(0.25)
    Q3_valores_promo = data['VALORES_PROMO'].quantile(0.75)
    IQR_valores_promo = Q3_valores_promo - Q1_valores_promo
    
    # Define o threshold para detecção de outlier
    iqr_multiplier = 3.5
    
    
    if categoria == "Residenciais":
        data = data[(data["AREA"] < 1500)]
        
    elif categoria == "Comerciais":
        data = data[(data["AREA"] < 1500)]
    
    
    

    # Remove linhas que estejam fora dos limites.
    filtered_data = data[(data['VALORES'] >= Q1_valores - iqr_multiplier * IQR_valores) &
                         (data['VALORES'] <= Q3_valores + iqr_multiplier * IQR_valores) &
                         (data['VALORES_PROMO'] >= Q1_valores_promo - iqr_multiplier * IQR_valores_promo) &
                         (data['VALORES_PROMO'] <= Q3_valores_promo + iqr_multiplier * IQR_valores_promo)
                         ]
    
    
    tamanho_filtrados = len(filtered_data)
    diminuiu = tamanho_dataset - tamanho_filtrados
    print("########################################")
    print("Para ", tipo," de imóveis" , categoria)
    print("\nTotal de imoveis:", tamanho_dataset)
    print("\nQuantidade atual: ", tamanho_filtrados)
    print("\nDiminuição do dataset: ", diminuiu, "imóveis, equivalente a ", 100*diminuiu/(tamanho_dataset),"% \n")
    
    filtered_data.to_csv("{}/preproc_{}_{}.txt".format(local, tipo, categoria), index=False)
