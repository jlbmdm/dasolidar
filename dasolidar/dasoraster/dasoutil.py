# -*- coding: UTF-8 -*-
import os
import math
import ast
import pandas as pd
# import sys
# import subprocess


# import win32com.client
# import requests

# def enviar_correo_graph(destinatario, asunto, cuerpo):
#     url = 'https://graph.microsoft.com/v1.0/me/sendMail'
#     headers = {
#         'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
#         'Content-Type': 'application/json'
#     }
#     email_data = {
#         "message": {
#             "subject": asunto,
#             "body": {
#                 "contentType": "Text",
#                 "content": cuerpo
#             },
#             "toRecipients": [
#                 {
#                     "emailAddress": {
#                         "address": destinatario
#                     }
#                 }
#             ]
#         }
#     }
#     response = requests.post(url, headers=headers, json=email_data)
#     if response.status_code == 202:
#         print(f'Correo enviado a {destinatario}')
#     else:
#         print(f'Error al enviar el correo: {response.status_code} - {response.text}')


# def enviar_correo(destinatario, asunto, cuerpo):
#     try:
#         outlook = win32com.client.Dispatch('Outlook.Application')
#         mail = outlook.CreateItem(0)  # 0 representa un correo
#         mail.To = destinatario
#         mail.Subject = asunto
#         mail.Body = cuerpo
#         mail.Send()
#         print(f'Correo enviado a {destinatario}')
#     except Exception as e:
#         print(f'Error al enviar el correo: {e}')

# # Ejemplo de uso
# try:
#     enviar_correo('benmarjo@jcyl.es', 'Asunto del correo1', 'Cuerpo del correo1')
# except:
#     print(f'No funciona outlook clásico')
#     enviar_correo_graph('benmarjo@jcyl.es', 'Asunto del correo2', 'Cuerpo del correo2')



#    # Ejemplo de uso

# quit()



import numpy as np
# from osgeo import gdal

# from qgis.utils import iface
from qgis.core import (
    # Qgis,
    # QgsApplication,
    # QgsMessageLog,
    QgsGeometry,
    QgsProject,
    # QgsSettings,
    # QgsVectorLayer,
    # QgsRasterLayer,
    QgsRectangle,
    QgsPointXY,
    # QgsRasterBandStats,
    QgsRaster,
    # QgsRasterDataProvider,
    # QgsRasterBlock,
    QgsFeatureRequest,
)
# from qgis.analysis import QgsZonalStatistics

PLUGIN_DIR = os.path.dirname(__file__)
SEP_CSV_INPUT = '\t'
SEP_CSV_OUT = '\t'
SEP_CSV_DSLD = '\t'
VERBOSE = False


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


def leer_csv_codigos1():
    ruta_codelists_local1 = os.path.join(PLUGIN_DIR, 'resources/data/codelist')
    ruta_codelists_local2 = os.path.join(PLUGIN_DIR, 'dasoraster/resources/data/codelist')
    mfe25cyl_sp = os.path.join(ruta_codelists_local1, 'mfe25cyl_sp.csv')
    if not os.path.exists(mfe25cyl_sp):
        print(f'betaraster-> No se encuentra: {mfe25cyl_sp}')
        mfe25cyl_sp = os.path.join(ruta_codelists_local2, 'mfe25cyl_sp.csv')
    dict_spp_mfe25cyl = {}
    if os.path.exists(mfe25cyl_sp):
        try:
            with open(mfe25cyl_sp, mode='r', encoding='utf-8') as my_list:
                lista_spp_mfe25cyl = my_list.readlines()
            lista_spp_num = [int(mi_sp.split(SEP_CSV_DSLD)[0]) for mi_sp in lista_spp_mfe25cyl]
            for mi_sp in lista_spp_mfe25cyl:
                list_sp = (mi_sp.rstrip('\n')).split(SEP_CSV_DSLD)
                dict_spp_mfe25cyl[int(list_sp[0])] = list_sp[1:]
            # print(f'betaraster-> Lista de especies leida ok: {mfe25cyl_sp}')
            # print(f'\tRebollo: {dict_spp_mfe25cyl[43]}')
        except:
            print(f'betaraster-> Error al leer la lista de especies: {mfe25cyl_sp}')
    else:
        print(f'betaraster-> No se encuentra: {mfe25cyl_sp}')
    return dict_spp_mfe25cyl


# def leer_csv_codigos2():
#     ruta_codelists_red = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$\dasoLidar\varios\modelos&ajustes\codelist'
#     ruta_codelists_local = os.path.join(PLUGIN_DIR, 'resources/data/codelist')
#     rutas_codelists = [ruta_codelists_red, ruta_codelists_local]

