##Para importar los ingredientes 
from neo4j import GraphDatabase

# Neo4j connection URI and credentials
uri = "bolt://neo4j_db:7687"  # Replace with your Neo4j URI

# Initialize Neo4j driver
driver = GraphDatabase.driver(uri)

def add_ingredient(tx, name):
    tx.run("CREATE (:Ingredient {name: $name})", name=name)

def import_ingredients(file_path):
    with driver.session() as session:
        with open(file_path, 'r') as file:
            next(file)  # Skip the header line
            for line in file:
                ingredient_name = line.strip()  # Extract ingredient name
                if ingredient_name:  # Check if the line is not empty
                    session.execute_write(add_ingredient, ingredient_name)

if __name__ == "__main__":
    file_path = 'ingredients.csv'
    import_ingredients(file_path)

    print("Ingredients imported successfully.")

driver.close()
