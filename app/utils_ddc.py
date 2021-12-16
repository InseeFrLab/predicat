#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All necessary functions

Created on Tue Jan 12 11:58:03 2021

@author: jeremylhour & byl
"""
import re
import pandas as pd
from typing import List


def predict_using_model(descriptions: List[str], model, k: int = 1):
    """
    predict_using_model: 
        Encapsulates fastText predict method to predict labels for a list of product descriptions.
        Outputs Returns a list (of length the number of descriptions) of lists (of length k) of dictionaries. 
    
    :param x: List(str): List of product descriptions to classify.
    :param model: fastText model.
    :param k: int: This function outputs the top k predictions. Default is 1.
    """
    output = model.predict(descriptions, k=k+(k==1)*1)

    all_predictions = []
    all_predicted_labels = output[0]
    all_predicated_probas = output[1]
    for predicted_labels, predicted_probas in zip(all_predicted_labels, all_predicated_probas):
        clean_labels = [re.findall('(?<=__label__).*$', str(label))[0] for label in predicted_labels]
        clean_probas = [format(p, '0.3f') for p in predicted_probas]
        confiance = [None] * k
        confiance[0] = format(predicted_probas[0] - predicted_probas[1], '0.3f')
    
        prediction = []
        for i in range(k):
            prediction.append({'label': clean_labels[i],
                               'proba': clean_probas[i],
                               'confiance': confiance[i]})
        all_predictions.append(prediction)

    return all_predictions


def preprocess_text(text: str):
    """
    preprocess_text:
        Cleans the text as per fasttext requirements.
    
    :text: str: text to clean
    :returns: str: cleaned text
    """
    text = text.upper()
    for pattern, replace in replace_values_ean.items():     # Substitution des regex appropriés à partir du dictionnaire de règles
        text = re.sub(pattern,replace,text)   
    text=re.sub(r'([ ]{2,})',' ',text)                      # Suppression des espaces multiples
    return text.strip()                                     # Suppression des espaces autour de la chaine


# Dictionnaires nécessaires pour les nettoyages
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
