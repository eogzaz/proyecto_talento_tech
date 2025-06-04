import streamlit as st
import json
from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *

#------------------------DATOS-------------------------------------

with open('data.json', 'r') as f:
  Paises_from_json = json.load(f)

Paises = {key: pd.DataFrame(data) for key, data in Paises_from_json.items()}

#-----------------------------------------------------------------------

# ---------- Configuración de la página y estilo del gráfico -----------
st.set_page_config(
    page_title="Dashboard Proyecto TalentoTech",
    layout="wide"
)

# ------------------- Barra Lateral de Controles (Sidebar) -----------------
st.sidebar.header("Filtros")

#Seleccion del pais
opciones_paises = ['(Elija un pais)','Latinoamerica','Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela']
eleccion_pais = st.sidebar.selectbox("Elige un pais para analizar: ", opciones_paises)

#Selección de rango de años
#Seleccion rango de años
min_value = 1985
max_value = 2023
desde_año, hasta_año = st.sidebar.slider(
    'Cuales años te interesan?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

#------------------------------------------------------------------------
#---------Generación de energia y emisiones de CO2 en el tiempo-----------
st.title(f"Análisis de generacion Energía y Emisiones de CO2 para {eleccion_pais}")

if eleccion_pais=='(Elija un pais)':
   st.write('(Escoge un pais para poder graficar)')
else:
  fig1=grafico_generacion_y_emision(Paises[eleccion_pais],eleccion_pais,desde_año,hasta_año)
  st.pyplot(fig1)


# --- ----------------Análisis Detallado por Año ----------------------------
st.title('Matriz energetica')

# Selector para el año específico
año = st.selectbox(
    "Selecciona un año para ver la matriz energetica:",
    options=np.arange(hasta_año,desde_año,-1))

if eleccion_pais=='(Elija un pais)':
   st.write('(Escoge un pais para poder graficar)')
else:
  fig2=grafico_pie(Paises[eleccion_pais],eleccion_pais,año)
  st.plotly_chart(fig2)
#---------------------------------------------------------------------------
if eleccion_pais=='(Elija un pais)':
   st.write('Escoge un pais para poder graficar')
else:
  fig3=grafico_matriz_energetica(Paises[eleccion_pais],eleccion_pais,desde_año,hasta_año)
  st.pyplot(fig3)
