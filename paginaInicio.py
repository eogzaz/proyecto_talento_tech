import streamlit as st
st.set_page_config(layout="wide")
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
            <div class="title-text">Diagnostico De la transición energetica y sus efectos en las emisiones de  CO₂ en Colombia y Latam</div>
        </div>
        <div class="parrafo">
            <p>Este trabajo aborda el impacto de la transición energética eléctrica en las emisiones de CO₂ 
                en Colombia, con un enfoque hacia fuentes de energía renovable. Se analiza cómo el país,
                históricamente dependiente de la generación hídrica, enfrenta retos relacionados con la variabilidad 
                climática y la necesidad de diversificación energética. 
                El estudio diagnostica y proyecta el cumplimiento los avances normativos y la importancia de integrar 
                fuentes renovables,como solar, eólica, geotermica y biomasa, para lograr un sistema más sostenible, 
                resiliente y alineado con los Objetivos de Desarrollo Sostenible, 
                especialmente el ODS 7 y el ODS 13.</p>   
        </div>
            """, unsafe_allow_html=True)
st.write(imagen1.jpeg)
