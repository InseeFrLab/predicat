# -*- coding: utf-8 -*-
"""
Main file for the API.
Created on Tue Jan 12 11:58:03 2021
@author: jeremylhour, Yves-Laurent Benichou
"""

import fasttext
import yaml
import csv

from typing import Optional
from fastapi import FastAPI

from utils_ddc import preprocess_text, predict_using_model

def read_yaml(file):
    with open(file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config

def read_dict(file):
    with open(file, mode='r',encoding='utf8') as f_in:
        reader = csv.reader(f_in,delimiter=';')
        dict_from_csv = {rows[0].strip():rows[1].strip() for rows in reader}
    return dict_from_csv

app = FastAPI()

@app.on_event("startup")
def startup_event():
    global models,config,dict_na2008
    config=read_yaml('config.yaml')
    dict_na2008=read_dict('nomenclatures/nomenclature_na2008.csv')
    models={model:fasttext.load_model('model/'+config['model_conf'][model]['file']) for model in config['models']}

@app.get("/")
async def read_root():
    output = {model : config['model_conf'][model] for model in config['models']}
    return { "loaded models" : output }

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

@app.get("/na2008")
async def na2008(code: str):
    return {code: dict_na2008.get(code,None)}
