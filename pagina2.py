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
paises_seleccionados=st.sidebar.multiselect('Seleccione los paises',list(Paises.keys()),
                                        key='pais1',
                                        placeholder="Elige un pais para analizar",
                                        default=['Colombia','Latinoamerica'], 
                                        max_selections=2,
                                        accept_new_options=True)
    
fuentes_de_energia = {'Solar':"Generacion solar [TWh]",
                          'Eólica':"Generacion eolica [TWh]",
                          'Geotérmica y Biomasa':"Generacion geotermica-biomasa-otras [TWh]",
                          'Hidro':"Generacion hidroelectrica [TWh]",
                          'Renovables':"Generacion renovable con hidroelectrica [TWh]",
                          'Renovables sin Hidro':"Generacion renovable sin hidroelectrica [TWh]",
                          'No renovable':"Generacion no renovable [TWh]"}
 
    #Selección de rango de años
desde_año, hasta_año = st.sidebar.slider(
        'Cuales años te interesan?',
        min_value=1985,
        max_value=2023,
        value=[1985, 2023])
    
variables_seleccionadas = st.sidebar.pills('Seleccione las fuentes de generacion energetica',
                                       list(fuentes_de_energia.keys()), 
                                       selection_mode="multi",
                                       default=['Hidro','Renovables sin Hidro','No renovables'],
                                       label_visibility="collapsed"
                                       )


st.write('''
         Se tiene que tanto en Colombia como América Latina presentan un claro potencial de transformación hacia una matriz energética más diversificada y sostenible. 
         Históricamente, la energía hidroeléctrica ha sido la base de la generación renovable en ambas regiones. Sin embargo, la creciente preocupación por 
         la fiabilidad de la hidroeléctrica, debido a factores como el cambio climático y la variabilidad hídrica, impulsa la necesidad de adoptar otras fuentes 
         de energía.Los datos revelan un crecimiento significativo, aunque reciente, en la generación de energía eólica y solar. 
         Esto indica que estas fuentes están ganando impulso y demostrando su capacidad para complementar y eventualmente reducir la dependencia de la energía 
         hidroeléctrica. 
         ''')

col1, col2 =st.columns([1,1])

with col1: 
    if  paises_seleccionados==[]:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig1=grafico_tiempo(Paises[paises_seleccionados[0]],["Generacion total de energia  [TWh]"]+variables_seleccionadas,desde_año,hasta_año,paises_seleccionados[0])
        st.pyplot(fig1)
        fig2=grafico_matriz_energetica_bar(Paises[paises_seleccionados[0]],paises_seleccionados[0],desde_año,hasta_año)
        st.pyplot(fig2)
    
with col2:
    if  paises_seleccionados==[] or paises_seleccionados[1]==None:
        st.write('(Escoge un pais para poder graficar)')
    else:
        fig3=grafico_tiempo(Paises[paises_seleccionados[1]],["Generacion total de energia  [TWh]"]+variables_seleccionadas,desde_año,hasta_año,paises_seleccionados[1])
        st.pyplot(fig3)
        fig4=grafico_matriz_energetica_bar(Paises[paises_seleccionados[1]],paises_seleccionados[1],desde_año,hasta_año)
        st.pyplot(fig4)

st.write('''
         Tanto en Colombia como en Latinoamérica la generación total de energía ha aumentado sostenidamente desde 1985, 
         pero con diferencias en la composición de las fuentes. En Colombia, la generación sigue dominada por la hidroeléctrica, 
         con un crecimiento lento de otras renovables a partir de 2015. En cambio, en Latinoamérica, aunque la hidroeléctrica también es importante, 
         se observa una mayor diversificación con un aumento notable de las energías renovables no hidráulicas desde 2010. Esto indica que la región 
         avanza más rápido hacia una matriz energética más diversificada y sostenible que Colombia.
         ''')



if variables_seleccionadas==[] or paises_seleccionados==[]:
    st.write('Seleciona para graficar')
else:
    fig1=grafico_barras_agrupadas(paises_seleccionados,desde_año,hasta_año,variables_seleccionadas,Paises)
    st.pyplot(fig1)



st.write('''
         La correlación entre la "Ren power (excl hydro) - TWh" y la generación solar y eólica es muy fuerte, especialmente en América Latina 
         (0.88 para solar y 0.98 para eólica), lo que destaca su contribución a la energía renovable más allá de la hidroeléctrica. En Colombia, aunque los 
         valores absolutos son menores, también se observan correlaciones positivas significativas.
         La mayor adopción de la energía solar y eólica tendrá un impacto multifacético, incluyendo una mayor seguridad energética al diversificar la matriz y 
         reducir la vulnerabilidad a eventos climáticos extremos. Además, contribuirá a la sostenibilidad ambiental al no producir emisiones de gases de efecto 
         invernadero durante su operación. También impulsará el desarrollo económico y la creación de empleo en nuevas industrias, mejorará el acceso a la energía 
         en comunidades remotas y reducirá los riesgos económicos asociados a la dependencia de una única fuente ante la variabilidad climática. En resumen, 
         la integración de la energía solar y eólica es crucial para fortalecer la seguridad energética, la sostenibilidad ambiental y el desarrollo socioeconómico 
         en la región.
         ''')
