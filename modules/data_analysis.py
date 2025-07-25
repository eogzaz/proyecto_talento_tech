import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import streamlit as st

def grafico_generacion_y_emision(pais,eleccion_pais,inicio,final):
    # Crear la figura y el primer eje
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Graficar la Generación Total en el primer eje (ax1)
    color1 = 'tab:blue'
    ax1.set_xlabel('Tiempo [años]')
    ax1.set_ylabel('Generación Total [TWh]', color=color1)
    ax1.plot(pais['Tiempo [años]'], pais['Generacion total de energia  [TWh]'], color=color1, marker='o', label='Generación Total (TWh)')
    ax1.tick_params(axis='y', labelcolor=color1)

    # Crear un segundo eje que comparte el eje X
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Emisiones de CO2 [MTon]', color=color2)
    ax2.plot(pais['Tiempo [años]'], pais['Emisiones de CO2 [MTon]'], color=color2, marker='s', linestyle='--', label='Emisiones CO2 (MTon)')
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.xlim(inicio,final)
    # Añadir título y leyenda
    plt.title(f'Evolución de Generación y Emisiones en {eleccion_pais}')
    fig.tight_layout() # Ajusta el layout para que no se superpongan los elementos
    fig.legend(loc=2, bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)

    return fig


def grafico_generacion_y_emision_go(pais, eleccion_pais, inicio, final):
    # Filtrar los datos en el rango de tiempo especificado
    df_filtrado = pais[(pais['Tiempo [años]'] >= inicio) & (pais['Tiempo [años]'] <= final)]

    # Crear la figura con dos ejes Y
    fig = go.Figure()

    # Añadir trazado para Generación Total
    fig.add_trace(go.Scatter(
        x=df_filtrado['Tiempo [años]'],
        y=df_filtrado["Consumo de energia primario [TWh]"],
        name="Consumo de energia primario [TWh]",
        mode='lines+markers',
        marker=dict(symbol='circle', color='blue'),
        yaxis='y1'
    ))

    # Añadir trazado para Emisiones de CO2
    fig.add_trace(go.Scatter(
        x=df_filtrado['Tiempo [años]'],
        y=df_filtrado['Emisiones de CO2 [MTon]'],
        name='Emisiones CO2 (MTon)',
        mode='lines+markers',
        line=dict(dash='dash', color='red'),
        marker=dict(symbol='square'),
        yaxis='y2'
    ))

    # Actualizar layout para ejes dobles
    fig.update_layout(
        #title=f'Evolución de Generación y Emisiones en {eleccion_pais}',
        xaxis=dict(title='Tiempo [años]'),
        yaxis=dict(
            title='Consumo de energia primario [TWh]',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Emisiones de CO2 [MTon]',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=1.15),
        height=500,
        width=900
    )

    return fig



def mostrar_kpis_generacion(df_pais, anio: float):
    # Extraer el año deseado
    entrada = df_pais.query(f'`Tiempo [años]` == {str(anio)}')
    

    # Cálculos básicos
    ene_total = entrada["Consumo de energia primario [TWh]"].iloc[0]
    emisiones = entrada["Emisiones de CO2 [MTon]"].iloc[0]
    intensidad_carbono = emisiones /ene_total
 

    # Mostrar métricas como tarjetas
    col1, col2,col3 = st.columns([3,3,3],border=True)
    col1.metric(f"🔋 Energía primaria {anio} ", f"{ene_total:.1f} TWh")
    col2.metric(f"🏭 Emisiones CO₂ {anio}", f"{emisiones:.1f} MTon")
    col3.metric(f"⚡ Intensidad de carbono {anio}", f"{intensidad_carbono:.1f} MTon/TWh")

    # CSS para modificar el tamaño de la fuente en los KPI
    st.markdown("""
    <style>
        /* Estilo para el valor principal de la métrica */
        .st-emotion-cache-1wivap2{ /* Esta clase puede variar, verifica con el inspector de elementos */
            font-size: 1.8rem; /* Ajusta el tamaño que desees */
        }

        /* Estilo para la etiqueta de la métrica */
        .st-emotion-cache-qoz3f2 { /* Esta clase puede variar, verifica con el inspector de elementos */
            font-size: 0.85rem; /* Ajusta el tamaño que desees */
        }
    </style>
    """, unsafe_allow_html=True)


def grafico_pie(pais,eleccion_pais,año):
    # Obtener los datos del año seleccionado
    year_data = pais[pais['Tiempo [años]'] == año].iloc[0]
    # Definir las fuentes renovables y sus valores
    renewable_sources = ['Generacion solar [TWh]','Generacion eolica [TWh]','Generacion geotermica-biomasa-otras [TWh]','Generacion hidroelectrica [TWh]','Generacion no renovable [TWh]']
    values = [year_data[source] for source in renewable_sources]
    labels = [source.replace(' [TWh]', '').replace('Generacion ','') for source in renewable_sources]
    colors = ['yellow','olivedrab','lime','deepskyblue','darkgrey']#sns.color_palette('pastel')[0:len(values)] # Usar paleta de colores de Seaborn

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4  # tipo donut
    )])

    fig.update_layout(title=f"Distribución de Energía - {eleccion_pais}")

    return fig

