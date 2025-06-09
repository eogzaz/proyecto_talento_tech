import streamlit as st


def paginaInicio():
    st.set_page_config(layout="wide")
    st.title("Página de inicio")

pg = st.navigation([
    st.Page(paginaInicio, title="Inicio"),
    st.Page("pagina1.py", title="Energía electrica y Emisiones de C02"),
    st.Page("pagina2.py", title="Mix Eléctrico"),
    st.Page("pagina3.py", title="Predicciones")
])
pg.run()