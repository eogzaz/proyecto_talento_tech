import pandas as pd
import numpy as np
import requests
from modules.data_cleaning import obtencion_dataframes
from modules.data_cleaning import exajoules_to_twh

def Cargar_Datos():
    #Datos obtenidos del proyecto The Energy Institute Statistical Review of World Energy del energy institute (https://www.energyinst.org/statistical-review)
    url = "https://www.energyinst.org/__data/assets/excel_doc/0020/1540550/EI-Stats-Review-All-Data.xlsx"
    nombre_del_archivo = "EI-Stats-Review-All-Data.xlsx"

    response = requests.get(url)

    with open(nombre_del_archivo, "wb") as file:
        file.write(response.content)



    paises_latam=['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia',
                            'Ecuador', 'Peru', 'Venezuela','Central America',
                            'Other South America']

    #-----------------------------Datos de emision de CO2------------------------------------------------
    df_EmisionesCO2 = obtencion_dataframes('Carbon Dioxide from Energy', 'Million tonnes of carbon dioxide',paises=paises_latam)[20:].reset_index(drop=True)

    #-----------------------------Datos de generación de energía-----------------------------------------

    #Generación Total
    df_electricity_generation = obtencion_dataframes('Electricity Generation - TWh',paises=paises_latam).reset_index(drop=True)

    #Generación Renovable
    df_solar_generation = obtencion_dataframes('Solar Generation - TWh',paises=paises_latam)[20:].reset_index(drop=True)
    df_wind_generation  = obtencion_dataframes('Wind Generation - TWh',paises=paises_latam)[20:].reset_index(drop=True)
    df_hydro_generation = obtencion_dataframes('Hydro Generation - TWh',paises=paises_latam)[20:].reset_index(drop=True)
    df_GeoBiomassOther  = obtencion_dataframes('Geo Biomass Other - TWh',paises=paises_latam)[20:].reset_index(drop=True)

    #Generación Renovable Total con Hidro
    df_Suma_Renovables_con_hidro = (df_solar_generation[paises_latam] + df_wind_generation[paises_latam] + df_GeoBiomassOther[paises_latam] + df_hydro_generation[paises_latam])
    df_Suma_Renovables_con_hidro.insert(0,'Años',np.arange(1985.0,2024.0,1))

    #Generación Renovable Total sin Hidro
    df_Suma_Renovables_sin_hidro = (df_solar_generation[paises_latam] + df_wind_generation[paises_latam] + df_GeoBiomassOther[paises_latam])
    df_Suma_Renovables_sin_hidro.insert(0,'Años',np.arange(1985.0,2024.0,1))

    #Generación no Renovable
    df_no_renovables_generation = (df_electricity_generation[paises_latam] - (df_solar_generation[paises_latam] + df_wind_generation[paises_latam] + df_GeoBiomassOther[paises_latam] + df_hydro_generation[paises_latam]))
    df_no_renovables_generation.insert(0,'Años',np.arange(1985.0,2024.0,1))

    #------------------------------Datos de comsumo energetico(Se hace la conversion de Exajulios a TWh)-------------------------------------------

    #Consumo primario total
    df_primary_energy_consumption = exajoules_to_twh(obtencion_dataframes('Primary energy cons - EJ','Exajoules',paises=paises_latam)[20:].reset_index(drop=True))

    #Consumo de energia Renovables
    df_solar_consumption = exajoules_to_twh(obtencion_dataframes('Solar Consumption - EJ','Exajoules (input-equivalent)',paises=paises_latam)[20:].reset_index(drop=True))
    df_wind_consumption  = exajoules_to_twh(obtencion_dataframes('Wind Consumption - EJ','Exajoules (input-equivalent)',paises=paises_latam)[20:].reset_index(drop=True))
    df_hydro_consumption = exajoules_to_twh(obtencion_dataframes('Hydro Consumption - EJ','Exajoules (input-equivalent)*',paises=paises_latam)[20:].reset_index(drop=True))
    df_GeoBiomassOther_consumption = exajoules_to_twh(obtencion_dataframes('Geo Biomass Other - EJ','Exajoules (input-equivalent)',paises=paises_latam)[20:].reset_index(drop=True))

    #Consumo Renovable total
    df_Suma_consumption_Renovables_con_hidro = (df_solar_consumption[paises_latam] + df_wind_consumption[paises_latam]+df_GeoBiomassOther_consumption[paises_latam]+df_hydro_consumption[paises_latam])
    df_Suma_consumption_Renovables_con_hidro.insert(0,'Años',np.arange(1985.0,2024.0,1))

    #Consumo Renovable total sin hidro
    df_Suma_consumption_Renovables_sin_hidro = (df_solar_consumption[paises_latam] + df_wind_consumption[paises_latam]+df_GeoBiomassOther_consumption[paises_latam])
    df_Suma_consumption_Renovables_sin_hidro.insert(0,'Años',np.arange(1985.0,2024.0,1))

    #Consumo No Renovable total
    df_no_renovables_consumption = (df_primary_energy_consumption[paises_latam] - (df_solar_consumption[paises_latam] + df_wind_consumption[paises_latam]+df_GeoBiomassOther_consumption[paises_latam]+df_hydro_consumption[paises_latam]))
    df_no_renovables_consumption.insert(0,'Años',np.arange(1985.0,2024.0,1))

    datos=[df_electricity_generation,
           df_solar_generation,
           df_wind_generation,
           df_GeoBiomassOther,
           df_hydro_generation,
           df_Suma_Renovables_con_hidro,
           df_Suma_Renovables_sin_hidro,
           df_no_renovables_generation,
           df_EmisionesCO2,
           df_primary_energy_consumption,
           df_solar_consumption,
           df_wind_consumption,
           df_hydro_consumption,
           df_GeoBiomassOther_consumption,
           df_Suma_consumption_Renovables_con_hidro,
           df_Suma_consumption_Renovables_sin_hidro,
           df_no_renovables_consumption]
    
    return datos




