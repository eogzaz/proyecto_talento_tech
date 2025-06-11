import streamlit as st
import matplotlib.pyplot as plt
from prophet import Prophet
import pandas as pd
import os # Importar os para manejar rutas de archivos

# --- Carga de Datos ---
file_path = './Correlacióndata_TWh.xlsx' # Asegúrate de que este archivo esté en el mismo directorio

@st.cache_data # Cargar datos solo una vez
def load_data(file_path):
    try:
        df_latam = pd.read_excel(file_path, sheet_name='Latinoamerica')
        df_colombia = pd.read_excel(file_path, sheet_name='Colombia')

        # Convertir 'Fecha' a datetime si es necesario
        if not pd.api.types.is_datetime64_any_dtype(df_latam['Fecha']):
            df_latam['Fecha'] = pd.to_datetime(df_latam['Fecha'])
        if not pd.api.types.is_datetime64_any_dtype(df_colombia['Fecha']):
            df_colombia['Fecha'] = pd.to_datetime(df_colombia['Fecha'])

        # Handle missing values
        if df_latam['Total'].isnull().any():
            df_latam['Total'] = df_latam['Total'].fillna(method='ffill')
        if df_colombia['Colombia'].isnull().any():
            df_colombia['Colombia'] = df_colombia['Colombia'].fillna(method='ffill')

        # Reshape dataframes from long to wide format
        df_latam_wide = df_latam.pivot(index='Fecha', columns='data_source', values='Total').fillna(0)
        df_colombia_wide = df_colombia.pivot(index='Fecha', columns='data_source', values='Colombia').fillna(0)

        # Ensure all energy values are numeric
        for col in df_latam_wide.columns:
            df_latam_wide[col] = pd.to_numeric(df_latam_wide[col], errors='coerce')
        for col in df_colombia_wide.columns:
            df_colombia_wide[col] = pd.to_numeric(df_colombia_wide[col], errors='coerce')

        return df_latam_wide, df_colombia_wide

    except FileNotFoundError:
        st.error(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None, None
    except Exception as e:
        st.error(f"Ocurrió un error al cargar o procesar los datos: {e}")
        return None, None

df_latam_wide, df_colombia_wide = load_data(file_path)

# --- Función prophet_forecast (copiada de tu cuaderno) ---
def prophet_forecast(df, column, periods):
    try:
        df_prophet = pd.DataFrame({'ds': df.index, 'y': df[column]})
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
        df_prophet['y'] = pd.to_numeric(df_prophet['y'], errors='coerce').fillna(0)

        model = Prophet(yearly_seasonality=True)
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=periods, freq='Y')
        forecast = model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    except Exception as e:
        st.error(f"Error durante Prophet forecasting para {column}: {e}")
        return None

# --- Lógica de Streamlit ---
st.title("Proyecciones de Generación de Energía")

if df_latam_wide is not None and df_colombia_wide is not None:
    # Determinar el último año en los datos
    last_date_latam = df_latam_wide.index.max()
    last_date_colombia = df_colombia_wide.index.max()
    forecast_end_year = 2030

    periods_to_forecast_latam = forecast_end_year - last_date_latam.year
    periods_to_forecast_colombia = forecast_end_year - last_date_colombia.year

    # Asegurarse de que el número de periodos sea al menos 1
    periods_to_forecast_latam = max(periods_to_forecast_latam, 1)
    periods_to_forecast_colombia = max(periods_to_forecast_colombia, 1)

    # Selección de región
    region = st.selectbox("Selecciona la región:", ["Latinoamérica", "Colombia"])

    if region == "Latinoamérica":
        df_selected = df_latam_wide
        periods_to_forecast = periods_to_forecast_latam
        st.subheader("Proyecciones para Latinoamérica")
    else:
        df_selected = df_colombia_wide
        periods_to_forecast = periods_to_forecast_colombia
        st.subheader("Proyecciones para Colombia")

    # Selección de fuente de energía
    # Obtener las columnas numéricas que no son de tiempo o features
    available_columns = [col for col in df_selected.columns if col not in ['year', 'month', 'quarter'] and not col.startswith(('lag_', 'rolling_mean_'))]
    energy_source = st.selectbox("Selecciona la fuente de energía:", available_columns)


    if energy_source in df_selected.columns:
        st.write(f"Mostrando proyección para: **{energy_source}**")

        # Generar el forecast
        forecast_result = prophet_forecast(df_selected, energy_source, periods_to_forecast)

        if forecast_result is not None:
            # Visualizar el forecast
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df_selected.index, df_selected[energy_source], label='Datos Históricos')
            ax.plot(forecast_result['ds'], forecast_result['yhat'], label='Proyección (Prophet)', color='orange')
            ax.fill_between(forecast_result['ds'], forecast_result['yhat_lower'], forecast_result['yhat_upper'], color='orange', alpha=0.2, label='Intervalo de Confianza')
            ax.set_title(f'Proyección de Generación de Energía para {energy_source} en {region}')
            ax.set_xlabel('Año')
            ax.set_ylabel('TWh')
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)
        else:
            st.warning("No se pudo generar la proyección para esta fuente de energía.")

    else:
        st.warning("Fuente de energía no encontrada o no seleccionable.")

else:
    st.error("No se pudieron cargar los datos. Por favor, verifica la ruta del archivo y el contenido.")
