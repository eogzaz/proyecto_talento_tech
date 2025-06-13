import streamlit as st

st.set_page_config(layout="wide")

# Título principal centrado
st.markdown("""
    <style>
    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        margin-top: -40px;
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    }
    </style>

    <div class="title-container">
        <div class="title-text">Diagnóstico de la Transición Energética y sus Efectos en las Emisiones de CO₂ en Colombia y LATAM</div>
    </div>
    <div class="parrafo">
            <p>Este trabajo aborda el impacto de la transición energética eléctrica en las emisiones de CO₂ 
            en Colombia, con un enfoque hacia fuentes de energía renovable. Se analiza cómo el país,
            históricamente dependiente de la generación hídrica, enfrenta retos relacionados con la variabilidad 
            climática y la necesidad de diversificación energética. 
            El estudio diagnostica y proyecta el cumplimiento de los avances normativos y la importancia de integrar 
            fuentes renovables —como solar, eólica, geotérmica y biomasa— para lograr un sistema más sostenible, 
            resiliente y alineado con los Objetivos de Desarrollo Sostenible, 
            especialmente el ODS 7 y el ODS 13.</p>   
    </div>
    """, unsafe_allow_html=True)
col1, col2=st.columns(2)

with col1:
    st.markdown("""
        <style>      
        .menu-section {
            margin-top: 30px;
            padding: 20px;
            border-radius: 10px;
        }
        .menu-section a {
            font-size: 18px;
            display: block;
            margin-bottom: 10px;
            color: #0066cc;
            text-decoration: none;
        }
        .menu-section a:hover {
            text-decoration: underline;
        }
        </style>
        <div class="menu-section">
            <h3>📑 Contenido del Dashboard</h3>
            <a href="./pagina1" target="_self">⚡ Energía Eléctrica y Emisiones de CO₂</a>
            <a href="./pagina2" target="_self">📊 Mix Eléctrico</a>
            <a href="./pagina3" target="_self">📈 Proyecciones de Emisiones</a>
            <a href="./Codigo_prediccion" target="_self">📈 Proyecciones de generación energetica electrica</a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Imagen decorativa 
    st.image('imagen1.jpeg')
