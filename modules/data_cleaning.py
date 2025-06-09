#librerias
import numpy as np
import pandas as pd


# Funciones  para limpiar datos

#----------------------limpieza y obtencion de dataframes---------------------------------
def obtencion_dataframes(nombre_hoja, años='Terawatt-hours',  paises = ['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia',
                        'Ecuador', 'Peru', 'Venezuela','Central America',
                        'Other South America','Total World']):

  #Creación del dataframe
  df = pd.read_excel('EI-Stats-Review-All-Data.xlsx', sheet_name=nombre_hoja)
  #Organización en los titulos de columnas y filas, se transpone el dataframe para  que las columnas sean los paises
  nombres_filas=np.arange(0,len(df.iloc[0]),1)
  df.columns = nombres_filas
  df = df.T
  nombres_columnas=df.iloc[0]
  df.columns = nombres_columnas
  df = df.drop([0,len(df)-1,len(df)-2,len(df)-3])

  df = df[[años]+ ['Argentina','Brazil','Chile','Colombia','Ecuador','Peru','Venezuela','Central America','Other Caribbean','Other South America',
                     'Canada','Mexico','US','Total North America',
                     'Total Europe',
                     'Total CIS',
                     'Total Middle East',
                     'Total Africa',
                     'Total Asia Pacific',
                     'Total World'
                    ]
          ]
  
  df = df.rename(columns={años: 'Años'})
  return df
#-------------------------------
def exajoules_to_twh(df_exajoules,paises=['Argentina','Brazil','Chile','Colombia','Ecuador','Peru','Venezuela','Central America','Other Caribbean','Other South America',
                     'Canada','Mexico','US','Total North America',
                     'Total Europe',
                     'Total CIS',
                     'Total Middle East',
                     'Total Africa',
                     'Total Asia Pacific',
                     'Total World'
                    ],años=np.arange(1985.0,2024.0,1)):
  df_TWh = df_exajoules[paises] * 277.778
  df_TWh.insert(0,'Años',años)
  return df_TWh
#---------------------------
