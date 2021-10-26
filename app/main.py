# -*- coding: utf-8 -*-
"""
Main file for the API.
Created on Tue Jan 12 11:58:03 2021
@author: jeremylhour, Yves-Laurent Benichou
"""

import fasttext
import yaml
import csv

from typing import Optional, List
from fastapi import FastAPI, Query

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

app = FastAPI(
    title="Predicat",
    description="Predict category from a product description",
    version="1.0.0")

@app.on_event("startup")
def startup_event():
    global models,config,dict_na2008
    config=read_yaml('config.yaml')
    dict_na2008=read_dict('nomenclatures/nomenclature_NA2008.csv')
    models={model:fasttext.load_model('model/'+config['model_conf'][model]['file']) for model in config['models']}

@app.get("/")
async def read_root():
    output = {model : config['model_conf'][model] for model in config['models']}
    return { "active models" : output }

@app.get("/label")
async def predict_label(q: List[str] = Query(..., title="query string", description="Description of the product to be classified"),\
        k: int = Query(1, title="top-K", description="Specify num of predictions to be displayed"),\
        v: Optional[bool] = Query(False, title="verbosity", description="If True, displays label of category")):
    output={}
    for item in set(q):
        pred=predict_using_model(x=preprocess_text(item), model=models['na2008'], k=k)
        if v:
            for i in pred:
                i['label']+=" | "+ dict_na2008.get(i['label'],None)
        output[item]=pred
    return output
    
@app.get("/process")
async def process(q: List[str] = Query(..., title="Query string",\
        description="Process description cleaning algorithm")):
    output={}
    for item in set(q):
        output[item]=preprocess_text(item)
    return output 

@app.get("/na2008")
async def na2008(q: List[str] = Query(..., title="Query string",\
        description="Convert NA2008 code to description")):
    output={}
    for item in set(q):
        item=item.upper()
        output[item]=dict_na2008.get(item,None)
    return output 