def df_variables(datos, pais):
    data={'Tiempo [años]':datos[0]['Años'],
        'Generacion total de energia  [TWh]':datos[0][pais],
            'Generacion solar [TWh]':datos[1][pais],
            'Generacion eolica [TWh]':datos[2][pais],
            'Generacion geotermica-biomasa-otras [TWh]':datos[3][pais],
            'Generacion hidroelectrica [TWh]':datos[4][pais],
            'Generacion renovable incluyendo hidroelectrica [TWh]':datos[5][pais],
            'Generacion renovable incluyendo hidroelectrica [TWh]':datos[6][pais],
            'Generacion no renovable [TWh]':datos[7][pais],
            'Emisiones de CO2 [MTon]':datos[8][pais],
            'Comsumo de energia primario [TWh]':datos[9][pais],
            'Comsumo de energia solar [TWh]':datos[10][pais],
            'Comsumo de energia eolica [TWh]':datos[11][pais],
            'Comsumo de energia hidroelectrica [TWh]':datos[12][pais],
            'Comsumo de energia geotermica-biomasa-otras [TWh]':datos[13][pais],
            'Comsumo de energia renovable incluyendo hidroelectrica [TWh]':datos[14][pais],
            'Comsumo de energia renovable incluyendo hidroelectrica [TWh]':datos[15][pais],
            'Comsumo de energia no renovable [TWh]':datos[16][pais]    
            }
    df_pais=pd.DataFrame(data)
    
    return df_pais

def dataframe_latam(datos,paises):
    l=[]  #lista auxiliar
    for i in paises:
        l.append(df_variables(datos,i))
    df_latam=sum(l)
        #Los años no se deben sumar
    df_latam['Tiempo [años]']=np.arange(1985.0,2024.0,1)
    return df_latam