def grafico_mix_electrico(pais_df, eleccion_pais, start_year, end_year):

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set(style="darkgrid")
    # Filter data by year range
    filtered_df = pais_df[(pais_df['Tiempo [años]'] >= start_year) & (pais_df['Tiempo [años]'] <= end_year)].copy()
 
    # Redraw with non-renewables as part of the stack
    ax.stackplot(filtered_df['Tiempo [años]'],
                 filtered_df['Generacion no renovable [TWh]'],
                 filtered_df['Generacion hidroelectrica [TWh]'],
                 filtered_df['Generacion solar [TWh]'],
                 filtered_df['Generacion eolica [TWh]'],
                 filtered_df['Generacion geotermica-biomasa-otras [TWh]'],
                 labels=['No Renovables','Hidro', 'Solar', 'Eólica', 'Geo/Biomasa/Otras'],
                 colors=['darkgrey','deepskyblue','yellow','olivedrab','lime'],
                 alpha=0.8)

    ax.set_xlabel('Tiempo [años]')
    ax.set_ylabel('Generación de Energía [TWh]')
    ax.set_title(f'Mix Eléctrico de {eleccion_pais}')
    ax.legend(loc='upper left')
    ax.grid(True)

    return fig

# prompt: colors = {"Generacion solar [TWh]":'yellow',
#           'Generacion eolica [TWh]':'olivedrab',
#           'Generacion geotermica-biomasa-otras [TWh]':'lime',
#           'Generacion hidroelectrica [TWh]':'deepskyblue',
#           "Generacion renovable con hidroelectrica [TWh]":'greenyellow',
#           "Generacion renovable sin hidroelectrica [TWh]":'yellowgreen',
#           "Generacion no renovable [TWh]":'darkred'} quiero que la funcion grafico_da_barras_agrupadas tenga estos colores

