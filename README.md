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

## Docker Compose

## MongoDB

## Neo4j


