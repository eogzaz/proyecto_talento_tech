import streamlit as st


def paginaInicio():
    st.set_page_config(layout="wide")
    st.title("Diagnostico De la transición energetica y sus efectos en las emisiones de CO2 en Colombia y Latam")
    st.write()
    
pg = st.navigation([
    st.Page(paginaInicio, title="Inicio"),
    st.Page("pagina1.py", title="Energía electrica y Emisiones de C02"),
    st.Page("pagina2.py", title="Mix Eléctrico"),
    st.Page("pagina3.py", title="Predicciones")
])
pg.run()
