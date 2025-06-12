from osgeo import gdal


### 2° REPROYECCIÓN HORIZONTAL
input_dem = "/home/ailin/Escritorio/spega/DEMs/SRTM/SRTM-X/W080S60/W080S60_XSAR_DEM.tif"
dem_posgar = "/home/ailin/Escritorio/spega/DEMs/SRTM/SRTM-X/W080S60/W080S60_XSAR_DEM_posgar.tif"

warp_horizontal = gdal.Warp(dem_posgar,input_dem,dstSRS='EPSG:5343') # POSGAR 07 faja 1

# Obtener la Metadata del DEM final
dem_final = gdal.Open(dem_posgar, gdal.GA_ReadOnly)
# Obtener la proyección
projection = dem_final.GetProjection()
print("Proyección:", projection)
dem_final.GetMetadata()

warp_horizontal = None # Closes the files