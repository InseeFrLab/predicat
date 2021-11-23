#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All necessary functions

Created on Tue Jan 12 11:58:03 2021

@author: jeremylhour & byl
"""
import re
import pandas as pd


def predict_using_model(x, model, k=1):
    """
    predict_from_model: 
        encapsulates fastText predict method to output clean variables.
        Outputs a list of dictionaries of len k.
    
    :param x: string, description of product to classify
    :param model: fastText model
    :param k: k for top-k prediction. default is k=1
    """    
    output = model.predict(x, k=k+(k==1)*1)
    clean_labels = [re.findall('(?<=__label__).*$', str(label))[0] for label in output[0]]
    clean_proba = [format(p, '0.3f') for p in output[1]]
    confiance = [None]*k
    confiance[0] = format(output[1][0] - output[1][1], '0.3f')
    
    prediction = []
    for i in range(k):
        prediction.append({'label': clean_labels[i],
                           'proba': clean_proba[i],
                           'confiance': confiance[i]})   
    return prediction


def preprocess_text(text: str):
    """
    preprocess_text:
        Cleans the text as per fasttext requirements.
    
    :text: str: text to clean
    :returns: str: cleaned text
    """
    text = text.upper()
    
    df = pd.DataFrame([{'libelle' : text}])
    df.replace({'libelle': replace_values_ean}, regex=True, inplace=True) # Substitution des regex appropriés
    df.replace({'libelle': replace_whitespaces}, regex=True, inplace=True) # Suppression des espaces multiples
    df['libelle'] = df['libelle'].str.strip() # Suppression des espaces autour de la chaine

    return str(df.loc[0,'libelle'])


# Dictionnaires nécessaires pour les nettoyages
replace_whitespaces = {r'([ ]{2,})': ' '}

replace_values_ean = {
            'NON RENSEIGNE': '',
            'NON CONNUE': '',
            'INCONNU': '',
            'QUEL GROUPE:': '',
            'FIN DE SERIE': '',
            'THIRD PARTY ITEM': '',
            'DECOTE': '',
            'SOLDES': '',
            'DEGAGEMENT': '',
            'PROMO DATE COURTE': '',
            'DLC COURTE': '',
            'FIELD COLLECTED IMAGE RECEIVED': '',
            '&AMP': ' ',
            '&QT': '',
            '&QUOT': '',
            '&TILT': '',
            '&GT': '',
            r"[a-zA-Z]\'": '',
            r"\'": ' ',
            '\.': ' ',
            ',': ' ',
            ';': ' ',
            r'\(': '',
            r'\)': '',
            r'\*': '',
            r'\-': '',
            r'\!': '',
            r'\?': '',
            '&': ' ',
            '/': ' ',
            '\+': ' ',
            r'\d+\.?\d*\s?(K?GR?)\b': ' #POIDS ',
            r'\d+\.?\d*\s?(C?MM?)\b': ' #DIMENSION ',
            r'\d+\.?\d*\s?([CM]?L)\b': ' #VOLUME ',
            r'\d+\.?\d*\s?%': ' #POURCENTAGE ',
            r'\d+\s?(X|\*)\s?\d*\b': ' #LOT ',
            r'\d*\s?(X|\*)\s?\d+\b': ' #LOT ',
            r'\d+\.?\d*\s?(CT)\b': ' #UNITE ',
            r'(\sX*S\b)|(\sM\b)|(\sX*L\b)': ' #TAILLE ',
            r'\s\d{2,}\/\d{2,}\b': ' #TAILLE ',
            r'\s\d+\b': ' ',
            r'^\d+ ': '',
            r'^[0-9]+$': '',       # pour éliminer les codes barres introduits par inadvertance
            r'[^a-zA-Z\d\s#]': ''  # supprime tous les caractères non alphanumeriques
        }
