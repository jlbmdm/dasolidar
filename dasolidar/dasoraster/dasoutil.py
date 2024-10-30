# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import math

import numpy as np

# from qgis.utils import iface
from qgis.core import (
    # Qgis,
    # QgsApplication,
    # QgsMessageLog,
    QgsGeometry,
    # QgsProject,
    # QgsSettings,
    # QgsVectorLayer,
    # QgsRasterLayer,
    QgsRectangle,
    QgsPointXY,
)

def identificar_usuario():
    # usuario_psutil = psutil.users()[0].name
    # usuario_psutil = psutil.users()
    usuario_env = ''
    usuario_profile = ''
    try:
        usuario_login = os.getlogin()
        print(f'Usuario_login ({type(usuario_login)}): {usuario_login}')
    except:
        usuario_login = None
        try:
            usuario_env = os.environ.get('USERNAME')
            print(f'Usuario_env ({type(usuario_env)}): {usuario_env}')
        except:
            usuario_env = None
            usuario_profile = os.path.expandvars("%userprofile%")[-8:].lower()
            print(f'Usuario_profile: {usuario_profile}')
    if isinstance(usuario_login, str) and len(usuario_login) == 8:
        usuario_actual = usuario_login.lower()
    elif isinstance(usuario_env, str) and len(usuario_env) == 8:
        usuario_actual = usuario_env.lower()
    elif isinstance(usuario_profile, str) and len(usuario_profile) == 8:
        usuario_actual = usuario_profile.lower()
    elif isinstance(usuario_login, str):
        usuario_actual = usuario_login.lower()
    elif isinstance(usuario_env, str):
        usuario_actual = usuario_env.lower()
    elif isinstance(usuario_profile, str):
        usuario_actual = usuario_profile.lower()
    else:
        usuario_actual = 'anonimo'
    return usuario_actual

# ==============================================================================
def calcular_valor_medio(raster_layer, x_consulta, y_consulta, radio_parcela=15, consultar_circulo=True):
    # Creo un círculo de consulta
    punto_central = QgsPointXY(x_consulta, y_consulta)
    consulta_circulo_geom = QgsGeometry.fromPointXY(punto_central).buffer(radio_parcela, 50)  #  Círculo de 50 segmentos
    consulta_cuadrado_bbox = consulta_circulo_geom.boundingBox()
    if consultar_circulo:
        consulta_geom = consulta_circulo_geom
    else:
        consulta_geom = consulta_cuadrado_bbox

    # Recorro los pixeles que tocan el rectángulo (extent_explora_pixels) incluye, con seguridad (los excede),
    # los píxeles cuyo centro está dentro de la geometría de consuilta (círculo o cuadrado)
    x_orig_explora_pixels = 10 * math.floor(consulta_cuadrado_bbox.xMinimum() / 10)
    y_orig_explora_pixels = 10 * math.ceil(consulta_cuadrado_bbox.yMaximum() / 10)
    rows = int(math.ceil(consulta_cuadrado_bbox.height() / raster_layer.rasterUnitsPerPixelY())) + 1
    cols = int(math.ceil(consulta_cuadrado_bbox.width() / raster_layer.rasterUnitsPerPixelX())) + 1
    extent_explora_pixels = QgsRectangle(
        x_orig_explora_pixels,
        y_orig_explora_pixels,
        x_orig_explora_pixels + (cols * raster_layer.rasterUnitsPerPixelY()),
        y_orig_explora_pixels - (rows * raster_layer.rasterUnitsPerPixelY())
    )
    # print(f'dasoutil-> Centro consulta: {x_consulta:0.1f}, {y_consulta:0.1f}')
    # print(f'dasoutil-> consulta_cuadrado_bbox: {consulta_cuadrado_bbox}')
    # print(f'dasoutil-> Centro retranqueado: {x_consulta:0.1f}, {y_consulta:0.1f}')
    # print(f'dasoutil-> extent_explora_pixels:  {extent_explora_pixels}')
    # print(f'dasoutil-> rows: {rows}; cols: {cols}')

    # Obtengo los datos ráster dentro del rectángulo de consulta (explora_pixels)
    provider = raster_layer.dataProvider()
    block = provider.block(1, extent_explora_pixels, cols, rows)

    # Extraer los valores de los píxeles dentro del círculo
    valores_selec = []
    for i in range(rows):
        for j in range(cols):
            x_pixel = x_orig_explora_pixels + (j + 0.5) * raster_layer.rasterUnitsPerPixelX()
            y_pixel = y_orig_explora_pixels - (i + 0.5) * raster_layer.rasterUnitsPerPixelY()
            punto_pixel = QgsPointXY(x_pixel, y_pixel)
            if consultar_circulo:
                if consulta_geom.contains(QgsGeometry.fromPointXY(punto_pixel)):
                    valor = block.value(i, j)
                    if valor != provider.sourceNoDataValue(1):  # Ignorar valores NoData
                        valores_selec.append(valor)
                # else:
                #     valor = -1
                # print(f'-->> {x_pixel}, {y_pixel} -> {valor}')
            else:
                if (
                        x_pixel >= consulta_cuadrado_bbox.xMinimum()
                        and x_pixel < consulta_cuadrado_bbox.xMaximum()
                        and y_pixel >= consulta_cuadrado_bbox.yMinimum()
                        and y_pixel < consulta_cuadrado_bbox.yMaximum()
                ):
                    valor = block.value(i, j)
                    if valor != provider.sourceNoDataValue(1):  # Ignorar valores NoData
                        valores_selec.append(valor)

    # Calculo el valor medio
    if valores_selec:
        valor_medio = np.mean(valores_selec)
        print(f'Valor medio: {valor_medio:0.0f}')
    else:
        valor_medio = -1
        print('No se encontraron valores válidos en el área de consulta.')

    return valor_medio, len(valores_selec)