#     # _____________________________________________________________________________
#     for ruta_codelists in rutas_codelists:
#         cod2L_nSP_file_name = os.path.join(ruta_codelists, 'cod2L_nSP.csv')
#         if os.path.exists(cod2L_nSP_file_name):
#             break
#     dict_cod2L_nSP = {}
#     dict_nSP_cod2L = {}
#     if os.path.exists(cod2L_nSP_file_name):
#         cod2L_nSP_df = pd.read_csv(
#             cod2L_nSP_file_name,
#             header=0,
#             sep=SEP_CSV_INPUT,
#             encoding='utf-8'
#         )
#         if VERBOSE:
#             print(f'\nLista valores de {cod2L_nSP_file_name}')
#         for index, mi_row in cod2L_nSP_df.iterrows():
#             if VERBOSE:
#                 print(f'índice: {index}, {mi_row["cod2L"]} {mi_row["nSP"]}')
#             dict_cod2L_nSP[mi_row['cod2L']] = mi_row['nSP']
#             dict_nSP_cod2L[mi_row['nSP']] = mi_row['cod2L']
#     # =========================================================================
#     for ruta_codelists in rutas_codelists:
#         esp_MFE_IFN_file_name = os.path.join(ruta_codelists, 'MFE_IFN_SP_correspondencias.csv')
#         if os.path.exists(esp_MFE_IFN_file_name):
#             break
#     dict_esp_nsp_equi = {}
#     dict_esp_cod2l_equi = {}
#     if os.path.exists(esp_MFE_IFN_file_name):
#         esp_MFE_IFN_df = pd.read_csv(
#             esp_MFE_IFN_file_name,
#             header=0,
#             sep=SEP_CSV_INPUT,
#             encoding='utf-8'
#         )
#         campo_esp_orig = 'nSP1'
#         campo_esp_equi = 'nSPeq'
#         campo_esp_name = 'Especie'
#         campo_esp_cod2L = 'Cod2L'
#         lista_esp_lidar_num = esp_MFE_IFN_df[campo_esp_equi].unique()  #  <class 'numpy.ndarray'>
#         # lista_esp_lidar_cod = esp_MFE_IFN_df[campo_esp_cod2L].unique()  #  <class 'numpy.ndarray'>
#         esp_lidar_num_df = esp_MFE_IFN_df[esp_MFE_IFN_df[campo_esp_orig].isin(lista_esp_lidar_num)]
#         if VERBOSE:
#             print(f'\nLista de especies seleccionadas para dasoLidar recogidas en {esp_MFE_IFN_file_name}')
#             print(esp_lidar_num_df[[campo_esp_orig, campo_esp_name]])

#         for mi_esp_lidar in lista_esp_lidar_num:
#             lista_esp_equi_nSP1 = esp_MFE_IFN_df[campo_esp_orig][esp_MFE_IFN_df[campo_esp_equi] == mi_esp_lidar].tolist()
#             lista_esp_equi_cod2L = esp_MFE_IFN_df[campo_esp_cod2L][esp_MFE_IFN_df[campo_esp_equi] == mi_esp_lidar].tolist()
#             dict_esp_nsp_equi[mi_esp_lidar] = lista_esp_equi_nSP1
#             dict_esp_cod2l_equi[mi_esp_lidar] = lista_esp_equi_cod2L
#             if mi_esp_lidar == 71:
#                 print(f'betaraster-> -------------> lista_esp_equi_nSP1: {lista_esp_equi_nSP1}; lista_esp_equi_cod2L: {lista_esp_equi_cod2L}')

#     lista_dict_codigos_estratos = (dict_zonas, dict_fechas, dict_cod_modelo)

#     lista_dict_codigos_especies = (dict_cod2L_nSP, dict_nSP_cod2L, dict_esp_cod2l_equi, dict_esp_nsp_equi)
#     return lista_dict_codigos_especies


