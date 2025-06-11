import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import seaborn as sns # Aunque no se usa directamente en el código de Streamlit, se importa en el notebook original

# Se asume que las funciones Cargar_Datos, df_variables, dataframe_latam y la carga inicial de Paises
# se ejecutarán para crear el diccionario 'Paises' antes de que Streamlit intente usarlo.
# En un entorno de Streamlit independiente, estas funciones deberían estar definidas en el mismo script
# o importadas desde otro archivo Python.
# Para esta respuesta, vamos a suponer que el diccionario `Paises` ya existe y está cargado.
# Si estás ejecutando esto como un script independiente de Streamlit, necesitarás incluir la carga de datos.

# Ejemplo de carga de datos si fuera un script independiente (descomentar y adaptar si es necesario)
# def obtencion_dataframes(...):
#     ... tu código ...
# def exajoules_to_twh(...):
#     ... tu código ...
# def Cargar_Datos():
#     ... tu código ...
# def df_variables(...):
#     ... tu código ...
# def dataframe_latam(...):
#     ... tu código ...
# Datos = Cargar_Datos()
# paises_latam=['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela','Central America','Other South America','Total World']
# Paises={}
# for i in paises_latam:
#   Paises[i]=df_variables(Datos,i)
# Paises['Latinoamerica']=dataframe_latam(Datos,paises_latam)

# --- Funciones para la App de Streamlit ---

def plot_energy_data_streamlit(dfs_paises, pais, fuente_energia, start_year, end_year, fit_model='linear'):
    """
    Genera un gráfico del porcentaje de una fuente de energía específica para un país
    dentro de un rango de años, con ajuste usando statsmodels, compatible con Streamlit.

    Args:
        dfs_paises (dict): Diccionario donde las claves son nombres de países
                           y los valores son DataFrames con los datos de energía.
        pais (str): El nombre del país a graficar.
        fuente_energia (str): La columna del DataFrame a graficar
                              (ej. 'Generacion renovable con hidroelectrica [TWh]').
        start_year (int): Año de inicio del rango a graficar.
        end_year (int): Año de fin del rango a graficar.
        fit_model (str): Tipo de modelo de ajuste ('linear', 'quadratic').

    Returns:
        matplotlib.figure.Figure: La figura de Matplotlib.
    """
    if pais not in dfs_paises:
        st.error(f"País '{pais}' no encontrado en los datos.")
        return None

    df_pais = dfs_paises[pais].copy()

    if fuente_energia not in df_pais.columns:
        st.error(f"Fuente de energía '{fuente_energia}' no encontrada para el país '{pais}'.")
        return None

    # Calcular el porcentaje de la fuente de energía seleccionada respecto al total
    # Manejar la división por cero si 'Generacion total de energia  [TWh]' es 0
    df_pais['Porcentaje'] = (df_pais[fuente_energia] / df_pais['Generacion total de energia  [TWh]']) * 100
    df_pais['Porcentaje'] = df_pais['Porcentaje'].replace([np.inf, -np.inf], np.nan) # Reemplazar inf con NaN


    # Filtrar por rango de años
    df_filtered = df_pais[(df_pais['Tiempo [años]'] >= start_year) & (df_pais['Tiempo [años]'] <= end_year)].copy()

    # Convertir explícitamente a tipo numérico y eliminar valores no finitos
    df_filtered['Tiempo [años]'] = pd.to_numeric(df_filtered['Tiempo [años]'], errors='coerce')
    df_filtered['Porcentaje'] = pd.to_numeric(df_filtered['Porcentaje'], errors='coerce')
    df_filtered.dropna(subset=['Tiempo [años]', 'Porcentaje'], inplace=True)

    if df_filtered.empty:
        st.warning(f"No hay datos disponibles para el país '{pais}', fuente '{fuente_energia}' en el rango de años {start_year}-{end_year}.")
        return None

    # Crear la figura de Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.fill_between(df_filtered['Tiempo [años]'], df_filtered['Porcentaje'], color="skyblue", alpha=0.4)
    ax.plot(df_filtered['Tiempo [años]'], df_filtered['Porcentaje'], color="Slateblue", alpha=0.6, linewidth=2)

    # Ajuste con statsmodels
    # Solo intentar ajustar la línea si hay suficientes puntos de datos (al menos 2 para lineal, 3 for quadratic)
    if fit_model == 'linear' and len(df_filtered) >= 2:
        X = df_filtered['Tiempo [años]']
        y = df_filtered['Porcentaje']
        X = sm.add_constant(X) # Añadir constante para el intercepto
        try:
            model = sm.OLS(y, X).fit()
             # Crear exog para predicción
            predict_years = np.arange(start_year, 2050, 1) # Extender predicción hasta 2050
            predict_exog = sm.add_constant(predict_years)
            ax.plot(predict_years, model.predict(predict_exog), "r--", label=f'Ajuste Lineal\n(Coef: {model.params[1]:.2f}, Intercepto: {model.params[0]:.2f}, R²: {model.rsquared:.2f})')
        except ValueError:
            st.warning("No se pudo ajustar el modelo lineal. Puede que los datos sean constantes o insuficientes.")


    elif fit_model == 'quadratic' and len(df_filtered) >= 3:
        df_filtered['Tiempo_sq'] = df_filtered['Tiempo [años]']**2
        X = df_filtered[['Tiempo [años]', 'Tiempo_sq']]
        y = df_filtered['Porcentaje']
        X = sm.add_constant(X) # Añadir constante para el intercepto
        try:
            model = sm.OLS(y, X).fit()
             # Crear exog para predicción con término cuadrático
            predict_years = np.arange(start_year, 2050, 1) # Extender predicción hasta 2050
            predict_exog = pd.DataFrame({
                'Tiempo [años]': predict_years,
                'Tiempo_sq': predict_years**2
            })
            predict_exog = sm.add_constant(predict_exog)
            ax.plot(predict_years, model.predict(predict_exog), "r--", label=f'Ajuste Cuadrático\n(Coef_lin: {model.params[1]:.2f}, Coef_quad: {model.params[2]:.4f}, Intercepto: {model.params[0]:.2f}, R²: {model.rsquared:.2f})')
        except ValueError:
             st.warning("No se pudo ajustar el modelo cuadrático. Puede que los datos sean constantes o insuficientes.")


    elif fit_model not in ['linear', 'quadratic']:
        st.warning(f"Modelo de ajuste '{fit_model}' no soportado. Use 'linear' o 'quadratic'.")

    ax.set_xlabel('Año')
    ax.set_ylabel('Porcentaje (%)')
    ax.set_title(f'Porcentaje de {fuente_energia.replace("[TWh]", "").strip()} en {pais} ({start_year}-{end_year})') # Limpiar el nombre de la fuente
    ax.grid(True)
    ax.legend()

    return fig

