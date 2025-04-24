## WeatherAPI

Esta API proporciona información meteorológica obtenida de OpenWeatherMap. Permite consultar datos climáticos completos o específicos de temperatura para cualquier ciudad disponible en la base de datos de OpenWeatherMap.

## 🚀 Tecnologías utilizadas:

- Python 3.10+
- FastAPI
- OpenWeatherMap API
- Swagger UI personalizado

## Crea un entorno virtual y actívalo:

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

## Instala las dependencias:

pip install fastapi uvicorn requests

## Ejecución:

uvicorn nombre_del_archivo:weather --reload

## Endpoints principales:

Método | Ruta | Descripción
GET | / | Página de inicio con ejemplos de uso
GET | /{city_name} | Pronóstico climático detallado de una ciudad
GET | /{city_name}/temp | Datos de temperatura (máx, mín, media) de la ciudad


## Errores personalizados

La API maneja errores comunes como:

502 Bad Gateway: fallas en la API externa.

404 Not Found: ciudad no encontrada.

422 Unprocessable Content: datos inválidos.

500 Internal Server Error: error interno al procesar la respuesta.


Contacto: Alcibiadeslopez21@gmail.com
