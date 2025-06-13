import streamlit as st

pg = st.navigation([
    st.Page("paginaInicio.py", title="Inicio"),
    st.Page("pagina1.py", title="Energía electrica y Emisiones de C02"),
    st.Page("pagina2.py", title="Mix Eléctrico"),
    st.Page("pagina3.py", title="Proyecciones de emisiones de CO2"),
    st.Page("Codigo_prediccion.py", title="Proyecciones de generación energetica"),
])
pg.run()

