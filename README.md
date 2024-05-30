# Proyecto BDNR Primavera 2024

Equipo: [Aranza Ibarra](https://github.com/AranzaIbarra08), [Frida Márquez](https://github.com/fridamarquezg), [Victor Esparza](https://github.com/VictorHEsp), [Armando Limón](https://github.com/ArmandoLimn).

## Estructura del Proyecto
- `data/`: Contiene archivos de datos utilizados en el proyecto.
- `img/`: Contiene imagenes ilustrativas utilizadas en el README del proyecto.
- `scripts/`: Incluye scripts para la obtención y procesamiento de datos.
- `Dockerfile.venv`: Configuración para el entorno virtual de Docker.
- `docker-compose.yml`: Configuración para la orquestación de contenedores Docker.
- `requirements.txt`: Lista de dependencias del proyecto.


## Instrucciones 
1. Hacer un Fork y clonar a tu local este repositorio. 
2. Dentro de la carpeta del repositorio, crear un archivo .env con la llave para la API.
3. En la carpeta del repositorio, escribir el siguiente comando en la terminal:
    ```bash
    docker compose up -d
    ```
    Nota: es importante asegurarte de que Docker este corriendo, de lo contrario marcará error.

4. Comprobar que los contenedores estén corriendo con el siguiente comando:
    ```bash
    docker ps
    ```
    Nota: Tal vez puede tomar unos minutos que todo se ejecute adecuadamente.

## API: MealDB
[MealDB](https://www.themealdb.com/) es una base de datos que tiene una amplia colección de recetas de comidas de todo el mundo. Actualmente, MealDB cuenta con 303 recetas y 575 ingredientes. Por cada receta, incluye detalles como ingredientes, instrucciones de preparación, áreas geográfica, imagen del platillo y categorías (o tags). 

El uso de la página donde se encuentran algunas de las recetas de MealDB es gratuita. Sin embargo, para tener acceso a la versión beta de la API, que permite filtros de múltiples ingredientes, agregar tus propias comidas e imágenes y listar la base de datos completa hay que pagar €3.6, aproximadamente $66 (mxn). 

![Meal_DB](./img/img_mealdb.jpg)

## Clave para acceder a la API
Dentro de el repositorio deberás crear un archivo `.env` con la llave de la API. Por motivos de seguiridad, los archivos `.env` fueron agregados al `gitignore`.  

## Archivos .csv
Los archivos `ingridients.csv` y `meals_filtered.csv`que se encuentran en la carpeta `data` fueron creados siguiendo estos pasos:

Nota: No es necesario realizar estos pasos si quieres ejecutar el proyecto. Son solo explicativos.

1. Entrar al bash del contenedor de Mongo.
    ```
    docker exec -it mongo_lake /bin/bash
    ```
2. Dentro del bash de Mongo, ejecutamos los siguientes comandos para exportar las colecciones a archivos .csv
    ```
    mongoexport --db meals --collection ingredients --type=csv --fields strIngredient --out /data/db/ingredients.csv
    ```
    ```
    mongoexport --db meals --collection dishes --type=csv --fields strMeal, strCategory, strArea --out /data/db/meals_filtered.csv
    ```

Una vez ejecutados, fuera del bash de Mongo, corrimos los siguientes comandos para guardar los archivos en la carpeta `data`:
```
docker cp mongo_lake:/data/db/ingredients.csv ./data
```
```
docker cp mongo_lake:/data/db/meals_filtered.csv ./data
```
    
## MongoDB

![Mongo_DB](./img/img_mongo.png)
Después de obtener los datos de la API de MealDB, los insertamos en MongoDB con un script de Python. 
Creamos dos colecciones dentro de la base de datos `meals`:

* `dishes`: almacena los platillos.
* `ingredients`: incluye todos los ingredientes.

Los elementos en la colección `dishes` tienen la siguiente estructura:
```
    {
        _id: ObjectId('6653f8b8c7650bfd6e7e6552'),
        idMeal: '52768',
        strMeal: 'Apple Frangipan Tart',
        strDrinkAlternate: null,
        strCategory: 'Dessert',
        strArea: 'British',
        strInstructions: 'Preheat the oven to 200C/180C Fan/Gas 6.\r\n' +
            'Put the biscuits in a large re-sealable freezer bag and bash with a rolling pin into fine crumbs. Melt the butter in a small pan, then add the biscuit crumbs and stir until coated with butter. Tip into the tart tin and, using the back of a spoon, press over the base and sides of the tin to give an even layer. Chill in the fridge while you make the filling.\r\n' +
            'Cream together the butter and sugar until light and fluffy. You can do this in a food processor if you have one. Process for 2-3 minutes. Mix in the eggs, then add the ground almonds and almond extract and blend until well combined.\r\n' +
            'Peel the apples, and cut thin slices of apple. Do this at the last minute to prevent the apple going brown. Arrange the slices over the biscuit base. Spread the frangipane filling evenly on top. Level the surface and sprinkle with the flaked almonds.\r\n' +
            'Bake for 20-25 minutes until golden-brown and set.\r\n' +
            'Remove from the oven and leave to cool for 15 minutes. Remove the sides of the tin. An easy way to do this is to stand the tin on a can of beans and push down gently on the edges of the tin.\r\n' +
            'Transfer the tart, with the tin base attached, to a serving plate. Serve warm with cream, crème fraiche or ice cream.',
        strMealThumb: 'https://www.themealdb.com/images/media/meals/wxywrq1468235067.jpg',
        strTags: 'Tart,Baking,Fruity',
        strYoutube: 'https://www.youtube.com/watch?v=rp8Slv4INLk',
        strSource: null,
        strImageSource: null,
        strCreativeCommonsConfirmed: null,
        dateModified: null,
        ingredients: [
            'digestive biscuits',
            'butter',
            'Bramley apples',
            'butter, softened',
            'caster sugar',
            'free-range eggs, beaten',
            'ground almonds',
            'almond extract',
            'flaked almonds'
        ],
        measures: [
            '175g/6oz', '75g/3oz',
            '200g/7oz', '75g/3oz',
            '75g/3oz',  '2',
            '75g/3oz',  '1 tsp',
            '50g/1¾oz'
        ]
    }
```
    
Mientras que los elementos de la colección `ingredients` tienen esta estructura:

```
    {
    _id: ObjectId('6653f8c3c7650bfd6e7e667f'),
    idIngredient: '1',
    strIngredient: 'Chicken',
    strDescription: 'The chicken is a type of domesticated fowl, a subspecies of the red junglefowl (Gallus gallus). It is one of the most common and widespread domestic animals, with a total population of more than 19 billion as of 2011. There are more chickens in the world than any other bird or domesticated fowl. Humans keep chickens primarily as a source of food (consuming both their meat and eggs) and, less commonly, as pets. Originally raised for cockfighting or for special ceremonies, chickens were not kept for food until the Hellenistic period (4th–2nd centuries BC).\r\n' +
        '\r\n' +
        'Genetic studies have pointed to multiple maternal origins in South Asia, Southeast Asia, and East Asia, but with the clade found in the Americas, Europe, the Middle East and Africa originating in the Indian subcontinent. From ancient India, the domesticated chicken spread to Lydia in western Asia Minor, and to Greece by the 5th century BC. Fowl had been known in Egypt since the mid-15th century BC, with the "bird that gives birth every day" having come to Egypt from the land between Syria and Shinar, Babylonia, according to the annals of Thutmose III.',
    strType: null
    }
```
    
### Consultas
Para realizar las consultas en MongoDB, es necesario seguir estos pasos:
1. Acceder al contenedor de MongoDB que está en el Docker Compose.
    ```bash
    docker exec -it mongo_lake mongosh
    ```
2. Activar la base de datos `meals`.
    ```
    use meals
    ```
3. Ejecutar las consultas:

    a. Contar la cantidad de comidas que hay por región y categoría:
    ```javascript
    db.dishes.aggregate([
    { $group: {
        _id: { category: "$strArea", area: "$strCategory" },
        count: { $sum: 1 }
    }},
    { $sort: { count: -1 }}
    ]).pretty()
    ```

    b. El nombre, categoría y región de la comida que tienen más de un tag ordenadas por nombre:
    ```javascript
    db.dishes.find({
        "strTags": { $regex: ",", $options: "i" }
    },
    {
        _id: 0,
        strMeal: 1,
        strCategory: 1,
        strArea: 1,
        strTags: 1
    }).sort({ strMeal: 1 }).pretty()
    ```

    c. Contar la cantidad de comidas que hay por la inicial de su nombre:
    ```javascript
    db.dishes.aggregate([
    { $project: {
        firstLetter: { $substrCP: ["$strMeal", 0, 1] },
        strMeal: 1
    }},
    { $group: {
        _id: "$firstLetter",
        count: { $sum: 1 }
    }},
    { $sort: { _id: 1 }}
    ]).pretty()
    ```
    
    d. Cantidad de platillos por número de ingredientes:
    ```javascript
    db.dishes.aggregate([
    { $project: {
        cantIngredientesXPlatillo: { $size: { $ifNull: ["$ingredients", []] } }
    }},
    { $group: {
        _id: "$cantIngredientesXPlatillo",
        countPlatillos: { $sum: 1 }
    }},
    { $project: {
        cantIngredientesXPlatillo: "$_id",
        countPlatillos: 1,
        _id: 0
    }},
    { $sort: { cantIngredientesXPlatillo: 1 }}
    ]).pretty()
    ```

## Neo4j
![Mongo_DB](./img/img_neo.png)
Para entrar al contenedor de Neo4j en el Docker Compose usamos tres scripts de Python:

* importIngridientsNeo4j: Crea objetos tipo `Ingredient` dentro de Neo4j.
* importMealsNeo4j: Crea objetos tipo `Meal` dentro de Neo4j.
* importRelationsNeo4j: Crea relaciones tipo `contains` y une `ingredients` a `meals`. 

### Consultas
Para realizar las consultas en Neo4j, es necesario seguir estos pasos:
1. Acceder al contenedor de Neo4j que está en el Docker Compose copiando el siguiente comando en el browser. 
```
localhost:7474/browser/
```
2. Oprimir el boton `Connect` (Este contenedor de Neo4j no pide usuario y contraseña).

3. Hacer las consultas:

    #### Consultas para conocer la elementos de la base de datos:

    a. Ver visualmnete la estrucutra de la base de datos (es decir, objetos y como están conectados)
    ```cypher
    MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100
    ```

    b. Ver la estructura de un objeto del tipo Meal
    ```cypher
    MATCH (m:Meal) RETURN m LIMIT 1
    ```

    c. Ver la estructura de un objeto del tipo Ingredient
    ```cypher
    MATCH (i:Ingredient) RETURN i LIMIT 1
    ```

    d. Ver todas las categorías de comida que hay
    ```cypher
    MATCH (m:Meal)
    RETURN DISTINCT m.category AS Category
    ```

    #### Consultas más específicas:

    a. Encontrar todas las Meals que contienen un Ingredient específico (en este caso "Chicken"), y ver de que región es cada platillo:
    ```cypher
    MATCH (i:Ingredient {name: "Chicken"})<-[:CONTAINS]-(m:Meal)
    RETURN m.name AS MealName, m.area AS Area
    ```

    b. Encontrar todos los Ingredients que se utilizan para una categoría de Meal específica (en este caso "Dessert):
    ```cypher
    MATCH (m:Meal {category: "Dessert"})-[:CONTAINS]->(i:Ingredient)
    RETURN DISTINCT i.name AS IngredientName
    ```

    c. Mostrar cuántos Ingredients tiene cada Meal, y ordenarlo por nombre descendiente:
    ```cypher
    MATCH (m:Meal)-[:CONTAINS]->(i:Ingredient)
    WITH m.name AS MealName, COLLECT(DISTINCT i.name) AS IngredientsList
    RETURN MealName, SIZE(IngredientsList) AS NumberOfDistinctIngredients
    ORDER BY NumberOfDistinctIngredients DESC
    ```

    d. Mostrar todas las Meals que no contienen un Ingredient en específico:
    ```cypher
    MATCH (m:Meal)
    WHERE NOT (m)-[:CONTAINS]->(:Ingredient {name: "Chicken"})
    RETURN m.name AS MealName, m.category AS Category, m.area AS Area
    ```

    e. Encontrar el Ingredient más común, y en cuántas Meals aparece:
    ```cypher
    MATCH (i:Ingredient)<-[:CONTAINS]-(m:Meal)
    WITH i, COLLECT(DISTINCT m.name) AS MealNames
    RETURN i.name AS IngredientName, SIZE(MealNames) AS NumberOfMeals
    ORDER BY NumberOfMeals DESC
    LIMIT 5
    ```

    f. Encontrar promedio, cuántos Ingredients hay en cada Meal, de cada tipo:
    ```cypher
    MATCH (m:Meal)
    WITH m.category AS category, SIZE(m.ingredients) AS ingredientCount
    RETURN category, AVG(ingredientCount) AS averageIngredientCount
    ORDER BY averageIngredientCount DESC
    ```

    g. Mostrar las Meals que contienen todos los Ingredients de una lista determinada:
    ```cypher
    MATCH (m:Meal)-[:CONTAINS]->(i:Ingredient)
    WITH m, COLLECT(i.name) AS ingredientList
    WHERE ALL(ingredient IN ["Bread", "Eggs", "Black Pudding"] WHERE ingredient IN ingredientList)
    RETURN DISTINCT(m.name) AS MealName
    ```

    h. Encontra las Meals que, a partir del número de ingredientes que comparten, podríamos considerar que son los más similares:
    ```cypher
    MATCH (m1:Meal)-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(m2:Meal)
    WHERE m1.name <> m2.name
    WITH DISTINCT m1, m2, COUNT(i) AS sharedIngredients, COLLECT(DISTINCT i.name) AS sharedIngredientList
    MATCH (m1)-[:CONTAINS]->(i1:Ingredient)
    WITH DISTINCT m1, m2, sharedIngredients, sharedIngredientList, COUNT(DISTINCT i1) AS totalIngredients1
    MATCH (m2)-[:CONTAINS]->(i2:Ingredient)
    WITH DISTINCT m1, m2, sharedIngredients, sharedIngredientList, totalIngredients1, COUNT(DISTINCT i2) AS totalIngredients2
    RETURN m1.name AS Meal1, m2.name AS Meal2, sharedIngredients, sharedIngredientList,
        (2.0 * sharedIngredients) / (totalIngredients1 + totalIngredients2) AS similarityScore
    ORDER BY similarityScore DESC
    LIMIT 1
    ```