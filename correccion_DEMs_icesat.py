### Se trabaja con la diferencia entre los puntos icesat y los DEMs obtenida para Spega con: /media/ailin/arturito/Sensores/pnlg/Spega/py y excel/correccion_DEMs_icesat.py
import pandas as pd

####### abro el archivo ABLACION con los puntos de elevación de los DEM
ablacion = pd.read_csv('/media/ailin/arturito/Sensores/pnlg/Escondidos/shapes/Dickson/point_sampling_ablacion_dickson.csv', decimal=',', sep=',')
print(ablacion.sample(10)) # chequeo si está correcto (si, soy insegura)

# cambio nombres de columnas con los nombres de los DEMs
ablacion.rename(
    columns=({'apliado_es':'alos', 'apliado__1':'srtm', 'apliado__2':'tandem'}), 
    inplace=True,
    )
print(ablacion.columns) # chequeo si está correcto
print(ablacion.sample(50))



# eliminar datos erroneos (NaN, ceros y outliers) y guardar archivo
ablacion = ablacion.dropna(subset=["srtm","alos", "tandem"])

# Intenta convertir todas las columnas a datos tipo float para evitar errores
for column in ablacion.columns:
    try:
        ablacion[column] = ablacion[column].astype(float)
    except ValueError:
        print(f"No se puede convertir la columna {column} a float.")
# elimino ceros y outliers de las columnas y decimales en tandem
ablacion['tandem'] = ablacion['tandem'].round(0)
ablacion = ablacion.query("srtm !=0 and srtm != -32767 and tandem !=0")

# check resultados
print(ablacion.head(20)) # o ablacion.sample(20)
ablacion.to_csv('/media/ailin/arturito/Sensores/pnlg/Escondidos/shapes/Dickson/point_sampling_ablacion_dickson_purged.csv', index=False) # guardo nuevo archivo

# Selecciono las columnas con los datos de interés
columnas = ['tandem', 'alos', 'srtm']



# # corregir error de importación en columna Tandem debido a decimales, openoffice o que se yo:
# # Correct the 'tandem' column by dividing by 1000 if they were erroneously scaled by e+06 instead of e+03
# ablacion['tandem'] = ablacion['tandem'].apply(lambda x: x / 1000 if x > 1e5 else x)
# # eliminar datos erroneos (NaN, ceros y outliers) y guardar archivo
# ablacion = ablacion.dropna(subset=["srtm","alos", "aster","tandem"])
# ablacion = ablacion.query("srtm !=0 and aster !=0 and tandem !=0 and alos !=-9999 and aster !=-9999 and tandem !=-32784 and srtm !=-32767")
# print(ablacion.sample(20)) # chequeo si está correcto (si, soy insegura)
# Convert 'tandem' column to integers porque tiene muchos decimales
# ablacion['tandem'] = ablacion['tandem'].round().astype(int)

# Calculate the minimum values for the specified columns
min_values = ablacion[columnas].min()
# Calculate the maximum values for the specified columns
max_values = ablacion[columnas].max()
# Print the minimum values
print("Minimum values:\n", min_values)
# Print the maximum values
print("Maximum values:\n", max_values) # si, sigo siendo insegura


# corregir los DEM según el promedio de las diferencias con los icesat:
average_differences = {'tandem':15,'alos':30,'srtm':14} # creo un diccionario que tendrá las diferencias promedios calculadas en "correccion_DEMs_icesat.py (spega)"

# iterar en cada valor del diccionario con las diferencias promedio (sumo porque antes hice la resta photon - DEM)
for column, avg_diff in average_differences.items():
    if column in ablacion.columns:
        ablacion[column] += avg_diff

# Check the result
print(ablacion.head(10))
ablacion.to_csv('/media/ailin/arturito/Sensores/pnlg/Escondidos/shapes/Dickson/point_sampling_ablacion_dickson_corregido.csv', index=False) # guardo nuevo archivo


####### abro el archivo ACUMULACION con los puntos de elevación de los DEM
acumulacion = pd.read_csv('/media/ailin/arturito/Sensores/pnlg/Escondidos/shapes/Dickson/point_sampling_acumulacion_dickson.csv', decimal=',', sep=',')
print(acumulacion.sample(10)) # chequeo si está correcto (si, soy insegura)

# cambio nombres de columnas con los nombres de los DEMs
acumulacion.rename(
    columns=({'apliado_es':'alos', 'apliado__1':'srtm', 'apliado__2':'tandem'}), 
    inplace=True,
    )
print(acumulacion.columns) # chequeo si está correcto
print(acumulacion.sample(10))


# eliminar datos erroneos (NaN, ceros y outliers) y guardar archivo
acumulacion = acumulacion.dropna(subset=["srtm","alos", "tandem"])

# Intenta convertir todas las columnas a datos tipo float para evitar errores
for column in acumulacion.columns:
    try:
        acumulacion[column] = acumulacion[column].astype(float)
    except ValueError:
        print(f"No se puede convertir la columna {column} a float.")

# elimino ceros y outliers de las columnas y decimales en tandem
acumulacion['tandem'] = acumulacion['tandem'].round(0)
acumulacion = acumulacion.query("srtm !=0 and srtm != -32767 and tandem !=0")
acumulacion.to_csv('/media/ailin/arturito/Sensores/pnlg/Escondidos/shapes/Dickson/point_sampling_acumulacion_dickson_purged.csv', index=False) # guardo nuevo archivo

# check resultados
print(acumulacion.head(20)) # o ablacion.sample(20)

# Selecciono las columnas con los datos de interés
columnas = ['tandem', 'alos', 'srtm']



# # corregir error de importación en columna Tandem debido a decimales, openoffice o que se yo:
# # Correct the 'tandem' column by dividing by 1000 if they were erroneously scaled by e+06 instead of e+03
# ablacion['tandem'] = ablacion['tandem'].apply(lambda x: x / 1000 if x > 1e5 else x)
# # eliminar datos erroneos (NaN, ceros y outliers) y guardar archivo
# ablacion = ablacion.dropna(subset=["srtm","alos", "aster","tandem"])
# ablacion = ablacion.query("srtm !=0 and aster !=0 and tandem !=0 and alos !=-9999 and aster !=-9999 and tandem !=-32784 and srtm !=-32767")
# print(ablacion.sample(20)) # chequeo si está correcto (si, soy insegura)
# Convert 'tandem' column to integers porque tiene muchos decimales
# ablacion['tandem'] = ablacion['tandem'].round().astype(int)




# Calculate the minimum values for the specified columns
min_values = acumulacion[columnas].min()
# Calculate the maximum values for the specified columns
max_values = acumulacion[columnas].max()
# Print the minimum values
print("Minimum values:\n", min_values)
# Print the maximum values
print("Maximum values:\n", max_values) # si, sigo siendo insegura


# corregir los DEM según el promedio de las diferencias con los icesat:
# iterar en cada valor del diccionario con las diferencias promedio (sumo porque antes hice la resta photon - DEM)
for column, avg_diff in average_differences.items():
    if column in acumulacion.columns:
        acumulacion[column] += avg_diff

# Check the result
print(acumulacion.head(10))
acumulacion.to_csv('/media/ailin/arturito/Sensores/pnlg/Escondidos/shapes/Dickson/point_sampling_acumulacion_dickson_corregido.csv', index=False) # guardo nuevo archivo