import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
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

import plotly.graph_objects as go

def grafico_generacion_y_emision_go(pais, eleccion_pais, inicio, final):
    # Filtrar los datos en el rango de tiempo especificado
    df_filtrado = pais[(pais['Tiempo [años]'] >= inicio) & (pais['Tiempo [años]'] <= final)]

    # Crear la figura con dos ejes Y
    fig = go.Figure()

    # Añadir trazado para Generación Total
    fig.add_trace(go.Scatter(
        x=df_filtrado['Tiempo [años]'],
        y=df_filtrado['Generacion total de energia  [TWh]'],
        name='Generación Total (TWh)',
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
        title=f' ',
        xaxis=dict(title='Tiempo [años]'),
        yaxis=dict(
            title='Generación Total [TWh]',
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
    gen_total = entrada["Generacion total de energia  [TWh]"].iloc[0]
    emisiones = entrada["Emisiones de CO2 [MTon]"].iloc[0]
    intensidad_carbono = emisiones / gen_total
    gen_renovable = entrada["Generacion renovable con hidroelectrica [TWh]"].iloc[0]
    porc_renovable = (gen_renovable / gen_total) * 100
    gen_solar = entrada["Generacion solar [TWh]"].iloc[0]
    gen_eolica = entrada["Generacion eolica [TWh]"].iloc[0]

    # Mostrar métricas como tarjetas
    col1, col2,col3 = st.columns([3,3,3],border=True)
    col1.metric(f"🔋 Generación Total {anio} ", f"{gen_total:.1f} TWh")
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

def grafico_tiempo(paises, col, inicio, final, pais):
    
    fig=plt.figure(figsize=(10, 6))
    for indice,nombres in enumerate(paises):
        plt.plot(nombres['Tiempo [años]'], nombres[col], label=pais[indice])

    # Generate title and labels automatically
    title = f'Tiempo [años] vs {col}' #en {pais}'
    xlabel = 'Tiempo [años]'
    ylabel = col

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.xlim(inicio,final)

    plt.grid(True)
    
    return fig


def grafico_matriz_energetica_bar(pais_df,eleccion_pais, start_year, end_year):

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set(style="darkgrid")
    # Filter data by year range
    pais = pais_df[(pais_df['Tiempo [años]'] >= start_year) & (pais_df['Tiempo [años]'] <= end_year)].copy()

    ax.bar(pais['Tiempo [años]'],pais['Generacion hidroelectrica [TWh]'], label='Hidro')
    ax.bar(pais['Tiempo [años]'],pais['Generacion solar [TWh]'],bottom= pais['Generacion hidroelectrica [TWh]'],label='solar')
    ax.bar(pais['Tiempo [años]'],pais['Generacion eolica [TWh]'], bottom= pais['Generacion hidroelectrica [TWh]']+pais['Generacion solar [TWh]'],label='eolica')
    ax.bar(pais['Tiempo [años]'],pais['Generacion geotermica-biomasa-otras [TWh]'], bottom= pais['Generacion hidroelectrica [TWh]']+pais['Generacion solar [TWh]']+pais['Generacion eolica [TWh]'], label='Geotherma-biomasa-others')
    ax.set_xlim(start_year,end_year)
    ax.set_xlabel('Tiempo [años]')
    ax.set_ylabel('Generación de Energía [TWh]')
    ax.set_title(f'Matriz Energética de {eleccion_pais}')
    ax.legend(loc='upper left')
    ax.grid(True)

    return fig





