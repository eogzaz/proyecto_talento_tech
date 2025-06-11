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
            text-align: center;
        }
        </style>

        <div class="title-container">
            <div class="title-text">Mix de Energía eléctrica</div>
        </div>
            """, unsafe_allow_html=True)
#-----------------------------------------------------------

col1, col2, col3 =st.columns(3)
with col1:
    paises_seleccionados=st.multiselect('Seleccione los paises',list(Paises.keys()),
                                        key='pais1',
                                        placeholder="Elige un pais para analizar",
                                        default=['Colombia','Latinoamerica'], 
                                        max_selections=3,
                                        accept_new_options=True)
    
    fuentes_de_energia = {'Solar':"Generacion solar [TWh]",
                          'Eólica':"Generacion eolica [TWh]",
                          'Geotérmica/Biomasa':"Generacion geotermica-biomasa-otras [TWh]",
                          'Hidro':"Generacion hidroelectrica [TWh]",
                          'Renovables':"Generacion renovable con hidroelectrica [TWh]",
                          'Renovables sin Hidro':"Generacion renovable sin hidroelectrica [TWh]",
                          'No renovable':"Generacion no renovable [TWh]"}
 
    #Selección de rango de años
    desde_año, hasta_año = st.slider(
        'Cuales años te interesan?',
        min_value=1985,
        max_value=2023,
        value=[1985, 2023])
    
    variables_seleccionadas = st.pills('Seleccione las fuentes de generacion energetica',
                                       list(fuentes_de_energia.keys()), 
                                       selection_mode="multi",
                                       default=list(fuentes_de_energia.keys())[0:3],
                                       label_visibility="collapsed"
                                       )
    if variables_seleccionadas==[] or paises_seleccionados==[]:
        st.write('Seleciona para graficar')
    else:
        fig1=grafico_barras_agrupadas(paises_seleccionados,desde_año,hasta_año,variables_seleccionadas,Paises)
        st.pyplot(fig1)

with col2:
    #Seleccion del pais
    eleccion_pais = st.selectbox("Elige un pais para analizar: ", 
                                 list(Paises.keys()),
                                 index=None,
                                 key='pais2',
                                 placeholder="Elige un pais para analizar",
                                 label_visibility="collapsed"
                                )
    año = st.selectbox(
        "Selecciona un año para ver el mix de generación de energía:",
        options=np.arange(2023,1985,-1))

    if eleccion_pais==None:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig2=grafico_pie(Paises[eleccion_pais],eleccion_pais,año)
        st.plotly_chart(fig2)


