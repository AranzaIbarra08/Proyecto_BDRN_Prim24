import requests
import pymongo
from dotenv import load_dotenv 
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = f"https://www.themealdb.com/api/json/v2/{API_KEY}/search.php?f="

client = pymongo.MongoClient("mongodb://mongo_lake:27017")
db = client["meals"]
collection_formatted = db["dishes"]
filtro=[None, "", " "]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'v', 'w', 'y']
for letter in letters:
    print(letter)
    
    # Hacer la solicitud a la API
    response = requests.get(url + str(letter)).json()
    
    # Iterar sobre los platos y crear listas para strInstructions, strIngredient y strMeasure
    if response["meals"]:
        for dish in response["meals"]:

            ingredients = [dish[key] for key in dish if key.startswith("strIngredient") and dish[key] not in filtro ]
            measures = [dish[key] for key in dish if key.startswith("strMeasure") and dish[key] not in filtro]
            
            # Crear un nuevo diccionario limpio sin las claves que ya se han procesado
            clean_dish = {key: value for key, value in dish.items() if key not in {"strIngredient", "strMeasure"}}
            
            # Eliminar las claves "strIngredient" y "strMeasure" del rango 1-15, ya que están dentro de un diccionario
            for num in range(1, 21):  # Ajuste a 20, ya que los ingredientes y medidas pueden llegar hasta 20
                ingredient_key = f"strIngredient{num}"
                measure_key = f"strMeasure{num}"
                if ingredient_key in clean_dish:
                    del clean_dish[ingredient_key]
                if measure_key in clean_dish:
                    del clean_dish[measure_key]
            
            # Agregar las listas y el diccionario de instrucciones al nuevo diccionario
            #clean_dish["instructions"] = instructions
            clean_dish["ingredients"] = ingredients
            clean_dish["measures"] = measures
            
            # Insertar cada plato individual en MongoDB
            collection_formatted.insert_one(clean_dish)
    

    
# Una colección para guardar únicamente los ingredientes
collection_ingredients = db["ingredients"]
url_ingredients = f"http://www.themealdb.com/api/json/v2/{API_KEY}/list.php?i=list"
response_ingredients = requests.get(url_ingredients).json()

for ingredient in response_ingredients["meals"]:
    collection_ingredients.insert_one(ingredient)
