# PREDICAT

API pour classification des libellés de caisse

En lien avec l'application: https://github.com/InseeFrLab/product-labelling

# Quick start

```
git clone https://github.com/InseeFrLab/predicat.git
cd predicat
pip3 install -r requirements.txt
cd app
uvicorn main:app # model not found
wget https://minio.lab.sspcloud.fr/conception-logicielle/model_na2008.bin
# déplacer le modèle dans app/model
uvicorn main:app
```