def grafico_barras_agrupadas(countries, start_year, end_year, generation_energy_types,dfs_paises):
    data_to_plot = {}
    fuentes_de_energia = {'Solar':"Generacion solar [TWh]",
                          'Eolica':"Generacion eolica [TWh]",
                          'Geotherm-Biomass':"Generacion geotermica-biomasa-otras [TWh]",
                          'Hidro':"Generacion hidroelectrica [TWh]",
                          'Renovables':"Generacion renovable con hidroelectrica [TWh]",
                          'Renovables sin Hidro':"Generacion renovable sin hidroelectrica [TWh]",
                          'No renovable':"Generacion no renovable [TWh]"}

    #generation_energy_types=[fuentes_de_energia.get(i) for i in fuentes_seleccionadas]
    # Iterar sobre los países seleccionados
    for country in countries:
        df_country = dfs_paises[country].copy().rename(columns={'Generacion solar [TWh]': 'Solar',
                                                                'Generacion eolica [TWh]': 'Eólica',
                                                                'Generacion geotermica-biomasa-otras [TWh]': 'Geotérmica y Biomasa',
                                                                'Generacion hidroelectrica [TWh]':'Hidro',
                                                                'Generacion renovable con hidroelectrica [TWh]': 'Renovables',
                                                                'Generacion renovable sin hidroelectrica [TWh]': 'Renovables sin Hidro',
                                                                'Generacion no renovable [TWh]':'No renovable'})
        
        df_filtered = df_country[(df_country['Tiempo [años]'] >= start_year) & (df_country['Tiempo [años]'] <= end_year)].copy()

        # Calcular porcentajes para cada tipo de energía y obtener el promedio
        country_percentages = {}
        for energy_type_col in generation_energy_types:
            # Manejar la división por cero
            percentage = (df_filtered[energy_type_col] / df_filtered['Generacion total de energia  [TWh]']) * 100
            percentage = percentage.replace([np.inf, -np.inf], np.nan) # Reemplazar inf con NaN
            avg_percentage = percentage.mean()
            country_percentages[energy_type_col] = avg_percentage

        if country_percentages: # Add country data only if there's any percentage calculated
             data_to_plot[country] = country_percentages

    # Convertir a DataFrame para graficar
    df_plot = pd.DataFrame(data_to_plot)

    # Crear el gráfico de barras agrupadas
    fig, ax = plt.subplots(figsize=(15, 8))

    colors = {
        'Solar': 'yellow',
        'Eólica': 'olivedrab',
        'Geotérmica y Biomasa': 'lime',
        'Hidro': 'deepskyblue',
        'Renovables': 'greenyellow',
        'Renovables sin Hidro': 'yellowgreen',
        'No renovable': 'grey'
    }

    # Transponer para que los países sean las etiquetas del eje X
    df_plot.T.plot(kind='bar', ax=ax, width=0.8,color=[colors.get(i) for i in generation_energy_types])

    #ax.set_xlabel('País')
    ax.set_ylabel('Porcentaje de la Generación Total de Electricidad (%)')
    ax.set_title(f'Porcentaje de las diferentes fuentes de electricidad en {end_year}')
    ax.tick_params(axis='x', rotation=0)
    ax.legend(title='Tipo de Generación', bbox_to_anchor=(1.005, 1), loc='upper left')
    ax.grid(axis='y')

    plt.tight_layout()
    plt.show()

    return fig



def grafico_dispersion(df, col1, col2,pais):

    fig=plt.figure(figsize=(10, 6))
    sns.set(style="darkgrid")
    sns.scatterplot(data=df, x=col1, y=col2)

    # Generate title and labels automatically
    title = f'{col1} vs {col2} en {pais}'
    xlabel = col1
    ylabel = col2

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    
    return fig

def grafico_tiempo(df_pais_, cols, inicio, final, pais):

    df_pais = df_pais_.copy().rename(columns={'Generacion solar [TWh]': 'Solar',
                                                                'Generacion eolica [TWh]': 'Eólica',
                                                                'Generacion geotermica-biomasa-otras [TWh]': 'Geotérmica y Biomasa',
                                                                'Generacion hidroelectrica [TWh]':'Hidro',
                                                                'Generacion renovable con hidroelectrica [TWh]': 'Renovables',
                                                                'Generacion renovable sin hidroelectrica [TWh]': 'Renovables sin Hidro',
                                                                'Generacion no renovable [TWh]':'No renovable'})
    
    fig=plt.figure(figsize=(8, 5))
    for i in cols:
        plt.plot(df_pais['Tiempo [años]'], df_pais[i], label=i)

    # Generate title and labels automatically
    title = f'Brechas entre fuentes energeticas en {pais}'
    xlabel = 'Tiempo [años]'
    ylabel = 'Generacion energetica [TWh]'

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.xlim(inicio,final)
    plt.grid(True)
    
    return fig


