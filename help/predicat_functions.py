#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class and methods to easily call the API.

Created on Mon Jan 25 13:51:07 2021

@author: jeremylhour&byl
"""

import requests
url='https://api.lab.sspcloud.fr/predicat/' # change with url of the service API

class predicat:
    """
    predicat:
        class to call the PREDICAT API.
    """
    def __init__(self):
        """
        init with a requests.session()
        
        
        """
        self.session = requests.session()
        self.url = url
        
    def predict(self, libelle, k=1, verbose=False, trace=False):
        """
        predict:
            call the API to predict the items in libelle

        @param k (int): number of categories to predict
        @param verbose (Bool): return also the label of the predicted category
        @param libelle (list of str): list of items to predict 
        """
        if type(libelle) == str:
            libelle = [libelle]
        
        call_url = self.url+'label?k='+str(k)+'&v='+str(verbose*1)+'&q='+'&q='.join(libelle)
        response = self.session.get(call_url)
        
        if response.ok and trace:
            print('Response received.')
        return response.json()
    
    def decode(self, categorie, trace=False):
        """
        decode:
            returns the label of a category

        @param categorie (list): categories to decode
        """
        if type(categorie) == str:
            categorie = [categorie]
            
        call_url = self.url+'label_description?q='+'&q='.join(categorie)
        response = self.session.get(call_url)
        if response.ok and trace:
            print('Response received.')
        return response.json()
    
    
# Example
classifier = predicat()

print(classifier.predict(['SAVON DE MARSEILLE',"Jus d'orange 1 litre"],verbose=True))
print(classifier.decode('05.6.1.1.1'))