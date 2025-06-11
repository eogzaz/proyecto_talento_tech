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

col1, col2 =st.columns(2)
with col1:
    #Seleccion del pais
    eleccion_pais = st.selectbox("Elige un pais para analizar: ", 
                                 list(Paises.keys()),
                                 index=None,
                                 key='pais2',
                                 placeholder="Elige un pais para analizar",
                                 label_visibility="collapsed"
                                )
   #Selección de rango de años
    desde_año, hasta_año = st.slider(
        'Cuales años te interesan?',
        min_value=1985,
        max_value=2023,
        value=[1985, 2023],
        key='años1')

    if eleccion_pais==None:
        st.write('(Escoge un pais para poder graficar)')
    else:
       # fig2=grafico_matriz_energetica_bar(Paises[eleccion_pais],eleccion_pais,desde_año,hasta_año)
        #st.pyplot(fig2)


  fig3=grafico_tiempo(Paises['Colombia'],1985,2023,'Colombia')
  #st.pyplot(fig3)
  
  #fig4=grafico_tiempo(Paises['Colombia'],1985,2023,'Latinoamerica')
  
  #st.pyplot(fig4)

with col2:
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



st.write('''Tanto Colombia como América Latina presentan un claro potencial de transformación hacia una matriz energética más diversificada y sostenible. Históricamente, la energía hidroeléctrica ha sido la base de la generación renovable en ambas regiones. Sin embargo, la creciente preocupación por la fiabilidad de la hidroeléctrica, debido a factores como el cambio climático y la variabilidad hídrica, impulsa la necesidad de adoptar otras fuentes de energía.
Los datos revelan un crecimiento significativo, aunque reciente, en la generación de energía eólica y solar. Esto indica que estas fuentes están ganando impulso y demostrando su capacidad para complementar y eventualmente reducir la dependencia de la energía hidroeléctrica. La correlación entre la "Ren power (excl hydro) - TWh" y la generación solar y eólica es muy fuerte, especialmente en América Latina (0.88 para solar y 0.98 para eólica), lo que destaca su contribución a la energía renovable más allá de la hidroeléctrica. En Colombia, aunque los valores absolutos son menores, también se observan correlaciones positivas significativas.
La mayor adopción de la energía solar y eólica tendrá un impacto multifacético, incluyendo una mayor seguridad energética al diversificar la matriz y reducir la vulnerabilidad a eventos climáticos extremos. Además, contribuirá a la sostenibilidad ambiental al no producir emisiones de gases de efecto invernadero durante su operación. También impulsará el desarrollo económico y la creación de empleo en nuevas industrias, mejorará el acceso a la energía en comunidades remotas y reducirá los riesgos económicos asociados a la dependencia de una única fuente ante la variabilidad climática. En resumen, la integración de la energía solar y eólica es crucial para fortalecer la seguridad energética, la sostenibilidad ambiental y el desarrollo socioeconómico en la región.''')

