import pandas as pd

def cargar_datos(ruta_csv):
    """
    Carga los datos del archivo CSV.
    """
    return pd.read_csv(ruta_csv, sep=',')

def calcular_balance_masa(ablacion, area_pixel, dens_hielo, dens_agua, SRTM, ALOS, TANDEM):
    """
    Calcula el balance de masa y el equivalente de nivel del lago para los periodos indicados.
    """
    años1 = ALOS - SRTM
    años2 = TANDEM - ALOS
    mask_pixels_ablacion = len(ablacion)
    mask_area_ablacion = mask_pixels_ablacion * area_pixel

    balance_ablac_vol_1 = (ablacion['alos'] - ablacion['srtm']).sum() * area_pixel * dens_hielo
    balance_ablac_maea_1 = balance_ablac_vol_1 / mask_area_ablacion / dens_agua / años1

    balance_ablac_vol_2 = (ablacion['tandem'] - ablacion['alos']).sum() * area_pixel * dens_hielo
    balance_ablac_maea_2 = balance_ablac_vol_2 / mask_area_ablacion / dens_agua / años2

    return balance_ablac_maea_1, balance_ablac_maea_2

def calcular_equivalente_nivel_lago(ablacion, area_pixel, dens_hielo, dens_agua, area_lago):
    """
    Calcula el equivalente en nivel del lago (LLE) para los periodos indicados.
    """
    ab_vol_1 = (ablacion['alos'] - ablacion['srtm']).sum() * area_pixel
    ab_vol_2 = (ablacion['tandem'] - ablacion['alos']).sum() * area_pixel

    LLE_1 = ab_vol_1 / area_lago * dens_hielo / dens_agua * (-1000)
    LLE_2 = ab_vol_2 / area_lago * dens_hielo / dens_agua * (-1000)

    return LLE_1, LLE_2

# Main Routine

ruta_csv = input("Ingrese la ruta al archivo CSV + Enter: ")
print("=============================================================================== ")
print("\033[1mCálculo de Balance De Masa:\033[0m")

ablacion = cargar_datos(ruta_csv)

area_pixel = 31 * 31  # [m2]
dens_hielo = 900  # densidad promedio hielo [kg/m3]
dens_agua = 1000  # densidad agua [kg/m3]
SRTM = 2000
ALOS = 2009
TANDEM = 2015
area_lago = 892000000  # [m2]

balance_ablac_maea_1, balance_ablac_maea_2 = calcular_balance_masa(
    ablacion, area_pixel, dens_hielo, dens_agua, SRTM, ALOS, TANDEM)

print("=============================================================================== ")
print("\033[1mBalance ablación neto anual entre 2000 y 2009 [mae]:\033[0m {:.4f}".format(balance_ablac_maea_1))
print("\033[1mBalance ablación neto anual entre 2009 y 2015 [mae]:\033[0m {:.4f}".format(balance_ablac_maea_2))
print("\033[1mBalance ablación neto anual entre 2000 y 2015 [mae]:\033[0m {:.4f}".format(balance_ablac_maea_1 + balance_ablac_maea_2))

LLE_1, LLE_2 = calcular_equivalente_nivel_lago(ablacion, area_pixel, dens_hielo, dens_agua, area_lago)

print("\033[1mEquivalente sobre nivel del lago entre 2000 y 2009 [mm]:\033[0m {:.4f}".format(LLE_1))
print("\033[1mEquivalente sobre nivel del lago entre 2009 y 2015 [mm]:\033[0m {:.4f}".format(LLE_2))
print("\033[1mEquivalente sobre nivel del lago entre 2000 y 2015 [mm]:\033[0m {:.4f}".format(LLE_1 + LLE_2))