def leer_csv_codigos3():
    ruta_codelists_red = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$\dasoLidar\varios\modelos&ajustes\codelist'
    ruta_codelists_local = os.path.join(PLUGIN_DIR, 'resources/data/codelist')
    rutas_codelists = [ruta_codelists_red, ruta_codelists_local]
    # =========================================================================
    for ruta_codelists in rutas_codelists:
        cod_modelo_file_name = os.path.join(ruta_codelists, 'ajustesLidar_usados_formateadosPython.csv')
        if os.path.exists(cod_modelo_file_name):
            break
    cod_modelo_df = pd.read_csv(
        cod_modelo_file_name,
        header=0,
        sep=SEP_CSV_INPUT,
        encoding='utf-8'
    )
    dict_cod_modelo = {}
    if os.path.exists(cod_modelo_file_name):
        campo_modelo_num = 'index'
        campo_modelo_txt = 'id_ajuste'
        campo_variable_explicada = 'variable_daso'
        campo_especie_asimilada_num = 'especie'
        campo_estratozona_txt = 'estrato'
        if VERBOSE:
            print(f'\nLista valores de {cod_modelo_file_name}')
        for index, mi_row in cod_modelo_df.iterrows():
            if VERBOSE:
                print(f"índice: {index}, {mi_row[campo_modelo_num]} {mi_row[campo_modelo_txt]}")
            mi_cod_num_modelo = mi_row[campo_modelo_num]
            if mi_cod_num_modelo in dict_cod_modelo.keys():
                dict_cod_modelo[mi_cod_num_modelo].append(
                    [
                        mi_row[campo_modelo_txt],
                        mi_row[campo_variable_explicada],
                        mi_row[campo_especie_asimilada_num],
                        mi_row[campo_estratozona_txt],
                    ]
                )
            else:
                dict_cod_modelo[mi_cod_num_modelo] = [
                        mi_row[campo_modelo_txt],
                        mi_row[campo_variable_explicada],
                        mi_row[campo_especie_asimilada_num],
                        mi_row[campo_estratozona_txt],
                    ]
        # print('dict_cod_modelo', dict_cod_modelo)
    # =========================================================================
    for ruta_codelists in rutas_codelists:
        zonas_lidar_file_name = os.path.join(ruta_codelists, 'zonasLidar.csv')
        if os.path.exists(zonas_lidar_file_name):
            break
    dict_zonas = {}
    if os.path.exists(zonas_lidar_file_name):
        zonas_lidar_df = pd.read_csv(
            zonas_lidar_file_name,
            header=0,
            sep=SEP_CSV_INPUT,
            encoding='utf-8'
        )
        campo_estrato_letra = 'EstratoLetra'
        campo_estrato_nombre = 'EstratoNombre'
        campo_estrato_numero = 'EstratoNumero'
        if VERBOSE:
            print(f'\nLista valores de {zonas_lidar_file_name}')
        for index, mi_row in zonas_lidar_df.iterrows():
            if VERBOSE:
                print(f"índice: {index}, {mi_row[campo_estrato_letra]} {mi_row[campo_estrato_nombre]} {ast.literal_eval(mi_row[campo_estrato_numero])}")
            dict_zonas[mi_row[campo_estrato_letra]] = [mi_row[campo_estrato_nombre], mi_row[campo_estrato_letra], ast.literal_eval(mi_row[campo_estrato_numero])]
    # =========================================================================
    for ruta_codelists in rutas_codelists:
        fecha_lidar_file_name = os.path.join(ruta_codelists, 'fechaLidar.csv')
        if os.path.exists(fecha_lidar_file_name):
            break
    fecha_lidar_df = pd.read_csv(
        fecha_lidar_file_name,
        header=0,
        sep=SEP_CSV_INPUT,
        encoding='utf-8'
    )
    dict_fechas = {}
    if os.path.exists(fecha_lidar_file_name):
        campo_fecha_num = 'fechaNum'
        campo_fecha_texto = 'fechaTexto'
        if VERBOSE:
            print(f'\nLista valores de {fecha_lidar_file_name}')
        for index, mi_row in fecha_lidar_df.iterrows():
            if VERBOSE:
                print(f"índice: {index}, {mi_row[campo_fecha_num]} {mi_row[campo_fecha_texto]}")
            cod_fecha_lidar = mi_row[campo_fecha_texto][: 7]
            if cod_fecha_lidar in dict_fechas.keys():
                dict_fechas[cod_fecha_lidar].append(mi_row[campo_fecha_num])
            else:
                dict_fechas[cod_fecha_lidar] = [mi_row[campo_fecha_num]]
        # print('dict_fechas', dict_fechas)
    # =========================================================================
    lista_dict_codigos_estratos = (dict_zonas, dict_fechas, dict_cod_modelo)
    return lista_dict_codigos_estratos


dict_spp_mfe25cyl = leer_csv_codigos1()
# lista_dict_codigos_especies =  leer_csv_codigos2()
# (dict_cod2L_nSP, dict_nSP_cod2L, dict_esp_cod2l_equi, dict_esp_nsp_equi) = lista_dict_codigos_especies
# lista_dict_codigos_estratos =  leer_csv_codigos3()
# (dict_zonas, dict_fechas, dict_cod_modelo) = lista_dict_codigos_estratos


