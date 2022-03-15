# PREDICAT

API pour classification des libellés de caisse

En lien avec l'application: https://github.com/InseeFrLab/product-labelling

## Quick start

```
git clone https://github.com/InseeFrLab/predicat.git
cd predicat
pip3 install -r requirements.txt
cd app
uvicorn main:app # model not found, see below
```

## Using models

Predicat loads all models defined in [config.yaml](config.yaml).  
```yaml
models:
  - na2008_old
```  

Predicat needs at least one model to start.  
Referencing a model that does not exist leads to a `ValueError` :  
```
ValueError: model/model_na2008.bin cannot be opened for loading!
```

A basic model, for demonstration purposes, can be downloaded here :  
[https://minio.lab.sspcloud.fr/conception-logicielle/model_na2008.bin](https://minio.lab.sspcloud.fr/conception-logicielle/model_na2008.bin)

```  
curl https://minio.lab.sspcloud.fr/conception-logicielle/model_na2008.bin -o model_na2008.bin  
mkdir model  
mv model_na2008.bin model/model_na2008.bin
```





