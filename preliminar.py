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
#----------------Series de tiempo-------------------------------------------
st.header("Series de tiempo")


#Seleccion de los pais
paises_seleccionados = st.multiselect(
    'Cuales paises te gustaria ver?',
    list(Paises.keys()),
    ['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela','Central America','Other South America'])


#Selección de variable a graficar vs el tiempo
variables = ['(Elija una variable)','Tiempo [años]', 'Generacion total de energia  [TWh]',
       'Generacion solar [TWh]', 'Generacion eolica [TWh]',
       'Generacion geotermica-biomasa-otras [TWh]',
       'Generacion hidroelectrica [TWh]',
       'Generacion renovable sin hidroelectrica [TWh]',
       'Generacion renovable con hidroelectrica [TWh]',
       'Generacion no renovable [TWh]', 'Emisiones de CO2 [MTon]',
       'Consumo de energia primario [TWh]', 'Consumo de energia solar [TWh]',
       'Consumo de energia eolica [TWh]',
       'Consumo de energia hidroelectrica [TWh]',
       'Consumo de energia geotermica-biomasa-otras [TWh]',
       'Consumo de energia renovable sin hidroelectrica [TWh]',
       'Consumo de energia renovable con hidroelectrica [TWh]',
       'Consumo de energia no renovable [TWh]']
variable_vs_time = st.selectbox("Elige primer variable para graficar: ", variables)


#Seleccion rango de años
min_value = 1985
max_value = 2023

from_year, to_year = st.slider(
    'Cuales años te interesan?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

if variable_vs_time=='(Elija una variable)':
  st.write('Escoge una variable para poder graficar')
else:
    fig=grafico_tiempo([Paises[i] for i in paises_seleccionados], variable_vs_time, from_year,to_year,paises_seleccionados)
    st.pyplot(fig)


#---------------------------------------------------------------------------------

#---------------------------Variables correlacionadas-----------------------------
st.header("Variables correlacionadas")

#Seleccion del pais
opciones_paises = ['(Elija un pais)','Latinoamerica','Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela']
eleccion_pais = st.selectbox("Elige un pais para analizar: ", opciones_paises)

#Seleccion de variables
variable_1 = st.selectbox("Elige primer variable para graficar: ", variables, key="var1")
variable_2 = st.selectbox("Elige segunda variable para graficar: ", variables, key="var2")

if eleccion_pais=='(Elija un pais)':
   st.write('Escoge un pais para poder graficar')
elif variable_1=='(Elija una variable)' or variable_2=='(Elija una variable)':
   st.write('Escoge las dos variables a correlacionar para poder graficar')
else:
    fig=grafico_dispersion(Paises[eleccion_pais], variable_1, variable_2,eleccion_pais) 
    st.pyplot(fig)
#---------------------------------------------------------------------------------------

#-----------------------------Matriz energetica-----------------------------------------
st.header('Matriz energetica')

#Seleccion del pais
opciones_paises1 = ['(Elija un pais)','Latinoamerica','Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela']
eleccion_pais1 = st.selectbox("Elige un pais para analizar: ", opciones_paises1, key='pais2')

#Seleccion rango de años
min_value = 1985
max_value = 2023

desde, hasta = st.slider(
    'Cuales años te interesan?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value],key='años1')

if eleccion_pais1=='(Elija un pais)':
   st.write('Escoge un pais para poder graficar')
else:
  fig1=grafico_matriz_energetica_bar(Paises[eleccion_pais1],eleccion_pais,desde,hasta)
  st.pyplot(fig1)
       