def buscar_vector_mfe():
    # Parámetros de entrada
    capa_nombre_MFE_1 = 'MFE25CyL — mfe25cyl'
    capa_nombre_MFE_2 = 'mfe25cyl'
    capas_nombre_MFE = [capa_nombre_MFE_1, capa_nombre_MFE_2]
    capa_nombre_MFE_ok = capa_nombre_MFE_1
    capa_MFE_encontrada = False
    capa_MFE_vector_ok = None
    for capa_nombre_MFE in capas_nombre_MFE:
        capa_vector_MFE = QgsProject.instance().mapLayersByName(capa_nombre_MFE)

        if capa_vector_MFE:
            capa_MFE_vector_ok = capa_vector_MFE[0]  #  Usar la capa 'MFE' si está cargada
            capa_MFE_encontrada = True
            capa_nombre_MFE_ok = capa_nombre_MFE
            break
        else:
            print(f'betaraster-> Capa {capa_nombre_MFE_1} no encontrada')
    return capa_MFE_encontrada, capa_MFE_vector_ok, capa_nombre_MFE_ok

def buscar_raster_mfe():
    # Parámetros de entrada
    capa_nombre_mfe_sp1 = f'mfe25_nSP1'
    capa_nombre_mfe_sp2 = f'mfe25_nSP2'
    capa_nombre_mfe_spx = f'mfe25_O2_O1O2'
    capa_raster_mfe_sp1 = QgsProject.instance().mapLayersByName(capa_nombre_mfe_sp1)
    capa_raster_mfe_sp2 = QgsProject.instance().mapLayersByName(capa_nombre_mfe_sp2)
    capa_raster_mfe_spx = QgsProject.instance().mapLayersByName(capa_nombre_mfe_spx)
    capa_mfe_sp1_raster_ok = None
    capa_mfe_sp2_raster_ok = None
    capa_mfe_spx_raster_ok = None
    if capa_raster_mfe_sp1:
        capa_mfe_sp1_raster_ok = capa_raster_mfe_sp1[0]
        capa_mfe_sp1_encontrada = True
    else:
        capa_mfe_sp1_encontrada = False
        print(f'betaraster-> Capa {capa_nombre_mfe_sp1} no encontrada')
    if capa_raster_mfe_sp2:
        capa_mfe_sp2_raster_ok = capa_raster_mfe_sp2[0]
        capa_mfe_sp2_encontrada = True
    else:
        capa_mfe_sp2_encontrada = False
        print(f'betaraster-> Capa {capa_nombre_mfe_sp2} no encontrada')
    if capa_raster_mfe_spx:
        capa_mfe_spx_raster_ok = capa_raster_mfe_spx[0]
        capa_mfe_spx_encontrada = True
    else:
        capa_mfe_spx_encontrada = False
        print(f'betaraster-> Capa {capa_nombre_mfe_spx} no encontrada')
    return (
        capa_mfe_sp1_encontrada, capa_mfe_sp1_raster_ok, capa_nombre_mfe_sp1,
        capa_mfe_sp2_encontrada, capa_mfe_sp2_raster_ok, capa_nombre_mfe_sp2,
        capa_mfe_spx_encontrada, capa_mfe_spx_raster_ok, capa_nombre_mfe_spx,
    )

