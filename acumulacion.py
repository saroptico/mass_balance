# Importar librerías
import pandas as pd

# Datos
mask_pixels_acumulacion = 120461
mask_area_acumulacion = 115.508*10**6 # [m2]
area_pixel = mask_area_acumulacion/mask_pixels_acumulacion
dens_nieve = 450 # densidad promedio nieve [kg/m3]
dens_agua = 1000 # densidad agua [kg/m3]
SRTM = 2000
ASTER = 2005
ALOS = 2011
TANDEM = 2015
años1 = ASTER-SRTM
años2 = ALOS-ASTER
años3 = TANDEM-ALOS

# Abrir el archivo csv 
acumulacion = pd.read_csv('collocation_DEMs/collocate4_acumulacion_posgar_Mask.txt', sep='\t')

# eliminar datos erroneos (NaN y ceros) y sobreescribir archivo
acumulacion = acumulacion.dropna(subset=["srtm", "tandem"])
acumulacion = acumulacion.query("srtm !=0 and aster !=0 and tandem !=0")
acumulacion.to_csv('collocation_DEMs/collocate4_acumulacion_posgar_Mask_purged.txt', index=False)


# Cálculo de BALANCE DE MASA

# Si quiero calcular el Balance de masa neto volumétrico [kg/m2]: balance_neto_acum_1 = balance_acum_vol_1/mask_area_acumulacion 

balance_acum_vol_1 = acumulacion ['srtm-aster'].sum()*area_pixel*dens_nieve*(-1) # Balance de masa volumétrico [kg]. Se multiplica por -1 para dar vuelta la resta de años
balance_acum_maea_1 = balance_acum_vol_1/mask_area_acumulacion/dens_agua/años1 # Balance de masa neto en metros de agua equivalentes
balance_acum_vol_2 = acumulacion ['aster-alos'].sum()*area_pixel*dens_nieve*(-1) # Balance de masa volumétrico. Se multiplica por -1 para dar vuelta la resta de años
balance_acum_maea_2 = balance_acum_vol_2/mask_area_acumulacion/dens_agua/años2 # Balance de masa neto en metros de agua equivalentes
balance_acum_vol_3 = acumulacion ['alos-tandem'].sum()*area_pixel*dens_nieve*(-1) # Balance de masa volumétrico. Se multiplica por -1 para dar vuelta la resta de años
balance_acum_maea_3 = balance_acum_vol_3/mask_area_acumulacion/dens_agua/años3 # Balance de masa neto en metros de agua equivalentes

print("Balance acumulación neto anual entre 2000 y 2005 [mae]: ", balance_acum_maea_1)
print("Balance acumulación neto anual entre 2005 y 2011 [mae]: ", balance_acum_maea_2)
print("Balance acumulación neto anual entre 2011 y 2015 [mae]: ", balance_acum_maea_3)
print("Balance acumulación neto anual entre 2000 y 2015 [mae]: ", balance_acum_maea_3 + balance_acum_maea_2 + balance_acum_maea_1)

# Cálculo de contribución al nivel del mar (https://www.antarcticglaciers.org/glaciers-and-climate/estimating-glacier-contribution-to-sea-level-rise/)

# Cálculo del volúmen de la masa de hielo perdida
acum_vol_1 = acumulacion ['srtm-aster'].sum()*area_pixel*0.000000001 # delta de volumen por área de pixel [km3]
acum_vol_2 = acumulacion ['aster-alos'].sum()*area_pixel*0.000000001 # delta de volumen por área de pixel [km3]
acum_vol_3 = acumulacion ['alos-tandem'].sum()*area_pixel*0.000000001 # delta de volumen por área de pixel [km3]

# Conversión de volumen a masa de hielo expresada en Gigatoneladas
dens_nieve = 0.45 # [Gt/km3]
masa_nieve_1 = acum_vol_1 * dens_nieve # [Gt]
masa_nieve_2 = acum_vol_2 * dens_nieve # [Gt]
masa_nieve_3 = acum_vol_3 * dens_nieve # [Gt]

# Conversión de masa de nieve en aumento de nivel del mar (suponiendo que toda esa masa se derrite)
# Para saber cuánto aumentaría el nivel del mar (n.d.m. o s.l.e.) en mm, tenemos que saber cuál es el área total que ocupa el océano. Por dato se sabe que es
# igual a 3.618.E8 km2. Entonces, 1 mm de incremento en el n.d.m. requiere de 10.E-3 m3 de agua por metro cuadrado de superficie, osea 10.E-12 Gt de agua.

# Calculo primero el volumen de agua requerido para incrementar el nivel del mar por 1 mm
area_mar = 3.618*10**8 # km2
altura = 10**-6 # km (1 mm)
volumen_mar = area_mar * altura # km3/mm print(volumen_mar)

# Si quisiera medir el equivalente en el nivel del Lago Argentino, reemplazo area_mar por area_lago
area_lago = 892 # km2
volumen_lago = area_lago * altura # km3/mm 

# Cálculo del equivalente en nivel del mar (sea level equivalent)
SLE_1 = masa_nieve_1 * (1/volumen_mar)
SLE_2 = masa_nieve_2 * (1/volumen_mar)
SLE_3 = masa_nieve_3 * (1/volumen_mar)

# Cálculo del equivalente en nivel del lago (lago level equivalent)
LLE_1 = masa_nieve_1 / volumen_lago
LLE_2 = masa_nieve_2 / volumen_lago
LLE_3 = masa_nieve_3 / volumen_lago

print("Equivalente sobre nivel del mar entre 2000 y 2005 [mm]: ", SLE_1)
print("Equivalente sobre nivel del mar entre 2005 y 2011 [mm]: ", SLE_2)
print("Equivalente sobre nivel del mar entre 2011 y 2015 [mm]: ", SLE_3)
print("Equivalente sobre nivel del mar entre 2000 y 2015 [mm]: ", SLE_1 + SLE_2 + SLE_3)

print("Equivalente sobre nivel del lago entre 2000 y 2005 [mm]: ", LLE_1)
print("Equivalente sobre nivel del lago entre 2005 y 2011 [mm]: ", LLE_2)
print("Equivalente sobre nivel del lago entre 2011 y 2015 [mm]: ", LLE_3)
print("Equivalente sobre nivel del lago entre 2000 y 2015 [mm]: ", LLE_1 + LLE_2 + LLE_3)

