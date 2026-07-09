# Miniproyecto final semana 1
# Extracción masiva de datos, filtracion de dichos datos y los pasa a un csv

import json
import pandas as pd
import requests

URL_USERS = 'https://dummyjson.com/users'
URL_POSTS = 'https://dummyjson.com/posts'

TOKEN = 'token_secreta'

cabeceras = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json; charset=utf-8'
}

# Lista vacía para acumular datos de forma eficiente
lista_dataframes = []

try:
    r1 = requests.get(URL_USERS)
    print(pd.json_normalize(r1.json()['users']))
except Exception as e:
    print()

try:
    r2 = requests.get(URL_POSTS)
    print(pd.json_normalize(r2.json()['posts']))
except Exception as e:
    print()