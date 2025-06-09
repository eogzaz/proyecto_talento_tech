#---------Generación de energia y emisiones de CO2 en el tiempo-----------
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
#la otra opcion es: 
st.title(f"Evolución de la generación de energía electrica y Emisiones de CO2")

#-----------------------------

#Pendiente comentar este codigo......

col1, col_sep, col2 = st.columns([1, 0.05, 1])

with col1:
    subcol1,subcol2,subcol3=st.columns([2.2, .9, 3])
    with subcol1:
        eleccion_pais1 = st.selectbox("Elige un pais para analizar: ", 
                                      list(Paises.keys()),
                                      index=None,
                                      key='pais1',
                                      placeholder="Elige un pais para analizar",
                                      label_visibility="collapsed"
                                      )
        
    with subcol2:
        st.write('Rango de años:')
    with subcol3:
        desde_año1, hasta_año1 = st.slider('Cuales años te interesan?',
                                         min_value=1985,
                                         max_value=2023,
                                         value=[1985, 2023],
                                         key='anios1',
                                         label_visibility="collapsed"
                                        )
        
    if eleccion_pais1==None:
        st.write('(Escoge un pais o región para poder graficar)')
    else:
        st.header(f"{eleccion_pais1}",divider=True)
        mostrar_kpis_generacion(Paises[eleccion_pais1],hasta_año1)
        fig1=grafico_generacion_y_emision_go(Paises[eleccion_pais1],eleccion_pais1,desde_año1,hasta_año1)
        st.plotly_chart(fig1,key='grafica1')

with col_sep:
    st.markdown("<div style='height: 700px; border-left: 0.5px solid #ccc;'></div>", unsafe_allow_html=True)

with col2:
    subcol1,subcol2,subcol3=st.columns([2.2, .9, 3])
    with subcol1:
        eleccion_pais2 = st.selectbox("Elige un pais para analizar: ", 
                                      list(Paises.keys()),
                                      index=None,
                                      key='pais2',
                                      placeholder="Elige un pais para analizar",
                                      label_visibility="collapsed"
                                      )
        
    with subcol2:
        st.write('Rango de años:')
    with subcol3:
        desde_año2, hasta_año2 = st.slider('Cuales años te interesan?',
                                         min_value=1985,
                                         max_value=2023,
                                         value=[1985, 2023],
                                         key='anios2',
                                         label_visibility="collapsed"
                                        )

    if eleccion_pais2==None:
        st.write('(Escoge un pais o región para poder graficar)')
    else:
        st.header(f"{eleccion_pais2}",divider=True) 
        mostrar_kpis_generacion(Paises[eleccion_pais2],hasta_año2)
        fig2=grafico_generacion_y_emision_go(Paises[eleccion_pais2],eleccion_pais2,desde_año2,hasta_año2)
        st.plotly_chart(fig2, key='grafica2')
        

