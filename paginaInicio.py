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
            <div class="title-text">Diagnostico De la transición energetica y sus efectos en las emisiones de CO2 en Colombia y Latam</div>
        </div>
            """, unsafe_allow_html=True)
#st.title("Diagnostico De la transición energetica y sus efectos en las emisiones de CO2 en Colombia y Latam")
st.write()
