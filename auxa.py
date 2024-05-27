import csv
from neo4j import GraphDatabase
import json

# Function to create relationships
def create_relationship(tx, meal_name, ingredient_name):
    query = (
        "MATCH (m:Meal {name: $meal_name}), (i:Ingredient {name: $ingredient_name}) "
        "MERGE (m)-[:CONTAINS]->(i)"
    )
    tx.run(query, meal_name=meal_name, ingredient_name=ingredient_name)

# Connect to Neo4j
driver = GraphDatabase.driver("neo4j://neo4j_db:7687")


# Open the CSV file for meals
with open('meals_filtered.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # For each line in the CSV...
    for row in reader:
        # Extract the meal name
        meal_name = row['strMeal']
        ingredients_str = row['ingredients'].replace("''", '"').replace('""', '"')
        ingredients = json.loads(ingredients_str)  # Now ingredients is a Python list
        
        
        # Run the transaction for each ingredient in the list
        with driver.session() as session:
            try:
                for ingredient in ingredients:
                    session.execute_write(create_relationship, meal_name, ingredient)
            except Exception as e:
                print(f"Failed to create relationships for {meal_name}: {str(e)}")

# Close the driver
driver.close()