def identifica_esp_mfe(self_punto_click, capa_mfe_sp1_encontrada, capa_mfe_sp1_raster_ok):
    cod_num_mfe_ok = False
    if capa_mfe_sp1_encontrada:
        result_mfe_sp1 = capa_mfe_sp1_raster_ok.dataProvider().identify(self_punto_click, QgsRaster.IdentifyFormatValue)
        if result_mfe_sp1.isValid():
            try:
                # print(f'betaraster-> result_mfe_sp1.results()    ({type(result_mfe_sp1.results())}): {result_mfe_sp1.results()}')  #  dict
                # print(f'betaraster-> result_mfe_sp1.results()[1] ({type(result_mfe_sp1.results()[1])}): {result_mfe_sp1.results()[1]}')  #  ?
                if result_mfe_sp1.results()[1] is None:
                    cod_num_mfe_sp_ = 0
                else:
                    cod_num_mfe_sp_ = int(result_mfe_sp1.results()[1])  #  Acceder al valor del píxel
                    cod_num_mfe_ok = True
            except:
                cod_num_mfe_sp_ = 0  #  'noNumero'
                print(f'betaraster-> cod_num_mfe_sp_ error 1 ({type(result_mfe_sp1.results())}): {result_mfe_sp1.results()}')
        else:
            cod_num_mfe_sp_ = 0  #  'noValida'
            print(f'betaraster-> cod_num_mfe_sp_ error 2 ({type(result_mfe_sp1)}): {result_mfe_sp1}')
    else:
        cod_num_mfe_sp_ = 0  #  'noCapa'
        print(f'betaraster-> cod_num_mfe_sp_ error 3 capa_mfe_sp1_encontrada: {capa_mfe_sp1_encontrada}')

    if cod_num_mfe_ok:
        if cod_num_mfe_sp_ in dict_spp_mfe25cyl.keys():
            try:
                cod_2L_sp_ = dict_spp_mfe25cyl[cod_num_mfe_sp_][0]
                nombre_sp_ = dict_spp_mfe25cyl[cod_num_mfe_sp_][1]
                dasolidar_sp_ = dict_spp_mfe25cyl[cod_num_mfe_sp_][2]
                cod_num_txt_asimilada_sp_ = dict_spp_mfe25cyl[cod_num_mfe_sp_][3]
                # print(f'betaraster-> cod_sp ok ({type(cod_num_mfe_sp_)}): {cod_num_mfe_sp_} -> Asimilada: ({type(cod_num_txt_asimilada_sp_)}): {cod_num_txt_asimilada_sp_}')
            except:
                print(f'betaraster-> cod_sp error 1 ({type(cod_num_mfe_sp_)}): {cod_num_mfe_sp_}')
                cod_2L_sp_ = 'Xx'
                nombre_sp_ = 'Especie desconocida'
                dasolidar_sp_ = 'NO'
                cod_num_txt_asimilada_sp_ = '00'
        else:
            print(f'betaraster-> Atencion: especie no en el dict cod_num_mfe_sp_: ({type(cod_num_mfe_sp_)}): {cod_num_mfe_sp_} -> dict_spp_mfe25cyl.keys(): {dict_spp_mfe25cyl.keys()}')
            cod_2L_sp_ = 'Xx'
            nombre_sp_ = 'Especie desconocida'
            dasolidar_sp_ = 'NO'
            cod_num_txt_asimilada_sp_ = '00'
    else:
        cod_2L_sp_ = 'Xx'
        nombre_sp_ = 'Especie desconocida'
        dasolidar_sp_ = 'NO'
        cod_num_txt_asimilada_sp_ = '00'
    return (cod_num_mfe_sp_, cod_2L_sp_, nombre_sp_, dasolidar_sp_, cod_num_txt_asimilada_sp_)

def leer_raster_float(self_punto_click, capa_raster_float_encontrada, capa_raster_float_ok):
    valor_raster_ok = False
    if capa_raster_float_encontrada:
        result_mfe_sp1 = capa_raster_float_ok.dataProvider().identify(self_punto_click, QgsRaster.IdentifyFormatValue)
        if result_mfe_sp1.isValid():
            try:
                valor_raster_float = result_mfe_sp1.results()[1]  #  Acceder al valor del píxel
                valor_raster_ok = True
            except:
                valor_raster_float = 0.0
        else:
            valor_raster_float = 0.0
    else:
        valor_raster_float = 0.0
    return (valor_raster_float, valor_raster_ok)


