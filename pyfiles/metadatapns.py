#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:19:35 2019

@author: josehcms
"""

import tablib

def get_metadata(filepath_xls):
    
    """
    Function to extract metadata from Brazilian National Health Survey 2013 (PNS)
    
        - **filepath_xls** file path for xls base dictionary file extracted from IBGE website
        
    Returns a structured variable dictionary
    """
    
    doc = tablib.Dataset()

    # leitura do arquivo
    with open(filepath_xls, 'rb') as file: # rb for read binary
        doc.load(file.read()) # carrega um fluxo de bytes no dataset
        
    # cria dicionario
    
    dicvars = {}
    part = ''
    for row in doc[1:]:
        
        # if it is the part of the questionnaire
        if row[0] and not row[1]:
             part = row[0]
        # if it reffers to the variable
        elif row[0] and row[1]:
            curvar                      = row[0]
            dicvars[curvar]             = {}
            dicvars[curvar]['pos']      = (int(row[1]),
                                           int(row[1] + int(row[2]) - 1),
                                           int(row[2]))
            dicvars[curvar]['part']     = part
            dicvars[curvar]['info']     = row[4]
            dicvars[curvar]['content']  = {}
        # if the row has the content for labels of variables
        else:
            dicvars[curvar]['content'][row[3]] = row[4] 
        
    return(dicvars)
    

dicionario=get_metadata('/media/jose/DATA/GIT/read-pns-python/dictionary/dicvar_household_pns_2013.xls')

leitura = [(var, dicionario[var]['pos'][0] - 1, dicionario[var]['pos'][1])
            for var in dicionario]


arquivo = ('/media/jose/DATA/GIT/read-pns-python/data_input/DOMPNS2013.txt')


destino = ('/media/jose/DATA/GIT/read-pns-python/data_output/DOMPNS2013.csv')


headers = ','.join(dicionario.keys()) 

with open(destino, 'w') as target:
    target.write(headers + '\n')
    with open(arquivo, 'r') as source:
        for linha in source:
            campos = []
            for var in leitura:
                campos.append((linha[var[1]:var[2]]).strip(' .')) # retira espacos e . vazios que o ibge bota
            target.write((','.join(campos)+'\n'))
            