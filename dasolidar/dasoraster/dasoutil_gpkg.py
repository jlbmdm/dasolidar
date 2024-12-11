# -*- coding: utf-8 -*-
'''
/***************************************************************************
        begin                : 2024-12-10
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jose Bengoa
        email                : dasolidar@gmail.com
 ***************************************************************************/
'''

import os
import math
import json
import math
import time
from datetime import datetime

from osgeo import ogr, osr


driver_gpkg = ogr.GetDriverByName('GPKG')

dict_nombres_variables_dasometricas = {
    'Volumen de madera (fustes)': 'VCC',
    'Diámetro medio (cuadrático)': 'DCM',
    'Número de pies por hectárea (densidad)': 'Npies',
    'Área basimétrica': 'Abas',
    'Crecimiento anual en volumen': 'IAVC',
    'Biomasa aérea': 'BA',
    'Volumen de leñas': 'VLE',
    'Altura dominante lidar (es una métrica lidar)': 'Hdom',
}
dict_nombres_variables_dasometricas_inverso = {}
for key, variable_dasometrica in dict_nombres_variables_dasometricas.items():
    dict_nombres_variables_dasometricas_inverso[variable_dasometrica] = key
dict_capas_variables_dasometricas = {
    'VolumenMadera_m3_ha': 'VCC',
    'DiamMed_cm': 'DCM',
    'NumPies_ha': 'Npies',
    'AreaBasimetrica_m2_ha': 'Abas',
    'CrecimientoVolumenMadera_m3_ha.año': 'IAVC',
    'BiomasaAerea_t_ha': 'BA',
    'VolumenLeñas_m3_ha': 'VLE',
    'AlturaDominanteLidar_m': 'alt95',
}
dict_capas_variables_dasometricas_inverso = {}
for key, variable_dasometrica in dict_capas_variables_dasometricas.items():
    dict_capas_variables_dasometricas_inverso[variable_dasometrica] = key
dict_capas_metricas_lidar = {
    'AlturaDominanteLidar_m': 'alt95',
    'Cob5m_PRT_PNOA2': 'cob5m',
    'Cob3m_PRT_PNOA2': 'cob3m',
    'CobEstr_MidHD_TopHD_TLR_PNOA2': 'c_sup',
    'CobEstr_200cm_MidHD_TLR_PNOA2': 'c_med',
    'CobEstr_050cm_200cm_TLR_PNOA2': 'c_inf',
    'CobEstrDe0025a0150cm_TLR_PNOA2': 'c_st1',
    'CobEstrDe0150a0250cm_TLR_PNOA2': 'c_st2',
    'CobEstrDe0250a0500cm_TLR_PNOA2': 'c_st3',
}
dict_capas_metricas_lidar_inverso = {}
for key, variable_dasometrica in dict_capas_metricas_lidar.items():
    dict_capas_metricas_lidar_inverso[variable_dasometrica] = key


def codifica_variable_dasometrica(variable_aportada):
    if variable_aportada in dict_nombres_variables_dasometricas:
        cod_variable_dasometrica = dict_nombres_variables_dasometricas[variable_aportada]
    elif variable_aportada in dict_capas_variables_dasometricas:
        cod_variable_dasometrica = dict_capas_variables_dasometricas[variable_aportada]
    elif variable_aportada in dict_capas_metricas_lidar:
        cod_variable_dasometrica = dict_capas_metricas_lidar[variable_aportada]
    else:
        cod_variable_dasometrica = variable_aportada
    return cod_variable_dasometrica


