# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

# Inicializar la aplicación FastAPI
app = FastAPI(title="API de Predicción - California Housing")

# --- CORRECCIÓN DE RUTAS ---
# Esto detecta automáticamente la ruta exacta de tu proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Cargar los modelos usando la ruta exacta
poly = joblib.load(os.path.join(MODEL_DIR, "poly_transform.pkl"))
modelo = joblib.load(os.path.join(MODEL_DIR, "modelo_california.pkl"))
# ---------------------------

# Definir la estructura del JSON que va a recibir la API
class CasaData(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

@app.post("/predict")
def predict_price(data: CasaData):
    # 1. Convertir los datos de entrada a un array de NumPy (1 fila, 8 columnas)
    features = np.array([[data.MedInc, data.HouseAge, data.AveRooms, 
                          data.AveBedrms, data.Population, data.AveOccup, 
                          data.Latitude, data.Longitude]])
    
    # 2. Aplicar la transformación polinomial (grado 2)
    features_poly = poly.transform(features)
    
    # 3. Hacer la predicción
    prediccion = modelo.predict(features_poly)[0]
    
    # El dataset de California tiene los precios en cientos de miles (ej: 2.5 = $250,000)
    precio_real = prediccion * 100000
    
    # Retornar el resultado en formato JSON
    return {"precio_estimado_usd": round(precio_real, 2)}