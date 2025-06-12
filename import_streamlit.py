import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *



def plot_energy_data(dfs_paises, pais, fuente_energia, start_year, end_year, fit_model='linear'):
    if pais not in dfs_paises:
        st.warning(f"País '{pais}' no encontrado en los datos.")
        return

    df_pais = dfs_paises[pais].copy()

    if fuente_energia not in df_pais.columns:
        st.warning(f"Fuente de energía '{fuente_energia}' no encontrada para el país '{pais}'.")
        return

    # Calculate the percentage of the selected energy source relative to the total generation
    # Handle division by zero if 'Generacion total de energia  [TWh]' is 0
    df_pais['Porcentaje'] = (df_pais[fuente_energia] / df_pais['Generacion total de energia  [TWh]']) * 100
    df_pais['Porcentaje'] = df_pais['Porcentaje'].replace([np.inf, -np.inf], np.nan) # Replace inf with NaN


    # Filter by year range
    df_filtered = df_pais[(df_pais['Tiempo [años]'] >= start_year) & (df_pais['Tiempo [años]'] <= end_year)].copy()

    # Convert explicitly to numeric type and remove non-finite values
    df_filtered['Tiempo [años]'] = pd.to_numeric(df_filtered['Tiempo [años]'], errors='coerce')
    df_filtered['Porcentaje'] = pd.to_numeric(df_filtered['Porcentaje'], errors='coerce')
    df_filtered.dropna(subset=['Tiempo [años]', 'Porcentaje'], inplace=True)

    if df_filtered.empty:
        st.info(f"No hay datos disponibles para el país '{pais}', fuente '{fuente_energia}' en el rango de años {start_year}-{end_year}.")
        return

    # Create the plot using matplotlib
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.fill_between(df_filtered['Tiempo [años]'], df_filtered['Porcentaje'], color="skyblue", alpha=0.4)
    ax.plot(df_filtered['Tiempo [años]'], df_filtered['Porcentaje'], color="Slateblue", alpha=0.6, linewidth=2)

    # Fit with statsmodels
    # Only attempt to fit the line if there are enough data points (at least 2 for linear, 3 for quadratic)
    if fit_model == 'linear' and len(df_filtered) >= 2:
        X = df_filtered['Tiempo [años]']
        y = df_filtered['Porcentaje']
        X = sm.add_constant(X) # Add constant for the intercept
        model = sm.OLS(y, X).fit()

        # Create exog for prediction
        predict_years = np.arange(start_year, 2050, 1) # Extend prediction up to 2050
        predict_exog = sm.add_constant(predict_years)

        ax.plot(predict_years, model.predict(predict_exog), "r--", label=f'Ajuste Lineal\n(Coef: {model.params[1]:.2f}, Intercepto: {model.params[0]:.2f}, R²: {model.rsquared:.2f})')
        # print(model.summary()) # Optional: print the model summary

    elif fit_model == 'quadratic' and len(df_filtered) >= 3:
        df_filtered['Tiempo_sq'] = df_filtered['Tiempo [años]']**2
        X = df_filtered[['Tiempo [años]', 'Tiempo_sq']]
        y = df_filtered['Porcentaje']
        X = sm.add_constant(X) # Add constant for the intercept
        model = sm.OLS(y, X).fit()

        # Create exog for prediction with quadratic term
        predict_years = np.arange(start_year, 2050, 1) # Extend prediction up to 2050
        predict_exog = pd.DataFrame({
            'Tiempo [años]': predict_years,
            'Tiempo_sq': predict_years**2
        })
        predict_exog = sm.add_constant(predict_exog)

        ax.plot(predict_years, model.predict(predict_exog), "r--", label=f'Ajuste Cuadrático\n(Coef_lin: {model.params[1]:.2f}, Coef_quad: {model.params[2]:.4f}, Intercepto: {model.params[0]:.2f}, R²: {model.rsquared:.2f})')
        # print(model.summary()) # Optional: print the model summary

    elif fit_model not in ['linear', 'quadratic']:
        st.warning(f"Modelo de ajuste '{fit_model}' no soportado. Use 'linear' o 'quadratic'.")


    ax.set_xlabel('Año')
    ax.set_ylabel('Porcentaje (%)')
    ax.set_title(f'Porcentaje de {fuente_energia} en {pais} ({start_year}-{end_year})')
    ax.grid(True)
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)
    plt.close(fig) # Close the figure to free memory


