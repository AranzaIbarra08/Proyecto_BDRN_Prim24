import csv
from neo4j import GraphDatabase
import json


uri = "bolt://neo4j_db:7687"
driver = GraphDatabase.driver(uri)

def add_meal(tx, meal_name, category, area, ingredients):
    query = (
        "CREATE (m:Meal {name: $name, category: $category, area: $area, ingredients: $ingredients})"
    )
    tx.run(query, name=meal_name, category=category, area=area, ingredients=ingredients)

def import_meals(file_path):
    with driver.session() as session:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                meal_name = row['strMeal']
                category = row['strCategory']
                area = row['strArea']
                ingredients_str= row['ingredients'].replace("''", '"').replace('""', '"')
                ingredients = json.loads(ingredients_str)
                session.execute_write(add_meal, meal_name, category, area, ingredients)

if __name__ == "__main__":
    file_path = 'meals_filtered.csv'
    import_meals(file_path)

    print("Meals imported successfully.")

driver.close()