#-------------------------Mix Electrico-----------------------------------
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
#-----------------------------------------------------------------
#--------------------------app----------------------------------------
st.set_page_config(layout="wide")

#Titulo, se usa st.markdown para mayor estetica,
#la otra opcion es: st.title(f"Evolución de la generación de energía electrica y Emisiones de CO2")
st.markdown("""
        <style>
        .title-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px; /* puedes reducirlo si quieres más arriba */
            margin-top: -40px; /* sube el título */
            margin-bottom: 20px;
        }
        .title-text {
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-align: center;
        }
        </style>

        <div class="title-container">
            <div class="title-text">Mix de Energía eléctrica</div>
        </div>
            """, unsafe_allow_html=True)
#--------------------------------

# ------------------- Barra Lateral de Controles (Sidebar) -----------------
st.sidebar.header("Filtros")

#Seleccion del pais
eleccion_pais = st.sidebar.selectbox("Elige un pais para analizar: ", 
                                      list(Paises.keys()),
                                      index=None,
                                      key='pais1',
                                      placeholder="Elige un pais para analizar",
                                      label_visibility="collapsed"
                                      )

#Selección de rango de años
desde_año, hasta_año = st.sidebar.slider(
    'Cuales años te interesan?',
    min_value=1985,
    max_value=2023,
    value=[1985, 2023])

# --- ----------------Análisis Detallado por Año ----------------------------

col1, col2 =st.columns(2)
with col1:
    año = st.selectbox(
        "Selecciona un año para ver el mix de generación de energía:",
        options=np.arange(hasta_año,desde_año,-1))

    if eleccion_pais==None:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig2=grafico_pie(Paises[eleccion_pais],eleccion_pais,año)
        st.plotly_chart(fig2)

with col2:
    st.write('Acá faltan KPIs')
    if eleccion_pais==None:
        st.write('Escoge un pais para poder graficar')
    else:
        fig3=grafico_mix_electrico(Paises[eleccion_pais],eleccion_pais,desde_año,hasta_año)
        st.pyplot(fig3)