def grafico_matriz_energetica_bar(pais_df,eleccion_pais, start_year, end_year):

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.set(style="darkgrid")
    # Filter data by year range
    pais = pais_df[(pais_df['Tiempo [años]'] >= start_year) & (pais_df['Tiempo [años]'] <= end_year)].copy()

    ax.bar(pais['Tiempo [años]'],pais["Generacion no renovable [TWh]"], label='No renovable')
    ax.bar(pais['Tiempo [años]'],pais['Generacion hidroelectrica [TWh]'],bottom=pais["Generacion no renovable [TWh]"], label='Hidro')
    ax.bar(pais['Tiempo [años]'],pais['Generacion solar [TWh]'],bottom= pais["Generacion no renovable [TWh]"]+pais['Generacion hidroelectrica [TWh]'],label='solar')
    ax.bar(pais['Tiempo [años]'],pais['Generacion eolica [TWh]'], bottom= pais["Generacion no renovable [TWh]"]+pais['Generacion hidroelectrica [TWh]']+pais['Generacion solar [TWh]'],label='eolica')
    ax.bar(pais['Tiempo [años]'],pais['Generacion geotermica-biomasa-otras [TWh]'], bottom= pais["Generacion no renovable [TWh]"]+pais['Generacion hidroelectrica [TWh]']+pais['Generacion solar [TWh]']+pais['Generacion eolica [TWh]'], label='Geotherma-biomasa-others')
    ax.set_xlim(start_year,end_year)
    ax.set_xlabel('Tiempo [años]')
    ax.set_ylabel('Generación de Energía [TWh]')
    ax.set_title(f'Evolución del Mix de {eleccion_pais}')
    ax.legend(loc='upper left')
    ax.grid(True)

    return fig

