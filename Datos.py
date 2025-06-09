from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *
import json

#------------------Variables importantes--------------------
Regiones_y_paises = ['Argentina','Brazil','Chile','Colombia','Ecuador','Peru','Venezuela','Central America','Other Caribbean','Other South America',
                      'Canada','Mexico','US','Total North America',
                      'Total Europe',
                      'Total CIS',
                      'Total Middle East',
                      'Total Africa',
                      'Total Asia Pacific',
                      'Total World'
                    ]

#-------------------------------------------------------------

#------------------Carga de los datos-----------------------
Datos = Cargar_Datos()

Paises={}
for i in Regiones_y_paises:
  Paises[i]=df_variables(Datos,i)

paises_para_agregado_latam = ['Mexico', 'Argentina', 'Brazil', 'Chile', 'Colombia',
                                  'Ecuador', 'Peru', 'Venezuela', 'Central America',
                                  'Other South America']

Paises['Latinoamerica']=dataframe_latam(Datos,paises_para_agregado_latam)

# Convertir cada DataFrame a un diccionario
d_json_ready = {key: df.to_dict(orient='records') for key, df in Paises.items()}

# Guardar en un archivo JSON
with open('data.json', 'w') as f:
    json.dump(d_json_ready, f, indent=4)
