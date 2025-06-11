import streamlit as st

pg = st.navigation([
    st.Page("paginaInicio.py", title="Inicio"),
    st.Page("pagina1.py", title="Energía electrica y Emisiones de C02"),
    st.Page("pagina2.py", title="Mix Eléctrico"),
    st.Page("streamlit.py", title="Predicciones")
])
pg.run()
