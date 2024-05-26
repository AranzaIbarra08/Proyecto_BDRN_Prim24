from pymongo import MongoClient
import requests

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mealdb"]
collection = db["meals"]

# Función para obtener datos de una comida por ID
def fetch_meal_data(meal_id):
   response = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}")
   if response.status_code == 200:
      data = response.json()
      if data["meals"]:
         return data["meals"][0]
      else:
         return None
   else:
      return None

# Función para insertar datos de una comida en la base de datos
def insert_meal_data(meal_id):
   meal_data = fetch_meal_data(meal_id)
   if meal_data:
      collection.insert_one(meal_data)
      print(f"Meal {meal_data['strMeal']} inserted into the database.")
   else:
      print(f"Error fetching data for meal ID {meal_id}.")

if __name__ == "__main__":
   for meal_id in range(50000, 55000):
      insert_meal_data(meal_id)
