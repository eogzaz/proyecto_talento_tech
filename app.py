import streamlit as st
from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *

#------------------Variables importantes--------------------
paises_latam=['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela','Central America','Other South America']

#-------------------------------------------------------------

#------------------Carga de los datos-----------------------
Datos = Cargar_Datos()

Paises={}
for i in paises_latam:
  Paises[i]=df_variables(Datos,i)
Paises['Latinoamerica']=dataframe_latam(Datos,paises_latam)
#-----------------------------------------------------------


#----------------Codigo streamlit-----------------------------
st.title("Variables en el tiempo")


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
       'Generacion renovable incluyendo hidroelectrica [TWh]',
       'Generacion no renovable [TWh]', 'Emisiones de CO2 [MTon]',
       'Comsumo de energia primario [TWh]', 'Comsumo de energia solar [TWh]',
       'Comsumo de energia eolica [TWh]',
       'Comsumo de energia hidroelectrica [TWh]',
       'Comsumo de energia geotermica-biomasa-otras [TWh]',
       'Comsumo de energia renovable incluyendo hidroelectrica [TWh]',
       'Comsumo de energia no renovable [TWh]']
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

