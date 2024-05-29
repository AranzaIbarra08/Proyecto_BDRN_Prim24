# Proyecto BDNR Primavera 2024

Equipo: [Aranza Ibarra](https://github.com/AranzaIbarra08), [Frida Márquez](https://github.com/fridamarquezg), [Victor Esparza](https://github.com/VictorHEsp), [Armando Limón](https://github.com/ArmandoLimn).

## Estructura del Proyecto
- `data/`: Contiene archivos de datos utilizados en el proyecto.
- `scripts/`: Incluye scripts para la obtención y procesamiento de datos.
- `src/`: Código fuente principal del proyecto.
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

El uso de la página donde se encuentran algunas de las recetas de MealDB es gratuita. Sin embargo, para tener acceso a la versión beta de la API, que permite filtros de múltiples ingredientes, agregar tus propias comidas e imágenes y listar la base de datos completa hay que pagar $50 (mxn). 

## Archivos .csv
Los archivos `ingridients.csv` y `meals_filtered.csv`que se encuentran en la carpeta `data` fueron creados siguiendo estos pasos:

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
Después de obtener los datos de la API de MealDB, los insertamos en MongoDB con un script de Python. 
Creamos dos colecciones:

* `meals`: almacena los elementos en un formato fácil de leer en MongoDB.
* `ingredients`: incluye todos los ingredientes disponibles en la API.

Los elementos en la colección `meals` tienen la siguiente estructura:
    
    ```
    meals.findOne()
    ```
Mientras que los elementos de la colección `ingredients` tienen esta estructura:
    ```
    ingredients.findOne()
    ```
# Consultas
Para realizar las consultas en MongoDB, es necesario seguir estos pasos:
1. Acceder al contenedor de MongoDB que está en el Docker Compose.
    ```bash
    docker exec -it mongo_lake mongosh
    ```
2. Activar la colección `meals`.
    ```
    use meals
    ```
3. Ejecutar las consultas

    a. Contar la cantidad de comidas que hay por región y categoría.
    ```javascript
    db.dishes.aggregate([
    { $group: {
        _id: { category: "$strArea", area: "$strCategory" },
        count: { $sum: 1 }
    }},
    { $sort: { count: -1 }}
    ]).pretty()
    ```

    b. El nombre, categoría y región de la comida que tienen más de un tag ordenadas por nombre.
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

    c. Contar la cantidad de comidas que hay por la inicial de su nombre.

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


## Neo4j

# Consultas


