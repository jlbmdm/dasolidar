import os
import sys
import time
import datetime
# import subprocess
# import requests

import pdal
#import qgis
# #from qgis.core import *

# from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox
# from qgis.PyQt.QtGui import QDesktopServices
# from qgis.PyQt.QtCore import QUrl
# from qgis.core import QgsFeature
# from PyQt5.QtWidgets import QInputDialog, QLineEdit

# print('Argumentos:', sys.argv)
if len(sys.argv) > 1:
    list_lazFiles = sys.argv[1]
else:
    print('No hay argumento en linea de comandos: se usa nombre de fichero con lista de lazFiles por defecto')
    list_lazFiles = 'listaLazFiles.txt'
path_lazFiles = os.path.abspath(os.path.dirname(list_lazFiles))

# # Initialize QGIS Application
# qgs = qgis.core.QgsApplication([], False)
# qgis.core.QgsApplication.setPrefixPath('C:/OSGeo4W/apps/qgis', True)
# qgis.core.QgsApplication.initQgis()
# # for alg in qgis.core.QgsApplication.processingRegistry().algorithms():
# #    print(alg.id(), "->", alg.displayName())

print('Generando copc.laz de lista de ficheros', list_lazFiles)
if os.path.exists(list_lazFiles):
    inicio_time = time.time()
    inicio_datetime = datetime.datetime.now()
    print(inicio_datetime)
    # inicio_txt = inicio_datetime
    inicio_txt = f'{inicio_datetime:%Y-%m-%d %H:%M}'
    mi_lista_lazFiles = open(list_lazFiles, mode='rt')
    num_lazFile = 0
    num_lazFileProcesados = 0
    while True:
        antes_time = time.time()
        antes_datetime = datetime.datetime.now()
        # antes_txt = antes_datetime
        antes_txt = f'{antes_datetime:%Y-%m-%d %H:%M}'

        num_lazFile += 1
        name_lazFile = mi_lista_lazFiles.readline().replace('"', '').replace('\\', '/').rstrip()
        if not name_lazFile:
            break
        print(num_lazFile, name_lazFile, end=' -> ')
        # print(num_lazFile, name_lazFile)
        if name_lazFile.endswith('.copc.laz'):
            print('Es un copc.laz')
            continue
        if os.path.exists(name_lazFile.replace('.laz', '.copc.laz')):
            print('Ya tiene su correspondiente copc.laz')
            continue
        if not os.path.exists(name_lazFile):
            print(f'\tlazFile no encontrado: {name_lazFile}')
            continue
        num_lazFileProcesados += 1
        file_bytes = os.path.getsize(name_lazFile)
        file_megabytes = file_bytes / (1024 * 1024)
        nombre_solo = os.path.basename(name_lazFile)
        print(
            f'{round(file_megabytes, 2)} MB',
            # end=' >>> '
        )
        mi_json = '''
[
    "''' + name_lazFile + '''",
    {
        "type": "writers.copc",
        "filename": "''' + name_lazFile.replace('.laz', '.copc.laz') + '''"
    }
]
'''
        # print(mi_json)
        pipeline = pdal.Pipeline(mi_json)
        count = pipeline.execute()
        arrays = pipeline.arrays
        metadata = pipeline.metadata
        log = pipeline.log
        # print('arrays', arrays)
        # print('log', log)
        # cl2_1 = qgis.core.QgsPointCloudLayer(list_lazFiles, nombre_solo, 'pdal')#, cl2LayerOptions)
        # # qgis.core.QgsProject.instance().addMapLayer(cl2_1)

        # Generacion COPC: ~1 MB/s
        # time.sleep((file_megabytes) + 10)
        fin_time = time.time()
        fin_datetime = datetime.datetime.now()
        despues = fin_datetime
        # despues = fin_datetime
        despues = f'{fin_datetime:%Y-%m-%d %H:%M}'
        print(
            '  ', count, 'puntos //',
            round(fin_time - antes_time, 1), 'seg. ||',
            'Media:', round((fin_time - inicio_time) / num_lazFileProcesados, 1), 'seg. =',
           despues,
            f'>>> X: {metadata["metadata"]["readers.las"]["minx"]}-{metadata["metadata"]["readers.las"]["maxx"]}',
            f'Y: {metadata["metadata"]["readers.las"]["miny"]}-{metadata["metadata"]["readers.las"]["maxy"]}',
            f'Z: {metadata["metadata"]["readers.las"]["minz"]}-{metadata["metadata"]["readers.las"]["maxz"]}',
        )
        # quit()
else:
    print('Fichero con lista de lazFiles no encontrado:', list_lazFiles)
