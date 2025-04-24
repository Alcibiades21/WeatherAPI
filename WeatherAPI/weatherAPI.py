from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import requests



weather = FastAPI(docs_url=None, redoc_url=None)
weather.mount("/static", StaticFiles(directory="static"), name="static")


def validacion_Errores(status_code):
    if status_code == 502:
        return {
            "error": "Bad Gateway",
            "message": "Fallas en la api externa",
            "status_code": status_code
        }
    elif status_code == 422:
        return {
            "error": "Unprocessable Content",
            "message": "Su solicitud fue incorrecta, por favor vuelva intentarlo",
            "status_code": status_code
        }
    elif status_code == 404:
        return {
            "error": "Not Found",
            "message": "La ciudad no existe",
            "status_code": status_code
        }
    else:
        return {
            "error": f"Error {status_code}",
            "message": "Ocurrió un error inesperado",
            "status_code": status_code
        }


@weather.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <h>
            <title>API Meteorológica</title>
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1>¡Bienvenido! ☀️</h1>
            <p>Esta API proporciona datos de temperatura de una ciudad seleccionada.</p>
            <h3>Uso del endpoint</h3>
            <p><strong>Ejemplo:</strong> http://ip:port/city_name/temp <br>Por favor, prueba estos endpoints:</p>
            <ul>
                <li><a href="/barranquilla/">/barranquilla</a> -> Introduce nombre de una ciudad: muestra datos climaticos de una ciudad especifico</li>
                <li><a href="/barranquilla/temp">/barranquilla/temp</a> -> Permite mostrar datos detallados de la temperatura</li>
            </ul>
            <p>Documentación interactiva: <a href="/static/swagger.yaml">aquí</a></p>
        </body>
    </html>
    """

@weather.get("/{city_name}")
def get_clima_info(city_name: str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&lang=es&appid=eea84b47fc6dd1d74a606382b3baad16"
    response = requests.get(url)
    
    if not response.ok:
        error_info = validacion_Errores(response.status_code)
        raise HTTPException(status_code=response.status_code, detail=error_info)
    
    try:
        dic = response.json()
        clima_info = {
            "id_city": dic["city"]["id"],
            "city_name": dic["city"]["name"],
            "country":dic["city"]["country"],
            "forecast":[]
        }

        for i in range(0, len(dic["list"])):
            
            main = dic["list"][i]["main"]
            datos_clima = {
                "temp":main["temp"],
                "feels_like":main["feels_like"],
                "temp_min":main["temp_min"],
                "temp_max":main["temp_max"],
                "pressurep":main["pressure"],
                "himidity":main["humidity"],
                "sea_level":main["sea_level"]
            }
            
            fecha = dic["list"][i]["dt_txt"]
            clima_info["forecast"].append({"clima":datos_clima, "date":fecha})
        return clima_info
    
    except (KeyError, TypeError) as e:
        raise HTTPException(status_code=500, detail={"error": "Error procesando datos", "details": str(e)})
        
    

@weather.get("/{city_name}/temp")
def get_temperatura(city_name:str):  
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&lang=es&appid=eea84b47fc6dd1d74a606382b3baad16"
    response = requests.get(url)  
    
    if not response.ok:
        error_info = validacion_Errores(response.status_code)
        raise HTTPException(status_code=response.status_code, detail=error_info)
    
    try:
        dic = response.json()
        main = dic["list"][0]["main"]
        fecha = dic["list"][0]["dt_txt"]
        return {
            "date":fecha,
            "temp":{
                "max":main["temp_max"],
                "min:":main["temp_min"],
                "media":main["temp"]
            }
        }
    except (KeyError, TypeError) as e:
        raise HTTPException(status_code=500, detail={"error": "Error procesando datos", "details": str(e)})