def mostrar_kpis_comparativos(df_colombia, df_latam, anio: float):
    """
    Calcula y muestra KPIs comparativos entre Colombia y Latinoamérica:
    1. Brecha de Generación Renovable (sin hidro)
    2. Brecha de Dependencia Hidroeléctrica
    
    Args:
        df_colombia (DataFrame): Datos de generación de energía para Colombia
        df_latam (DataFrame): Datos de generación de energía para Latinoamérica (promedio)
        anio (float): Año para el cálculo de los KPIs
    """
    
    # Filtrar datos para el año seleccionado
    col_anio = df_colombia.query(f'`Tiempo [años]` == {str(anio)}')
    latam_anio = df_latam.query(f'`Tiempo [años]` == {str(anio)}')
    
    if col_anio.empty or latam_anio.empty:
        st.warning(f"No hay datos disponibles para el año {anio}")
        return
    
    # Calcular porcentajes para Colombia
    gen_total_col = col_anio["Generacion total de energia  [TWh]"].iloc[0]
    gen_renovable_sin_hidro_col = col_anio["Generacion renovable sin hidroelectrica [TWh]"].iloc[0]
    gen_hidro_col = col_anio["Generacion hidroelectrica [TWh]"].iloc[0]
    
    pct_renovable_sin_hidro_col = (gen_renovable_sin_hidro_col / gen_total_col) * 100
    pct_hidro_col = (gen_hidro_col / gen_total_col) * 100
    
    # Calcular porcentajes para Latinoamérica (promedio)
    gen_total_latam = latam_anio["Generacion total de energia  [TWh]"].iloc[0]
    gen_renovable_sin_hidro_latam = latam_anio["Generacion renovable sin hidroelectrica [TWh]"].iloc[0]
    gen_hidro_latam = latam_anio["Generacion hidroelectrica [TWh]"].iloc[0]
    
    pct_renovable_sin_hidro_latam = (gen_renovable_sin_hidro_latam / gen_total_latam) * 100
    pct_hidro_latam = (gen_hidro_latam / gen_total_latam) * 100
    
    # Calcular brechas
    brecha_renovable = pct_renovable_sin_hidro_latam - pct_renovable_sin_hidro_col
    brecha_hidro = pct_hidro_col - pct_hidro_latam
    

    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.metric(
            label="🌱 Brecha de Generación Renovable (sin hidro)",
            value=f"{brecha_renovable:.1f}%",
            help="Diferencia en % de generación renovable no hidroeléctrica entre Latinoamérica y Colombia"
        )
        
        st.markdown(f"""
        <div style= padding:15px; border-radius:10px; margin-top:10px;">
            <p style="font-size:14px; margin-bottom:5px;"><b>Detalle:</b></p>
            <p style="font-size:12px; margin-bottom:2px;">Latinoamérica: {pct_renovable_sin_hidro_latam:.1f}%</p>
            <p style="font-size:12px; margin-bottom:2px;">Colombia: {pct_renovable_sin_hidro_col:.1f}%</p>
            <p style="font-size:12px; margin-top:10px;"><i>Valor positivo indica que Latinoamérica está más avanzada</i></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(
            label="💧 Brecha de Dependencia Hidroeléctrica",
            value=f"{brecha_hidro:.1f}%",
            help="Diferencia en % de generación hidroeléctrica entre Colombia y Latinoamérica"
        )
        
        st.markdown(f"""
        <div style= padding:15px; border-radius:10px; margin-top:10px;">
            <p style="font-size:14px; margin-bottom:5px;"><b>Detalle:</b></p>
            <p style="font-size:12px; margin-bottom:2px;">Colombia: {pct_hidro_col:.1f}%</p>
            <p style="font-size:12px; margin-bottom:2px;">Latinoamérica: {pct_hidro_latam:.1f}%</p>
            <p style="font-size:12px; margin-top:10px;"><i>Valor positivo indica mayor dependencia de Colombia en hidro</i></p>
        </div>
        """, unsafe_allow_html=True)
    
    # CSS para modificar el tamaño de la fuente en los KPI
    st.markdown("""
    <style>
        /* Estilo para el valor principal de la métrica */
        .st-emotion-cache-1wivap2 {
            font-size: 1.8rem !important;
        }

        /* Estilo para la etiqueta de la métrica */
        .st-emotion-cache-qoz3f2 {
            font-size: 1rem !important;
        }
        
        /* Mejorar el espaciado entre elementos */
        .stMetric {
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def plot_co2_projection(dfs_paises, pais):
    df_country = dfs_paises[pais].copy()
    df_country["Tiempo [años]"] = pd.to_numeric(df_country["Tiempo [años]"], errors='coerce')
    df_country["Emisiones de CO2 [MTon]"] = pd.to_numeric(df_country["Emisiones de CO2 [MTon]"], errors='coerce')
    df_country.dropna(subset=["Tiempo [años]", "Emisiones de CO2 [MTon]"], inplace=True)

    # Ensure data for regression starts from 2000 onwards (as in the original code context)
    df_regression = df_country[df_country["Tiempo [años]"] >= 2000].copy() # Assuming 2000 was the intended start for regression

    X = df_regression[["Tiempo [años]"]]
    y = df_regression["Emisiones de CO2 [MTon]"]

    modelo = LinearRegression()
    modelo.fit(X, y)

        # Project to 2030
    proyeccion_2030 = modelo.predict(np.array([[2030]]))[0]
        # Meta oficial para el sector eléctrico  en 2030 (used as a reference)
    meta_2030 = dfs_paises[pais]['Emisiones de CO2 [MTon]'].to_numpy().mean()
    meta_min=meta_2030-(meta_2030*0.1)
    meta_max=meta_2030+(meta_2030*0.1)
        # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_country["Tiempo [años]"], df_country["Emisiones de CO2 [MTon]"], label="Histórico")
    ax.scatter([2030], [proyeccion_2030], color='red', zorder=5, label=f"Proyección {pais} 2030") # Use zorder to ensure scatter point is visible
    ax.axhline(y=meta_2030, color='green', linestyle='--', label=f"Meta {pais} 2030 ({meta_2030:.2f} Mt)")
    # Optionally add the min and max goals from the original plot as reference
    ax.axhline(y=meta_min, color='orange', linestyle=':', label=f"Meta mínima {pais} ({meta_min:.2f} Mt)")
    ax.axhline(y=meta_max, color='blue', linestyle=':', label=f"Meta máxima {pais} ({meta_min:.2f} Mt)")

    ax.set_xlabel("Año")
    ax.set_ylabel("Emisiones CO₂ (Mt)")
    ax.set_title(f"Emisiones de CO₂ {pais}: Histórico, Proyección y Meta {pais} 2030")

    ax.legend()
    ax.grid(True)

    return fig