def componer_geodata(
        usuario_actual,
        tipo_consulta,
        x_consulta,
        y_consulta,
        parcela_circular,
        radio_parcela,
        rodal_hectareas,
        layer_raster_XXX_name_txt,
        medicion_dasolidar,
        datos_recibidos='',
        obs_txt_multi_linea_etiquetado='',
        obs_txt_multi_linea_sinretornos='',
        obs_lista_lineas_sinetiquetar=[],  #  No lo uso
    ):
    hoy_AAAAMMDD = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
    ahora_HHMMSS = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    [especie_aportada, variable_aportada, medicion_aportada, unidad_aportada, publicar_datos, fiabilidad_datos] = datos_recibidos

    cod_variable_dasometrica = codifica_variable_dasometrica(variable_aportada)

    if not obs_txt_multi_linea_sinretornos:
        obs_txt_multi_linea_sinretornos = ''
        for num_linea, mi_linea in enumerate(obs_txt_multi_linea_etiquetado):
            # list_linea = str(mi_linea.split(';')[2:])
            # txt_linea = ''
            # for t_linea in list_linea:
            #     txt_linea += t_linea.replace('\r\n', ' ').replace('\n', ' ')
            if len(mi_linea) > 5 and mi_linea[5] == ';':
                txt_linea = mi_linea[6:].replace('\r\n', ' -/- ').replace('\n', ' -/- ')
            elif len(mi_linea) > 7:
                txt_linea = mi_linea[7:].replace('\r\n', ' -/- ').replace('\n', ' -/- ')
            else:
                txt_linea = mi_linea.replace('\r\n', ' -/- ').replace('\n', ' -/- ')
            if ' -/- ' in txt_linea:
                obs_txt_multi_linea_sinretornos += txt_linea
            else:
                obs_txt_multi_linea_sinretornos += f'{txt_linea} -/- '
        obs_txt_multi_linea_sinretornos = obs_txt_multi_linea_sinretornos.replace('\r\n', ' -/- ').replace('\n', ' -/- ')

    dict_geodata = {
        'x_parcela': float(x_consulta),
        'y_parcela': float(y_consulta),
        'Usuario332': usuario_actual,
        'FechaEntrada_AAAAMMDD': hoy_AAAAMMDD,
        'VariableAportada': cod_variable_dasometrica,
        'UnidadAportada': unidad_aportada,
        'EspecieAportada': especie_aportada[-3:-1],
        'CapaDasolidar': layer_raster_XXX_name_txt,
        'MedicionDasolidar': float(medicion_dasolidar),
        'fiabilidad_datos': int(fiabilidad_datos),
        'Observaciones': obs_txt_multi_linea_sinretornos,
    }
    # if medicion_aportada.isdigit(): -> no conisdera digit el . y ,
    # En origen es texto; admito decimales con '.' y con ',' 
    medicion_aportada = medicion_aportada.replace(',', '.')
    try:
        dict_geodata['MedicionAportada'] = float(medicion_aportada)
    except:
        dict_geodata['MedicionAportada'] = 0.0

    if tipo_consulta == 'parcela':
        if parcela_circular == 'False':
            dict_geodata['tipo_recinto'] = 'parcelaCuadrada'
        else:
            dict_geodata['tipo_recinto'] = 'parcelaCircular'
        try:
            dict_geodata['RadioParcela'] = float(radio_parcela)
        except:
            dict_geodata['RadioParcela'] = 15.0
        dict_geodata['SuperficieRodal_ha'] = 0.0
    elif tipo_consulta == 'rodal':
        dict_geodata['tipo_recinto'] = 'rodal'
        dict_geodata['RadioParcela'] = 0.0
        try:
            dict_geodata['SuperficieRodal_ha'] = float(rodal_hectareas)
        except:
            dict_geodata['SuperficieRodal_ha'] = 0
    return dict_geodata

def crear_circulo(x, y, radio, num_puntos=100):
    puntos = []
    for i in range(num_puntos):
        angulo = 2 * math.pi * i / num_puntos  # Dividir el círculo en segmentos
        punto_x = x + radio * math.cos(angulo)
        punto_y = y + radio * math.sin(angulo)
        puntos.append((punto_x, punto_y))
    return puntos

def crear_cuadrado(x, y, lado):
    half_side = lado / 2
    puntos = [
        (x - half_side, y - half_side),  # Esquina inferior izquierda
        (x + half_side, y - half_side),  # Esquina inferior derecha
        (x + half_side, y + half_side),  # Esquina superior derecha
        (x - half_side, y + half_side),  # Esquina superior izquierda
        (x - half_side, y - half_side)   # Cerrar el cuadrado
    ]
    return puntos