def identifica_especies_mfe(punto_click, usar_mfe_raster=True):
    if usar_mfe_raster:
        (
            capa_mfe_sp1_encontrada, capa_mfe_sp1_raster_ok, capa_nombre_mfe_sp1,
            capa_mfe_sp2_encontrada, capa_mfe_sp2_raster_ok, capa_nombre_mfe_sp2,
            capa_mfe_spx_encontrada, capa_mfe_spx_raster_ok, capa_nombre_mfe_spx,
        ) = buscar_raster_mfe()
        (
            cod_num_mfe_sp1, cod_2L_sp1, nombre_sp1, dasolidar_sp1, cod_num_txt_asimilada_sp1
        ) = identifica_esp_mfe(punto_click, capa_mfe_sp1_encontrada, capa_mfe_sp1_raster_ok)
        (
            cod_num_mfe_sp2, cod_2L_sp2, nombre_sp2, dasolidar_sp2, cod_num_txt_asimilada_sp2
        ) = identifica_esp_mfe(punto_click, capa_mfe_sp2_encontrada, capa_mfe_sp2_raster_ok)

        (
            valor_raster_float, valor_raster_ok
        ) = leer_raster_float(punto_click, capa_mfe_spx_encontrada, capa_mfe_spx_raster_ok)
        (capa_MFE_encontrada, cod_num_especie, cod_2L_especie, nombre_especie) = (False, 0, 'Xx', 'Especie desconocida')

    else:
        # Podría usar el vectorial pero es mucho más lento
        capa_MFE_encontrada, capa_MFE_vector_ok, capa_MFE_ok = buscar_vector_mfe()
        # layer_selec = QgsProject.instance().mapLayersByName('cargar_nubeDePuntos_LidarPNOA2')
        buffer_size=0.001
        request = QgsFeatureRequest().setFilterRect(
            QgsRectangle(
                punto_click.x() - buffer_size,
                punto_click.y() - buffer_size,
                punto_click.x() + buffer_size,
                punto_click.y() + buffer_size
            )
        )
        # selected_features = capa_MFE_vector_ok.dataProvider().getFeatures(request)
        selected_features = capa_MFE_vector_ok.getFeatures(request)
        cod_num_especie = 1
        contador_teselas_totales = 0
        if selected_features:
            # Convierto el iterador a una lista para contar las características
            features_list = list(selected_features)
            num_features = len(features_list)
            if num_features != 1:
                print(f'betaraster-> Número de teselas MFE seleccionados-> {num_features} (debería ser una solo)')
            for feature in features_list:
                contador_teselas_totales += 1
                # Obtener el valor del campo COPC1
                cod_num_especie = feature['n_sp1']
                cod_2L_especie = feature['SP1']
                nombre_especie = feature['Especie1']
                break

            if cod_num_especie and cod_num_especie in dict_spp_mfe25cyl.keys():
                cod_2L_especie_ = dict_spp_mfe25cyl[cod_num_especie][0]
            else:
                cod_2L_especie_ = 'Xx'
        else:
            cod_num_especie = 0
            cod_2L_especie = 'Xx'
            cod_2L_especie_ = 'Xx'
            nombre_especie = 'Especie desconocida'
        print(f'betaraster-> cod_num_especie: {cod_num_especie}; cod_2L_especie: {cod_2L_especie}; {cod_2L_especie_}; nombre_especie: {nombre_especie}')
    return (
        (capa_mfe_sp1_encontrada, cod_num_mfe_sp1, cod_2L_sp1, nombre_sp1, dasolidar_sp1, cod_num_txt_asimilada_sp1),
        (capa_mfe_sp2_encontrada, cod_num_mfe_sp2, cod_2L_sp2, nombre_sp2, dasolidar_sp2, cod_num_txt_asimilada_sp2),
        (valor_raster_float, valor_raster_ok),
        (capa_MFE_encontrada, cod_num_especie, cod_2L_especie, nombre_especie),
    )