# --- Load Data ---
Datos = Cargar_Datos()
paises_latam=['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela','Central America','Other South America','Total World']
Paises={}
for i in paises_latam:
  Paises[i]=df_variables(Datos,i)
Paises['Latinoamerica']=dataframe_latam(Datos,paises_latam)

# --- Streamlit App ---
st.set_page_config(layout="wide")
st.title("Análisis comparativo de emisiones de CO₂ por generación eléctrica")
st.subheader("Colombia y América Latina (2010-2030)")

st.write("""
Esta aplicación permite explorar los datos históricos y proyectar las emisiones de CO₂
asociadas a la generación eléctrica por fuente en Colombia y otros países de América Latina.
""")

# --- Section 1: Exploratory Analysis ---
st.header("Análisis Exploratorio por País y Fuente de Energía")

available_countries = list(Paises.keys())
available_energy_sources = [
    'Generacion total de energia  [TWh]',
    'Generacion solar [TWh]',
    'Generacion eolica [TWh]',
    'Generacion geotermica-biomasa-otras [TWh]',
    'Generacion hidroelectrica [TWh]',
    'Generacion renovable con hidroelectrica [TWh]',
    'Generacion renovable sin hidroelectrica [TWh]',
    'Generacion no renovable [TWh]',
    'Emisiones de CO2 [MTon]',
    'Consumo de energia primario [TWh]',
    'Consumo de energia solar [TWh]',
    'Consumo de energia eolica [TWh]',
    'Consumo de energia hidroelectrica [TWh]',
    'Consumo de energia geotermica-biomasa-otras [TWh]',
    'Consumo de energia renovable con hidroelectrica [TWh]',
    'Consumo de energia renovable sin hidroelectrica [TWh]',
    'Consumo de energia no renovable [TWh]'
]
available_fit_models = ['linear', 'quadratic']

col1, col2 = st.columns(2)

with col1:
    selected_country = st.selectbox("Seleccione un país", available_countries)

with col2:
    selected_source = st.selectbox("Seleccione una fuente de energía", available_energy_sources)

col3, col4, col5 = st.columns(3)
with col3:
    # Get available years from the selected country's data
    if selected_country in Paises and 'Tiempo [años]' in Paises[selected_country].columns:
         min_year = int(Paises[selected_country]['Tiempo [años]'].min())
         max_year = int(Paises[selected_country]['Tiempo [años]'].max())
    else:
         min_year = 1985 # Default if data is not available
         max_year = 2023 # Default if data is not available


    start_year = st.slider("Año de inicio", min_year, max_year, min_year)

with col4:
    end_year = st.slider("Año de fin", min_year, max_year, max_year)

with col5:
    selected_fit_model = st.selectbox("Modelo de ajuste", available_fit_models)

if st.button("Generar Gráfico de Análisis Exploratorio"):
    plot_energy_data(Paises, selected_country, selected_source, start_year, end_year, selected_fit_model)


# --- Section 2: CO2 Projection for Colombia ---
st.header("Proyección de Emisiones de CO₂ para Colombia")

st.write("Proyección lineal de las emisiones de CO₂ para Colombia hasta 2030, comparada con la meta nacional.")

