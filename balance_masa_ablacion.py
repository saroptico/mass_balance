# Importar librerías
import pandas as pd

### Quizás con alguna librería como gdal o similar se pueden extraer los valores de pixel en cada DEM y generar el csv sin pasar por SNAP
# Abrir el csv con los datos de elevación ya purgados y corregidos según el archivo: correccion_DEMs_icesat.py
ablacion = pd.read_csv('/media/ailin/arturito/Sensores/pnlg/Escondidos/shapes/Dickson/point_sampling_ablacion_dickson_corregido.csv', sep=',')
print(ablacion.columns)


# Cálculo de BALANCE DE MASA

# Datos
mask_pixels_ablacion = 32521
area_pixel = 31*31 # [m2]
mask_area_ablacion = mask_pixels_ablacion*area_pixel # [m2]
dens_agua = 1000 # densidad agua [kg/m3]
dens_hielo = 900 # densidad promedio hielo [kg/m3]
SRTM = 2000
ALOS = 2009
TANDEM = 2015
años1 = ALOS-SRTM
años2 = TANDEM-ALOS


# Si quiero calcular el Balance de masa neto volumétrico [kg/m2]: balance_neto_ablac_1 = balance_ablac_vol_1/mask_area_ablacion

balance_ablac_vol_1 = (ablacion ['alos'] - ablacion['srtm']).sum()*area_pixel*dens_hielo # Balance de masa volumétrico [kg]
balance_ablac_maea_1 = balance_ablac_vol_1/mask_area_ablacion/dens_agua/años1 # Balance de masa neto anual en metros de agua equivalentes
balance_ablac_vol_2 = (ablacion ['tandem'] - ablacion['alos']).sum()*area_pixel*dens_hielo # Balance de masa volumétrico [kg]
balance_ablac_maea_2 = balance_ablac_vol_2/mask_area_ablacion/dens_agua/años2 # Balance de masa neto anual en metros de agua equivalentes

print("Balance ablación neto anual entre 2000 y 2009 [mae]: ", balance_ablac_maea_1)
print("Balance ablación neto anual entre 2009 y 2015 [mae]: ", balance_ablac_maea_2)
print("Balance ablación neto anual entre 2000 y 2015 [mae]: ", balance_ablac_maea_1 + balance_ablac_maea_2)

# Cálculo de contribución al nivel del mar (https://nbviewer.org/gist/jmalles/ca70090812e6499b34a22a3a7a7a8f2a referido a: https://www.nature.com/articles/s41561-019-0300-3)
### solo se van a calcular los mm correspondientes al período de balance negativo (cuando se derritió hielo) ###

# Cálculo del volúmen de la masa de hielo perdida
ab_vol_1 = (ablacion ['alos'] - ablacion['srtm']).sum()*area_pixel # delta de volumen por área de pixel [m3]. 
ab_vol_2 = (ablacion ['tandem'] - ablacion['alos']).sum()*area_pixel # delta de volumen por área de pixel [m3]. 


# Conversión de masa de hielo en aumento de nivel del mar (suponiendo que toda esa masa se derrite)
# Para saber cuánto aumentaría el nivel del mar (n.d.m. o s.l.e.) en mm, tenemos que saber cuál es el área total que ocupa el océano. Por dato se sabe que es
# igual a 3.618.E8 km2. Entonces, 1 mm de incremento en el n.d.m. requiere de 10.E-3 m3 de agua por metro cuadrado de superficie, osea 10.E-12 Gt de agua.

# Calculo primero el volumen de agua requerido para incrementar el nivel del mar por 1 mm
area_mar = 3.618*10**8 # km2
altura = 0.001 # m
volumen_mar = area_mar * altura # km3 print(volumen_mar)
# Si quisiera medir el equivalente en el nivel del Lago Argentino, reemplazo area_mar por area_lago
area_lago = 892000000 # m2
volumen_lago = area_lago * altura # m3 

# Cálculo del equivalente en nivel del lago (lago level equivalent)
LLE_1 = ab_vol_1 / area_lago * dens_hielo / dens_agua * (-1000) # mm
LLE_2 = ab_vol_2 / area_lago * dens_hielo / dens_agua * (-1000) # mm

print("Equivalente sobre nivel del lago entre 2000 y 2009 [mm]: ", LLE_1)
print("Equivalente sobre nivel del lago entre 2009 y 2015 [mm]: ", LLE_2)
print("Equivalente sobre nivel del lago entre 2000 y 2015 [mm]: ", LLE_1 + LLE_2)