# ==============================================================================
def calcular_valor_medio_parcela_rodal(
        raster_layer,
        x_consulta,
        y_consulta,
        radio_parcela=15,
        parcela_circular=True,
        rodal_consulta=False,
        rodal_geom=None,
        buscar_esp_mfe=True,
        usar_mfe_raster=True,
    ):
    # Creo un círculo de consulta
    if rodal_consulta:
        consulta_geom = rodal_geom
    else:
        punto_consulta = QgsPointXY(x_consulta, y_consulta)
        consulta_circulo_geom = QgsGeometry.fromPointXY(punto_consulta).buffer(radio_parcela, 50)  #  Círculo de 50 segmentos
        consulta_cuadrado_bbox = consulta_circulo_geom.boundingBox()
        consulta_cuadrado_geom = QgsGeometry.fromRect(consulta_cuadrado_bbox)
        if parcela_circular:
            consulta_geom = consulta_circulo_geom
        else:
            consulta_geom = consulta_cuadrado_geom

    consulta_bbox = consulta_geom.boundingBox()
    print(f'betaraster-> calcular_valor_medio_parcela---> rodal_consulta: {rodal_consulta}')
    print(f'betaraster-> calcular_valor_medio_parcela---> consulta_geom:  {type(consulta_geom)}')
    print(f'betaraster-> calcular_valor_medio_parcela---> consulta_bbox:  {type(consulta_bbox)}')
    print(f'betaraster-> calcular_valor_medio_parcela---> Coord:          {consulta_bbox.xMinimum()} - {consulta_bbox.yMaximum()}')
    print(f'betaraster-> calcular_valor_medio_parcela---> Dimension:      {consulta_bbox.height()} x {consulta_bbox.width()}')
    print(f'betaraster-> calcular_valor_medio_parcela---> raster_layer:   {type(raster_layer)}')

    # Recorro los pixeles que tocan el rectángulo (extent_explora_pixels) incluye, con seguridad (los excede),
    # los píxeles cuyo centro está dentro de la geometría de consuilta (círculo o cuadrado)
    x_orig_explora_pixels = 10 * math.floor(consulta_bbox.xMinimum() / 10)
    y_orig_explora_pixels = 10 * math.ceil(consulta_bbox.yMaximum() / 10)
    rows = int(math.ceil(consulta_bbox.height() / raster_layer.rasterUnitsPerPixelY())) + 1
    cols = int(math.ceil(consulta_bbox.width() / raster_layer.rasterUnitsPerPixelX())) + 1
    extent_explora_pixels = QgsRectangle(
        x_orig_explora_pixels,
        y_orig_explora_pixels,
        x_orig_explora_pixels + (cols * raster_layer.rasterUnitsPerPixelY()),
        y_orig_explora_pixels - (rows * raster_layer.rasterUnitsPerPixelY())
    )
    # print(f'dasoutil-> Centro consulta: {x_consulta:0.1f}, {y_consulta:0.1f}')
    # print(f'dasoutil-> consulta_bbox: {consulta_bbox}')
    # print(f'dasoutil-> Centro retranqueado: {x_consulta:0.1f}, {y_consulta:0.1f}')
    # print(f'dasoutil-> extent_explora_pixels:  {extent_explora_pixels}')
    # print(f'dasoutil-> rows: {rows}; cols: {cols}')

    # Obtengo los datos ráster dentro del rectángulo de consulta (explora_pixels)
    raster_layer_provider = raster_layer.dataProvider()
    raster_layer_block = raster_layer_provider.block(1, extent_explora_pixels, cols, rows)

    recorte_previo = True
    if recorte_previo:
        (
            capa_mfe_sp1_encontrada, capa_mfe_sp1_raster_ok, capa_nombre_mfe_sp1,
            capa_mfe_sp2_encontrada, capa_mfe_sp2_raster_ok, capa_nombre_mfe_sp2,
            capa_mfe_spx_encontrada, capa_mfe_spx_raster_ok, capa_nombre_mfe_spx,
        ) = buscar_raster_mfe()
        if not capa_mfe_sp1_raster_ok is None:
            raster_mfe_sp1_provider = capa_mfe_sp1_raster_ok.dataProvider()
            raster_mfe_sp1_block = raster_mfe_sp1_provider.block(1, extent_explora_pixels, cols, rows)
        if not capa_mfe_sp2_raster_ok is None:
            raster_mfe_sp2_provider = capa_mfe_sp2_raster_ok.dataProvider()
            raster_mfe_sp2_block = raster_mfe_sp2_provider.block(1, extent_explora_pixels, cols, rows)
        if not capa_mfe_spx_raster_ok is None:
            raster_mfe_spx_provider = capa_mfe_spx_raster_ok.dataProvider()
            raster_mfe_spx_block = raster_mfe_spx_provider.block(1, extent_explora_pixels, cols, rows)

    # Extraer los valores de los píxeles dentro del círculo
    valores_selec = []
    dict_spp_mfe_sp1 = {}
    dict_spp_mfe_sp2 = {}
    num_puntos_leidos = 0
    for i in range(rows):
        for j in range(cols):
            x_pixel = x_orig_explora_pixels + (j + 0.5) * raster_layer.rasterUnitsPerPixelX()
            y_pixel = y_orig_explora_pixels - (i + 0.5) * raster_layer.rasterUnitsPerPixelY()
            punto_click_pixel = QgsPointXY(x_pixel, y_pixel)
            punto_interior = False
            if parcela_circular:
                if consulta_geom.contains(QgsGeometry.fromPointXY(punto_click_pixel)):
                    punto_interior = True
            else:
                if (
                        x_pixel >= consulta_bbox.xMinimum()
                        and x_pixel < consulta_bbox.xMaximum()
                        and y_pixel >= consulta_bbox.yMinimum()
                        and y_pixel < consulta_bbox.yMaximum()
                ):
                    punto_interior = True
            if not punto_interior:
                continue
            num_puntos_leidos += 1

            # print(f'betaraster-> punto_click_pixel 2: ({type(punto_click_pixel)}): {punto_click_pixel}')  #  (<class 'qgis._core.QgsPointXY'>): <QgsPointXY: POINT(520173 2)>
            if recorte_previo:
                if not capa_mfe_sp1_raster_ok is None:
                    valor_mfe_sp1 = raster_mfe_sp1_block.value(i, j)
                    # print(f'betaraster-> valor_mfe_sp1 ({type(valor_mfe_sp1)}): {valor_mfe_sp1} [noData: {raster_mfe_sp1_provider.sourceNoDataValue(1)}]')
                    if valor_mfe_sp1 == raster_mfe_sp1_provider.sourceNoDataValue(1):
                        cod_num_mfe_sp1 = 0
                    else:
                        try:
                            cod_num_mfe_sp1 = int(raster_mfe_sp1_block.value(i, j))
                        except:
                            cod_num_mfe_sp1 = -1
                    if not capa_mfe_sp2_raster_ok is None:
                        valor_mfe_sp2 = raster_mfe_sp2_block.value(i, j)
                        if valor_mfe_sp2 == raster_mfe_sp2_provider.sourceNoDataValue(1):
                            cod_num_mfe_sp2 = 0
                        else:
                            try:
                                cod_num_mfe_sp2 = int(raster_mfe_sp2_block.value(i, j))
                            except:
                                cod_num_mfe_sp2 = -1
                    else:
                        cod_num_mfe_sp2 = -1
                    try:
                        mfe_spx_valor = raster_mfe_spx_block.value(i, j)
                    except:
                        mfe_spx_valor = 0.0
                    if cod_num_mfe_sp1 in dict_spp_mfe_sp1.keys():
                        dict_spp_mfe_sp1[cod_num_mfe_sp1] += 1
                    else:
                        dict_spp_mfe_sp1[cod_num_mfe_sp1] = 1
                    if cod_num_mfe_sp2 in dict_spp_mfe_sp2.keys():
                        dict_spp_mfe_sp2[cod_num_mfe_sp2] += 1
                    else:
                        dict_spp_mfe_sp2[cod_num_mfe_sp2] = 1
            else:
                if num_puntos_leidos < 100:
                    if buscar_esp_mfe:
                        (
                            (capa_mfe_sp1_encontrada, cod_num_mfe_sp1, cod_2L_sp1, nombre_sp1, dasolidar_sp1, cod_num_txt_asimilada_sp1),
                            (capa_mfe_sp2_encontrada, cod_num_mfe_sp2, cod_2L_sp2, nombre_sp2, dasolidar_sp2, cod_num_txt_asimilada_sp2),
                            (valor_raster_float, valor_raster_ok),
                            (capa_MFE_encontrada, cod_num_especie, cod_2L_especie, nombre_especie),
                        ) = identifica_especies_mfe(punto_click_pixel, usar_mfe_raster=usar_mfe_raster)
                        if usar_mfe_raster:
                            capa_MFE_encontrada = capa_mfe_sp1_encontrada
                            cod_num_especie = cod_num_mfe_sp1
                            cod_2L_especie = cod_2L_sp1
                            nombre_especie = nombre_sp1
                        cod_num_asimilada_sp_ = int(cod_num_txt_asimilada_sp1)
                    else:
                        # Fuente: capa vectorial:
                        capa_MFE_encontrada = False
                        cod_num_especie = 0
                        cod_2L_especie = 'Xx'
                        nombre_especie = 'Especie desconocida'
                        # Fuente: capas raster:
                        (capa_mfe_sp1_encontrada, cod_num_mfe_sp1, cod_2L_sp1, nombre_sp1, dasolidar_sp1, cod_num_txt_asimilada_sp1) = (False, 0, 'Xx', 'Especie desconocida', 'NO', 0)
                        (capa_mfe_sp2_encontrada, cod_num_mfe_sp2, cod_2L_sp2, nombre_sp2, dasolidar_sp2, cod_num_txt_asimilada_sp2) = (False, 0, 'Xx', 'Especie desconocida', 'NO', 0)
                        (valor_raster_float, valor_raster_ok) = (0.0, False)
                        cod_num_asimilada_sp_ = int(cod_num_txt_asimilada_sp1)
                if cod_num_mfe_sp1 in dict_spp_mfe_sp1.keys():
                    dict_spp_mfe_sp1[cod_num_mfe_sp1] += 1
                else:
                    dict_spp_mfe_sp1[cod_num_mfe_sp1] = 1

            valor = raster_layer_block.value(i, j)
            if valor != raster_layer_provider.sourceNoDataValue(1):  # Ignorar valores NoData
                valores_selec.append(valor)

    print(f'betaraster-> dict_spp_mfe_sp1: {dict_spp_mfe_sp1}')
    # Calculo el valor medio
    if valores_selec:
        valor_medio = np.mean(valores_selec)
        if rodal_consulta:
            print(f'Valor medio rodal: {valor_medio:0.0f}')
        else:
            print(f'Valor med parcela: {valor_medio:0.0f}')
        print(f'Numero pixeles:    {len(valores_selec)}')
    else:
        valor_medio = -1
        print('No se encontraron valores válidos en el área de consulta.')

    return valor_medio, len(valores_selec), dict_spp_mfe_sp1, dict_spp_mfe_sp2

