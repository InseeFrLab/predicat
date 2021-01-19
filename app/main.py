# -*- coding: utf-8 -*-
"""
Main file for the API.
Created on Tue Jan 12 11:58:03 2021
@author: jeremylhour, Yves-Laurent Benichou
"""

import fasttext
import yaml

from typing import Optional
from fastapi import FastAPI

from utils_ddc import preprocess_text, predict_using_model

app = FastAPI()
models={}

@app.on_event("startup")
def startup_event():
    config_file= 'config.yaml' 
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    model_list=config['models']
    global models
    models={model:fasttext.load_model(config['model_conf'][model]['file']) for model in model_list}


@app.get("/")
def read_root():
    # mettre les dernieres infos du modele
    # avec un fichier config yaml
    return {"Hello": "World"}


@app.get("/label")
async def predict_label(text: str, k: int=1):
    output = {'query': text,
              'count': k,
              'result': predict_using_model(x=preprocess_text(text), model=models['na2008'], k=k)
              }
    return output 


@app.get("/process")
async def process(text: str):
    return preprocess_text(text)

'''
@app.get("/na2008")
async def na2008(text: str):
    pass
    return
'''
