import streamlit as st
from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *

st.title("Graficas para analizar")

paises_latam=['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia',
                           'Ecuador', 'Peru', 'Venezuela','Central America',
                           'Other South America']

#Seleccion del pais
opciones_paises = ['(Elija un pais)','Latinoamerica','Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela']
eleccion_pais = st.selectbox("Elige un pais para analizar: ", opciones_paises)

#Seleccion de variables
variables = ['(Elijja una variable)','Tiempo [años]', 'Generacion total de energia  [TWh]',
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
variable_1 = st.selectbox("Elige primer variable para graficar: ", variables)
variable_2 = st.selectbox("Elige segunda variable para graficar: ", variables)


#Datos del pais seleccionado
pais=datos(eleccion_pais)

fig=grafico_dispersion(pais, variable_1, variable_2,eleccion_pais) 
st.pyplot(fig)

