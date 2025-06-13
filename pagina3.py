#librerias
import streamlit as st
import json
from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *

#------------------------DATOS-------------------------------------
with open('data.json', 'r') as f:
  Paises_from_json = json.load(f)

Paises = {key: pd.DataFrame(data) for key, data in Paises_from_json.items()}
#---------------------------------------------------------------------
# --- Streamlit App ---
st.set_page_config(layout="wide")
st.title("Análisis comparativo de emisiones de CO₂")

st.write("""
Acá se exploran los datos históricos y proyecciones de las emisiones de CO₂
asociadas a la generación eléctrica por fuente en Colombia y Latinoamerica en general.
Aunque tambien se pueden comparar otros paises y regiones.
""")

available_countries = list(Paises.keys())


col1, col2 = st.columns(2)

with col1:
    pais1 = st.selectbox("Seleccione un país",
                        list(Paises.keys()),
                        index=3,
                        key='pais1')
    fig1=plot_co2_projection(Paises,pais1)
    st.pyplot(fig1)

with col2:
    pais2 = st.selectbox("Seleccione un país",
                        list(Paises.keys()),
                        index=20,
                        key='pais2')
    fig2=plot_co2_projection(Paises,pais2)
    st.pyplot(fig2)

if pais1=='Colombia' or pais2=='Colombia':
    st.write('''
         La proyección actual indica que Colombia podría no alcanzar la meta de reducción de emisiones de CO₂
        en el sector eléctrico para 2030 si la tendencia continúa.
        Por lo que Colombia debe  hacer esfuerzos extras para diversificar su matriz energetica y asi lograr esta meta.
        ''')

