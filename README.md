# PREDICAT

API pour classification des libellés de caisse

En lien avec l'application: https://github.com/InseeFrLab/product-labelling

## Quick start

```
git clone https://github.com/InseeFrLab/predicat.git
cd predicat
pip3 install -r requirements.txt
cd app
uvicorn main:app # model not found
```

## Using models

Sample model : na2008_old
```
wget https://minio.lab.sspcloud.fr/conception-logicielle/model_na2008.bin
```

All models are loaded in startup through : 
`config.yaml`

```yaml
project:
  name: predicat

models:
  - na2008_old
  - na2008
  - coicop
  
model_conf:
  na2008_old:
    file: model_na2008.bin
    desc: Model trained on products in IRI+DDC dataset 
    date: 2020/12/14
  
  na2008:
    file: code_na2008_2021-12-10.bin
    desc: Model trained with use_in_train=True 
    date: 2021/12/10

  iri:
    file:
    date:  
  
  coicop:
    file: model_coicop10.bin
    desc: Model trained on products in IRI+DDC dataset
    date: 2021/11/02
```

Be sure to take all your belongings with you.
> Non en gros il faut que vous supprimiez éventuellement les entrées de {models:[]} que vous n'avez pas.


 
