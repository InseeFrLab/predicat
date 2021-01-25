#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class and methods to easily call the API.

Created on Mon Jan 25 13:51:07 2021

@author: jeremylhour
"""

import requests


class predicat:
    """
    predicat:
        class to call the PREDICAT API.
    """
    def __init__(self, k=1, verbose=False):
        """
        init with a requests.session()
        
        @param k (int): number of categories to predict
        @param verbose (Bool): return the label of the category also?
        """
        self.session = requests.session()
        self.url = 'https://api-predicat.kub.sspcloud.fr/label?k='+str(k)+'&v='+str(verbose*1)
        
    def predict(self, libelle, trace=False):
        """
        predict:
            call the API to predict the items in libelle
            
        @param libelle (list of str): list of items to predict 
        """
        if type(libelle) == str:
            libelle = [libelle]
        
        call_url = self.url+'&q='+'&q='.join(libelle)
        response = self.session.get(call_url)
        
        if response.ok and trace:
            print('Response received.')
        return response.json()
    
    def decode(self, categorie, trace=False):
        """
        decode:
            returns the title of the NA2008 category

        @param categorie (list): categories to decode
        """
        if type(categorie) == str:
            categorie = [categorie]
            
        na2008_url = 'https://api-predicat.kub.sspcloud.fr/na2008?q='+'&q='.join(categorie)
        response = self.session.get(na2008_url)
        if response.ok and trace:
            print('Response received.')
        return response.json()
    
    
# Example
classifier = predicat()

classifier.predict('SAVON DE MARSEILLE')
classifier.decode('C20B')