def plot_co2_projection_streamlit(dfs_paises, pais="Colombia"):
    """
    Genera un gráfico de emisiones de CO2 histórico y proyectado para un país,
    mostrando la meta 2030, compatible con Streamlit.

    Args:
        dfs_paises (dict): Diccionario donde las claves son nombres de países
                           y los valores son DataFrames con los datos de energía.
        pais (str): El nombre del país a graficar (por defecto "Colombia").

    Returns:
        matplotlib.figure.Figure: La figura de Matplotlib.
    """
    if pais not in dfs_paises:
        st.error(f"País '{pais}' no encontrado en los datos para la proyección de CO2.")
        return None

    df_pais = dfs_paises[pais].copy()

    # Convertir las columnas necesarias a numéricas
    df_pais["Tiempo [años]"] = pd.to_numeric(df_pais["Tiempo [años]"], errors='coerce')
    df_pais["Emisiones de CO2 [MTon]"] = pd.to_numeric(df_pais["Emisiones de CO2 [MTon]"], errors='coerce')

    # Eliminar filas con datos faltantes en las columnas clave
    df_pais = df_pais.dropna(subset=["Tiempo [años]", "Emisiones de CO2 [MTon]"])

    if len(df_pais) < 2:
        st.warning(f"No hay suficientes datos históricos para {pais} para realizar la proyección de CO2.")
        return None

    # Usar los datos históricos disponibles para el ajuste
    X = df_pais[["Tiempo [años]"]]
    y = df_pais["Emisiones de CO2 [MTon]"]

    # Entrenar el modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Crear un rango de años para la proyección (desde el último año histórico hasta 2030)
    last_hist_year = int(df_pais["Tiempo [años]"].max())
    anios_proy = np.arange(last_hist_year + 1, 2031).reshape(-1, 1) # Empezar la proyección después del último año histórico

    # Asegurarse de que predict_anios_proy tiene datos antes de predecir
    if anios_proy.size > 0:
        proy_co2 = modelo.predict(anios_proy)

        # DataFrame de proyección
        df_proy = pd.DataFrame({
            "Tiempo [años]": anios_proy.flatten(),
            "Emisiones de CO2 [MTon]": proy_co2,
            "Tipo": "Proyección"
        })
    else:
         df_proy = pd.DataFrame(columns=["Tiempo [años]", "Emisiones de CO2 [MTon]", "Tipo"])


    # DataFrame de datos reales
    df_real = df_pais[["Tiempo [años]", "Emisiones de CO2 [MTon]"]].copy()
    df_real["Tipo"] = "Histórico"

    # Juntar ambos dataframes
    df_final = pd.concat([df_real, df_proy], ignore_index=True)

    # Meta oficial para el sector eléctrico en Colombia en 2030 (puedes ajustar)
    meta_2030 = 67  # Mt CO₂

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar datos históricos y proyectados
    sns.lineplot(data=df_final, x="Tiempo [años]", y="Emisiones de CO2 [MTon]", hue="Tipo", ax=ax)

    # Agregar punto de proyección para 2030 si hay datos proyectados
    if not df_proy.empty:
        proyeccion_2030_valor = df_proy[df_proy["Tiempo [años]"] == 2030]["Emisiones de CO2 [MTon]"].iloc[0] if 2030 in df_proy["Tiempo [años"]].values else None
        if proyeccion_2030_valor is not None:
             ax.scatter([2030], [proyeccion_2030_valor], color='red', zorder=5, label="Proyección 2030")


    # Agregar línea de la meta 2030
    ax.axhline(y=meta_2030, color='green', linestyle='--', label=f"Meta 2030 ({meta_2030:.2f} Mt)")

    # Agregar metas opcionales
    ax.axhline(y=59, color='orange', linestyle=':', label="Meta mínima (59 Mt)")
    ax.axhline(y=75, color='blue', linestyle=':', label="Meta máxima (75 Mt)")


    ax.set_xlabel("Año")
    ax.set_ylabel("Emisiones CO₂ (Mt)")
    ax.set_title(f"Emisiones de CO₂ {pais}: Histórico, Proyección y Meta 2030")
    ax.grid(True)
    ax.legend()

    return fig