def guardar_parcela_en_gpkg(
        geopackage_filepath_all,
        tipo_geodata='parcela',
        dicts_geodata=[{}],
        geojson_path=None,
        # publicar_datos=False,
    ):
    # if tipo_geodata == 'parcela':
    #     layer_name = 'parcelas'
    # elif tipo_geodata == 'rodal':
    #     layer_name = 'rodales'

    geopackage_filepath_ok = []
    for num_geopack, mi_geopackage_filepath in enumerate(geopackage_filepath_all):
        if os.path.exists(mi_geopackage_filepath):
            geopackage_filepath_ok.append(mi_geopackage_filepath)
    geodata_source_all = [None] * len(geopackage_filepath_ok)
    for num_geopack, mi_geopackage_filepath in enumerate(geopackage_filepath_ok):
        try:
            geodata_source_all[num_geopack] = driver_gpkg.Open(mi_geopackage_filepath, 1)  # 1 significa que abrimos en modo de escritura
        except:
            print(f'Error al abrir el GeoPackage {mi_geopackage_filepath}')
            continue
        if geodata_source_all[num_geopack] is None:
            print(f'No se pudo abrir el GeoPackage {mi_geopackage_filepath}')
            continue

    if any(x is not None for x in geodata_source_all):
        for num_geosource, geodata_source_ in enumerate(geodata_source_all):
            if geodata_source_ is None:
                continue
            mi_geopackage_filepath = geopackage_filepath_ok[num_geosource]
            # Obtener la capa existente -------> Capa de puntos
            layer_name1 = 'parcelas'
            layer_name2 = 'parcela'
            mi_layer = geodata_source_.GetLayer(layer_name1)
            if mi_layer is None:
                mi_layer = geodata_source_.GetLayer(layer_name2)
                layer_name = layer_name2
            else:
                layer_name = layer_name1
            if mi_layer is None:
                print(f'El gpkg {mi_geopackage_filepath} no tiene la capa {layer_name1} ni {layer_name2}')
                geodata_source_ = None
            else:
                for mi_parcela_rodal in dicts_geodata:
                    # Guardo el punto
                    punto = ogr.Geometry(ogr.wkbPoint)
                    punto.AddPoint(mi_parcela_rodal['x_parcela'], mi_parcela_rodal['y_parcela'])
                    new_feature = ogr.Feature(mi_layer.GetLayerDefn())
                    new_feature.SetGeometry(punto)
                    lista_campos = list(mi_parcela_rodal.keys())
                    try:
                        lista_campos.remove('x_parcela')
                        lista_campos.remove('y_parcela')
                        # lista_campos.remove('RadioParcela')
                        # lista_campos.remove('SuperficieRodal_ha')
                    except ValueError as e:
                        print(f"Error al eliminar claves: {e}")
                    try:
                        for mi_campo in lista_campos:
                            campo_index = new_feature.GetFieldIndex(mi_campo)
                            if campo_index != -1:
                                # if mi_campo == 'tipo_recinto':
                                #     if tipo_geodata == 'parcela':
                                #         if mi_parcela_rodal['tipo_recinto'] == 'parcelaCircular':
                                #             new_feature.SetField('tipo_recinto', 'parcelaCircular')
                                #         else:
                                #             new_feature.SetField('tipo_recinto', 'parcelaCuadrada')
                                #     else:
                                #         new_feature.SetField('tipo_recinto', tipo_geodata)
                                #     continue
                                #     # new_feature.SetField('tipo_recinto', tipo_geodata)
                                new_feature.SetField(mi_campo, mi_parcela_rodal[mi_campo])
                                # print(f"Campo '{mi_campo}' encontrado en la posición {campo_index}.")
                            else:
                                print(f'El campo "{mi_campo}" no existe en la capa {layer_name}.')
                    except ValueError as e:
                        print(f"Error al guardar campos en la capa {layer_name}: {e}")
                    # Añadir la característica a la capa
                    try:
                        mi_layer.CreateFeature(new_feature)
                    except ValueError as e:
                        print(f"Error al crear el nuevo registro de punto en la capa {layer_name}: {e}")
                    # Limpiar la característica
                    new_feature = None

            # Obtener la capa existente -------> Capa de poligonos
            layer_name1 = 'rodal'
            layer_name2 = 'rodales'
            mi_layer = geodata_source_.GetLayer(layer_name1)
            if mi_layer is None:
                mi_layer = geodata_source_.GetLayer(layer_name2)
                layer_name = layer_name2
            else:
                layer_name = layer_name1
            if mi_layer is None:
                print(f'El gpkg {mi_geopackage_filepath} no tiene la capa {layer_name1} ni {layer_name2}')
                geodata_source_ = None
                continue
            for mi_parcela_rodal in dicts_geodata:
                # Guardo la parcela
                if tipo_geodata == 'parcela':
                    if mi_parcela_rodal['tipo_recinto'] == 'parcelaCircular':
                        # Crear los puntos del círculo
                        puntos_parcela = crear_circulo(
                            mi_parcela_rodal['x_parcela'],
                            mi_parcela_rodal['y_parcela'],
                            mi_parcela_rodal['RadioParcela'],
                        )
                    else:
                        # Crear un cuadrado
                        puntos_parcela = crear_cuadrado(
                            mi_parcela_rodal['x_parcela'],
                            mi_parcela_rodal['y_parcela'],
                            mi_parcela_rodal['RadioParcela'] * 2  # Usar el radio como la mitad del lado
                        )

                    # Crear la geometría del polígono
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    for punto in puntos_parcela:
                        ring.AddPoint(punto[0], punto[1])
                    ring.CloseRings()
                    poligono = ogr.Geometry(ogr.wkbPolygon)
                    poligono.AddGeometry(ring)
                    multipoligono = ogr.Geometry(ogr.wkbMultiPolygon)
                    multipoligono.AddGeometry(poligono)
                    # Crear una nueva característica (feature)
                    new_feature = ogr.Feature(mi_layer.GetLayerDefn())
                    new_feature.SetGeometry(multipoligono)

                    lista_campos = list(mi_parcela_rodal.keys())
                    try:
                        lista_campos.remove('x_parcela')
                        lista_campos.remove('y_parcela')
                        # lista_campos.remove('RadioParcela')
                        # lista_campos.remove('SuperficieRodal_ha')
                    except ValueError as e:
                        print(f"Error al eliminar claves: {e}")
                    try:
                        for mi_campo in lista_campos:
                            campo_index = new_feature.GetFieldIndex(mi_campo)
                            if campo_index != -1:
                                # if mi_campo == 'tipo_recinto':
                                #     if mi_parcela_rodal['tipo_recinto'] == 'parcelaCircular':
                                #         new_feature.SetField('tipo_recinto', 'parcelaCircular')
                                #     else:
                                #         new_feature.SetField('tipo_recinto', 'parcelaCuadrada')
                                #     continue
                                new_feature.SetField(mi_campo, mi_parcela_rodal[mi_campo])
                                # print(f"Campo '{mi_campo}' encontrado en la posición {campo_index}.")
                            else:
                                print(f'El campo "{mi_campo}" no existe en la capa {layer_name}.')
                    except ValueError as e:
                        print(f"Error al guardar campos en la capa {layer_name}: {e}")
                    # Añadir la característica a la capa
                    try:
                        mi_layer.CreateFeature(new_feature)
                    except ValueError as e:
                        print(f"Error al crear el nuevo registro de poligono en la capa {layer_name}: {e}")
                    # Limpiar la característica
                    new_feature = None

                elif tipo_geodata == 'rodal':
                    # Abrir el archivo GeoJSON
                    if geojson_path is None or not geojson_path:
                        print('No hay fichero adjunto. Tipo de dato aportado: {tipo_geodata}.')
                        geojson_data_source = None
                    else:
                        # Esto no corrije el mensaje de "ERROR 1: PROJ: proj_create: no database context specified"
                        manipular_crs = False
                        quitar_doble_dos_puntos = False
                        quitar_crs = False
                        asignar_crs_EPSG25830 = False
                        if manipular_crs:
                            # Verificar el CRS en el archivo GeoJSON
                            with open(geojson_path, 'r', encoding='utf-8') as f:
                                geojson_content = json.load(f)
                            # Ubicación de mi proj: C:\conda\py39\envs\clid2023\Library\share\proj
                            # Comprobar y corregir el CRS
                            if 'crs' in geojson_content:
                                if quitar_doble_dos_puntos:
                                    crs = geojson_content['crs']
                                    if 'properties' in crs and 'name' in crs['properties']:
                                        crs_name = crs['properties']['name']
                                        if '::' in crs_name:
                                            print(f'CRS encontrado con doble dos puntos: {crs_name}')
                                            crs_name = crs_name.replace('::', ':')
                                            print(f'CRS corregido: {crs_name}')
                                            # Actualizar el CRS en el contenido
                                            crs['properties']['name'] = crs_name
                                # Elimino la clave 'crs'
                                if quitar_crs:
                                    if 'crs' in geojson_content:
                                        del geojson_content['crs']
                                        print("Sección 'crs' eliminada del GeoJSON.")
                                if asignar_crs_EPSG25830:
                                    # Asignar el nuevo CRS (EPSG:25830)
                                    geojson_content['crs'] = {
                                        "type": "name",
                                        "properties": {
                                            "name": "urn:ogc:def:crs:EPSG:25830"
                                        }
                                    }
                            # Guardo el GeoJSON corregido
                            with open(geojson_path, 'w', encoding='utf-8') as f:
                                json.dump(geojson_content, f, indent=4)  # Usar indent=4 para una mejor legibilidad

                        geojson_driver = ogr.GetDriverByName('GeoJSON')
                        geojson_data_source = geojson_driver.Open(geojson_path, 0)  # 0 significa que abro en modo de solo lectura

                    if geojson_data_source is None:
                        print('No se pudo abrir el archivo GeoJSON {geojson_path}.')
                    else:
                        # Obtener la capa del GeoJSON
                        geojson_layer = geojson_data_source.GetLayer()

                        # # Iterar sobre las características del GeoJSON y añadirlas a la capa del GeoPackage
                        for mi_feature in geojson_layer:
                            # Crear una nueva característica (feature) para la capa del GeoPackage
                            new_feature = ogr.Feature(mi_layer.GetLayerDefn())
                            new_feature.SetGeometry(mi_feature.GetGeometryRef())

                            # # Podría copiar los campos adicionales que llegan en el GeoJSON, pero son variados
                            for campo_origen in mi_feature.keys():
                                if campo_origen == 'C_MON_ID' or campo_origen == 'MONT' or campo_origen == 'MONTE_LD':
                                    # Numero de monte en las capas:
                                    # mup_ex_etrs89         -> MONT
                                    # montes_ordenados_CyL  -> MONT y MONTE_LD
                                    # RODAL                 -> C_MON_ID
                                    campo_destino = 'C_MON_ID'
                                    campo_index = new_feature.GetFieldIndex(campo_destino)
                                    if campo_index != -1:
                                        new_feature.SetField(campo_destino, mi_feature.GetField(campo_origen))
                                else:
                                    pass
                            if False:
                                target_srs = osr.SpatialReference()
                                target_srs.ImportFromEPSG(25830)
                                # Obtener la geometría del GeoJSON
                                geom = mi_feature.GetGeometryRef()
                                # Obtener el sistema de referencia de la geometría
                                source_srs = geom.GetSpatialReference()
                                # Transformar la geometría al CRS de la capa del GeoPackage si es necesario
                                if source_srs is not None and not source_srs.IsSame(target_srs):
                                    transform = osr.CoordinateTransformation(source_srs, target_srs)
                                    geom.Transform(transform)  # Transformar la geometría
                                # Establecer la geometría transformada en la nueva característica
                                new_feature.SetGeometry(geom)

                            lista_campos = list(mi_parcela_rodal.keys())
                            try:
                                lista_campos.remove('x_parcela')
                                lista_campos.remove('y_parcela')
                                # lista_campos.remove('RadioParcela')
                                # lista_campos.remove('SuperficieRodal_ha')
                            except ValueError as e:
                                print(f"Error al eliminar claves: {e}")
                                geodata_source_ = None
                                return
                            try:
                                for mi_campo in lista_campos:
                                    campo_index = new_feature.GetFieldIndex(mi_campo)
                                    if campo_index != -1:
                                        # if mi_campo == 'tipo_recinto':
                                        #     new_feature.SetField('tipo_recinto', tipo_geodata)
                                        #     continue
                                        new_feature.SetField(mi_campo, mi_parcela_rodal[mi_campo])
                                        # print(f"Campo '{mi_campo}' encontrado en la posición {campo_index}.")
                                    else:
                                        print(f'El campo "{mi_campo}" no existe en la capa {layer_name}.')
                            except ValueError as e:
                                print(f"Error al guardar campos en la capa {layer_name}: {e}")
                            # Añadir la característica a la capa
                            mi_layer.CreateFeature(new_feature)
                            # Limpiar la característica
                            new_feature = None

            # Cerrar el GeoPackage
            geodata_source_ = None
            print(f'Datos de parcela añadidos correctamente a {os.path.basename(mi_geopackage_filepath)} ({num_geosource + 1} de {len(geodata_source_all)})')
