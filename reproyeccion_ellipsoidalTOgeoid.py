from osgeo import gdal
import subprocess


### 1° REPROYECCIÓN VERTICAL ###
# Ruta al archivo de entrada y salida
input_dem = "/media/ailin/arturito/Sensores/pnlg/Spega/DEMs/Tandem/TDM1_DEM__04_S51W074_DEM.tif"
output_dem = "/media/ailin/arturito/Sensores/pnlg/Spega/DEMs/Tandem/TDM1_DEM__04_S51W074_DEM_EGM96.tif"

# Abrir el archivo de entrada
ds = gdal.Open(input_dem, gdal.GA_ReadOnly)

if ds is None:
    print("No se pudo abrir el archivo de entrada.")
    exit(1)
ds.GetMetadata() #  uso GetMetadata porque GetProjection no me informa sobre el sist de coordenadas vertical
input_vertical = ds.GetMetadataItem("VERTICAL_CS")
if input_vertical:
    print("Proyección vertical:", input_vertical)
else:
    print("No se encontró información de proyección vertical.")

# Definir la línea de comando GDAL para la conversión EGM96 a WGS84
comando_gdal = 'gdalwarp -overwrite /media/ailin/arturito/Sensores/pnlg/Spega/DEMs/Tandem/TDM1_DEM__04_S51W074_DEM.tif /media/ailin/arturito/Sensores/pnlg/Spega/DEMs/Tandem/TDM1_DEM__04_S51W074_DEM_EGM96.tif -s_srs EPSG:7661 -t_srs EPSG:4326+5773' # lo saqué de https://gis.stackexchange.com/questions/378891/epsg-for-tandem-x-ellipsoid
# EPSG 7661 es Datum: World Geodetic System 1984 (G1150) con Ellipsoid: WGS 84 (perteneciente al TanDEM). EPSG 4326 es WGS 84 + 5773 es EGM96 height (3D)

# Ejecutar el comando utilizando subprocess
proceso = subprocess.run(comando_gdal, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Verificar si hubo algún error durante la ejecución del proceso
if proceso.returncode != 0:
    print('Ocurrió un error durante la conversión:')
    print(proceso.stderr.decode('utf-8'))
else:
    print('Conversión exitosa.')

# Obtener la Metadata del output_dem
output_ds = gdal.Open(output_dem, gdal.GA_ReadOnly)
output_ds.GetMetadata() # uso GetMetadata porque GetProjection no me informa sobre el sist de coordenadas vertical
ds.GetProjection()
vertical_projection = output_ds.GetMetadataItem("VERTICAL_CS")
if vertical_projection:
    print("Proyección vertical:", vertical_projection)
else:
    print("No se encontró información de proyección vertical.")

# Funciona bien la repro, da igual que con rasterio y se resume en una linea
# Cerrar los datasets
output_ds = None
ds = None