# --- Interfaz de Streamlit ---

st.title('Análisis Comparativo de Emisiones y Generación Eléctrica en América Latina')

st.markdown("""
Esta aplicación permite visualizar la evolución y proyección de las emisiones de CO₂
y la composición de la matriz eléctrica para diferentes países de América Latina,
utilizando datos del Energy Institute.
""")

# Secciones de la App
st.sidebar.title("Navegación")
option = st.sidebar.radio(
    "Selecciona un Análisis",
    ['Porcentaje de Energía por Fuente', 'Proyección de Emisiones de CO₂ para Colombia']
)

# Definir las fuentes de energía disponibles para selección
fuentes_energia_disponibles = [
    'Generacion total de energia  [TWh]',
    'Generacion solar [TWh]',
    'Generacion eolica [TWh]',
    'Generacion geotermica-biomasa-otras [TWh]',
    'Generacion hidroelectrica [TWh]',
    'Generacion renovable con hidroelectrica [TWh]',
    'Generacion renovable sin hidroelectrica [TWh]',
    'Generacion no renovable [TWh]',
    # 'Emisiones de CO2 [MTon]', # Esto es emisión, no generación para porcentaje
    # 'Consumo de energia primario [TWh]', # Esto es consumo
    # 'Consumo de energia solar [TWh]',
    # 'Consumo de energia eolica [TWh]',
    # 'Consumo de energia hidroelectrica [TWh]',
    # 'Consumo de energia geotermica-biomasa-otras [TWh]',
    # 'Consumo de energia renovable con hidroelectrica [TWh]',
    # 'Consumo de energia renovable sin hidroelectrica [TWh]',
    # 'Consumo de energia no renovable [TWh]'
]


if option == 'Porcentaje de Energía por Fuente':
    st.header('Porcentaje de Energía por Fuente de Generación')

    # Controles para la selección del gráfico
    paises_disponibles = list(Paises.keys())
    pais_seleccionado = st.selectbox(
        'Selecciona un País',
        paises_disponibles,
        index=paises_disponibles.index('Colombia') if 'Colombia' in paises_disponibles else 0
    )

    fuente_seleccionada = st.selectbox(
        'Selecciona la Fuente de Energía',
        fuentes_energia_disponibles,
        index=fuentes_energia_disponibles.index('Generacion renovable con hidroelectrica [TWh]') if 'Generacion renovable con hidroelectrica [TWh]' in fuentes_energia_disponibles else 0
    )

    # Rango de años disponible en los datos
    if pais_seleccionado in Paises and 'Tiempo [años]' in Paises[pais_seleccionado].columns:
        min_year = int(Paises[pais_seleccionado]['Tiempo [años]'].min())
        max_year = int(Paises[pais_seleccionado]['Tiempo [años]'].max())
    else:
        min_year = 1985 # Valores por defecto si no se cargan los datos correctamente
        max_year = 2023

    start_year, end_year = st.slider(
        'Selecciona el Rango de Años',
        min_year, max_year, (min_year, max_year)
    )

    modelo_ajuste = st.radio(
        'Selecciona el Modelo de Ajuste',
        ('linear', 'quadratic', 'none'),
        index=0
    )

    # Generar y mostrar el gráfico
    if st.button('Generar Gráfico'):
        fig = plot_energy_data_streamlit(Paises, pais_seleccionado, fuente_seleccionada, start_year, end_year, modelo_ajuste)
        if fig is not None:
            st.pyplot(fig)

elif option == 'Proyección de Emisiones de CO₂ para Colombia':
    st.header('Proyección de Emisiones de CO₂ para Colombia')
    st.markdown("""
    Este gráfico muestra la tendencia histórica de las emisiones de CO₂ asociadas
    a la generación eléctrica en Colombia y una proyección lineal hasta 2030.
    Se compara esta proyección con la meta nacional de reducción para el sector eléctrico en 2030.
    """)

    # Generar y mostrar el gráfico de proyección de CO2 para Colombia
    # No se necesitan más controles en esta sección, ya que se centra en Colombia y la proyección lineal simple
    st.write("Proyección de emisiones basada en la tendencia histórica de los datos disponibles.")

    fig_co2 = plot_co2_projection_streamlit(Paises, pais="Colombia")
    if fig_co2 is not None:
        st.pyplot(fig_co2)
    else:
         st.warning("No se pudo generar el gráfico de proyección de emisiones de CO₂ para Colombia.")