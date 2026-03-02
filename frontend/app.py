# frontend/app.py
import streamlit as st
import requests

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Predicción de Viviendas", page_icon="🏡", layout="centered")

# Título y descripción
st.title("🏡 Predicción de Precios de Viviendas en California")
st.markdown("Ingrese las características del distrito para predecir el valor medio de la casa utilizando nuestro modelo de Machine Learning (Regresión Polinomial Grado 2).")

st.divider()

# Crear dos columnas para organizar el formulario
col1, col2 = st.columns(2)

with col1:
    medinc = st.number_input("Ingreso Medio (en decenas de miles, ej. 3.5)", value=3.50, step=0.5)
    houseage = st.number_input("Edad Media de la Casa (años)", value=20.0, step=1.0)
    averooms = st.number_input("Promedio de Habitaciones", value=5.0, step=0.5)
    avebedrms = st.number_input("Promedio de Dormitorios", value=1.0, step=0.1)

with col2:
    population = st.number_input("Población del Bloque", value=1000.0, step=50.0)
    aveoccup = st.number_input("Ocupación Promedio por Casa", value=3.0, step=0.5)
    latitude = st.number_input("Latitud", value=34.0, step=0.1)
    longitude = st.number_input("Longitud", value=-118.0, step=0.1)

st.divider()

# Botón principal para predecir
if st.button("Calcular Precio Estimado 📊", use_container_width=True):
    # 1. Empaquetar los datos tal como los espera la API
    datos_json = {
        "MedInc": medinc, 
        "HouseAge": houseage, 
        "AveRooms": averooms,
        "AveBedrms": avebedrms, 
        "Population": population, 
        "AveOccup": aveoccup,
        "Latitude": latitude, 
        "Longitude": longitude
    }
    
    # 2. Enviar los datos a la API (Puerto 8080)
    try:
        # Mostramos un mensaje de carga mientras se conecta
        with st.spinner("Calculando predicción..."):
            respuesta = requests.post("https://california-housing-ml-lyyo.onrender.com/predict", json=datos_json)_json)
        
        # 3. Mostrar el resultado
        if respuesta.status_code == 200:
            precio = respuesta.json()["precio_estimado_usd"]
            st.success(f"### 💰 Precio Estimado: ${precio:,.2f} USD")
            st.balloons()  # Animación festiva al funcionar
        else:
            st.error("Error al procesar la predicción en el servidor. Revisa los datos ingresados.")
            
    except requests.exceptions.ConnectionError:

        st.error("❌ No se pudo conectar con la API. Asegúrese de que el backend (uvicorn) esté corriendo en el puerto 8080 en su otra ventana de CMD.")