# CO2 Emission Projection for Colombia
if "Colombia" in Paises:
    df_colombia = Paises["Colombia"].copy()
    df_colombia["Tiempo [años]"] = pd.to_numeric(df_colombia["Tiempo [años]"], errors='coerce')
    df_colombia["Emisiones de CO2 [MTon]"] = pd.to_numeric(df_colombia["Emisiones de CO2 [MTon]"], errors='coerce')
    df_colombia.dropna(subset=["Tiempo [años]", "Emisiones de CO2 [MTon]"], inplace=True)

    # Ensure data for regression starts from 2000 onwards (as in the original code context)
    df_regression = df_colombia[df_colombia["Tiempo [años]"] >= 2000].copy() # Assuming 2000 was the intended start for regression

    if len(df_regression) < 2:
         st.error("Error: No hay suficientes datos válidos a partir del año 2000 para realizar la regresión lineal para Colombia.")
    else:
        X = df_regression[["Tiempo [años]"]]
        y = df_regression["Emisiones de CO2 [MTon]"]

        modelo = LinearRegression()
        modelo.fit(X, y)

        # Project to 2030
        proyeccion_2030 = modelo.predict(np.array([[2030]]))[0]
        st.write(f"Proyección de emisiones de CO₂ en 2030 para Colombia: **{proyeccion_2030:.2f} Mt**")

        # Meta oficial para el sector eléctrico en Colombia en 2030 (puedes cambiar a 59 o 75 si prefieres un límite exacto)
        meta_2030 = 67  # Mt CO₂

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_colombia["Tiempo [años]"], df_colombia["Emisiones de CO2 [MTon]"], label="Histórico")
        ax.scatter([2030], [proyeccion_2030], color='red', zorder=5, label="Proyección 2030") # Use zorder to ensure scatter point is visible
        ax.axhline(y=meta_2030, color='green', linestyle='--', label=f"Meta 2030 ({meta_2030:.2f} Mt)")
        ax.set_xlabel("Año")
        ax.set_ylabel("Emisiones CO₂ (Mt)")
        ax.set_title("Emisiones de CO₂ Colombia: Histórico, Proyección y Meta 2030")
        ax.axhline(y=59, color='orange', linestyle=':', label="Meta mínima (59 Mt)")
        ax.axhline(y=75, color='blue', linestyle=':', label="Meta máxima (75 Mt)")

        ax.legend()
        ax.grid(True)

        # Display the plot
        st.pyplot(fig)
        plt.close(fig) # Close the figure to free memory

        if proyeccion_2030 <= meta_2030:
            st.success("La proyección actual indica que Colombia está en camino de cumplir la meta de reducción de emisiones de CO₂ en el sector eléctrico para 2030.")
        else:
            st.warning("La proyección actual indica que Colombia podría no alcanzar la meta de reducción de emisiones de CO₂ en el sector eléctrico para 2030 si la tendencia continúa.")

else:
    st.error("Los datos para Colombia no están disponibles.")


# --- Section 3: Data Table (Optional) ---
st.header("Tabla de Datos (Ejemplo)")
st.write("Visualización de una muestra de los datos.")

# You can choose to display a specific dataframe or a combined one
# For simplicity, let's show the data for the selected country in the exploratory section
if selected_country in Paises:
    st.dataframe(Paises[selected_country].head())
else:
    st.info("Seleccione un país para ver una muestra de los datos.")

# --- Section 4: Methodology and Source ---
st.header("Metodología y Fuente de Datos")
st.write("""
El análisis se basa en datos históricos de emisiones de CO₂ y generación eléctrica por fuente
del Energy Institute Statistical Review of World Energy (https://www.energyinst.org/statistical-review).

Se utiliza un modelo de regresión lineal para proyectar las emisiones de CO₂ para Colombia hasta 2030
basado en la tendencia histórica (datos a partir del año 2000).
""")

# --- About Section (Optional) ---
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Esta aplicación fue creada para visualizar y analizar las tendencias de emisiones de CO₂ "
    "en el sector eléctrico de Colombia y América Latina."
)
