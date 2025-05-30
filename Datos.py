from modules.data_load import *
from modules.data_cleaning import *
from modules.data_analysis import *
import json

#------------------Variables importantes--------------------
paises_latam=['Mexico','Argentina', 'Brazil', 'Chile', 'Colombia','Ecuador', 'Peru', 'Venezuela','Central America','Other South America']

#-------------------------------------------------------------

#------------------Carga de los datos-----------------------
Datos = Cargar_Datos()

Paises={}
for i in paises_latam:
  Paises[i]=df_variables(Datos,i)
Paises['Latinoamerica']=dataframe_latam(Datos,paises_latam)

# Convertir cada DataFrame a un diccionario
d_json_ready = {key: df.to_dict(orient='records') for key, df in Paises.items()}

# Guardar en un archivo JSON
with open('data.json', 'w') as f:
    json.dump(d_json_ready, f, indent=4)
