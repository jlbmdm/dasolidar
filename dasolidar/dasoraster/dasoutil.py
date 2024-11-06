# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import math

import numpy as np
from osgeo import gdal

from qgis.utils import iface
from qgis.core import (
    Qgis,
    # QgsApplication,
    # QgsMessageLog,
    QgsGeometry,
    # QgsProject,
    # QgsSettings,
    # QgsVectorLayer,
    # QgsRasterLayer,
    QgsRectangle,
    QgsPointXY,
    QgsRasterBandStats,
    QgsRaster,
    QgsRasterDataProvider,
    QgsRasterBlock,
)
from qgis.analysis import QgsZonalStatistics


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
def calcular_valor_medio_rodal(
        raster_layer,
        layer_rodales,
        rodal_feat,
        raster_array=None,
        raster_dataset=None,
):
    # https://qgis.org/pyqgis/3.34/core/QgsRasterLayer.html
    print(f'raster_layer ({type(raster_layer)}): {raster_layer}')  #  <class 'qgis._core.QgsRasterLayer'>
    # print(dir(raster_layer))
    # ['Actions', 'AllStyleCategories', 'AnnotationLayer', 'AttributeTable', 'ColorLayer', 'CustomProperties', 'Diagrams',
    # 'Elevation', 'Fields', 'FlagDontResolveLayers', 'FlagForceReadOnly', 'FlagReadExtentFromXml', 'FlagTrustLayerMetadata',
    # 'Forms', 'GeometryOptions', 'GrayOrUndefined', 'GroupLayer', 'Identifiable', 'Labeling', 'LayerConfiguration',
    # 'LayerFlag', 'LayerFlags', 'LayerOptions', 'LayerType', 'Legend', 'MULTIPLE_BAND_MULTI_BYTE_ENHANCEMENT_ALGORITHM',
    # 'MULTIPLE_BAND_MULTI_BYTE_MIN_MAX_LIMITS', 'MULTIPLE_BAND_SINGLE_BYTE_ENHANCEMENT_ALGORITHM',
    # 'MULTIPLE_BAND_SINGLE_BYTE_MIN_MAX_LIMITS', 'MapTips', 'MeshLayer', 'Metadata', 'Multiband', 'Notes', 'Palette',
    # 'PluginLayer', 'PointCloudLayer', 'Private', 'PropertyType', 'RasterLayer', 'ReadFlag', 'ReadFlags', 'Relations',
    # Removable', 'Rendering', 'SAMPLE_SIZE', 'SINGLE_BAND_ENHANCEMENT_ALGORITHM', 'SINGLE_BAND_MIN_MAX_LIMITS',
    # 'Searchable', 'Style', 'StyleCategories', 'StyleCategory', 'Symbology', 'Symbology3D', 'Temporal', 'TiledScene',
    # 'VectorLayer', 'VectorTileLayer', 'abstract', 'accept', 'appendError', 'attributeTable', 'attributeTableCount',
    # 'attribution', 'attributionUrl', 'autoRefreshInterval', 'autoRefreshIntervalChanged', 'autoRefreshMode',
    # 'bandCount', 'bandName', 'beforeResolveReferences', 'blendMode', 'blendModeChanged', 'blockSignals',
    # 'brightnessFilter', 'canCreateRasterAttributeTable', 'childEvent', 'children', 'clone', 'configChanged',
    # 'connectNotify', 'constDataProvider', 'createMapRenderer', 'createProfileGenerator', 'crs', 'crsChanged',
    # 'customEvent', 'customProperties', 'customProperty', 'customPropertyChanged', 'customPropertyKeys', 'dataChanged',
    # 'dataProvider', 'dataSourceChanged', 'dataUrl', 'dataUrlFormat', 'decodedSource', 'deleteLater',
    # 'deleteStyleFromDatabase', 'dependencies', 'dependenciesChanged', 'destroyed', 'disconnect', 'disconnectNotify',
    # 'draw', 'dumpObjectInfo', 'dumpObjectTree', 'dynamicPropertyNames', 'editingStarted', 'editingStopped',
    # 'elevationProperties', 'emitStyleChanged', 'encodedSource', 'error', 'event', 'eventFilter', 'exportNamedMetadata',
    # 'exportNamedStyle', 'exportSldStyle', 'exportSldStyleV2', 'extensionPropertyType', 'extent', 'findChild',
    # 'findChildren', 'flags', 'flagsChanged', 'formatLayerName', 'generateId', 'getStyleFromDatabase',
    # 'hasAutoRefreshEnabled', 'hasDependencyCycle', 'hasMapTips', 'hasScaleBasedVisibility', 'height', 'htmlMetadata',
    # 'hueSaturationFilter', 'id', 'ignoreExtents', 'importNamedMetadata', 'importNamedStyle', 'inherits',
    # 'installEventFilter', 'invalidateWgs84Extent', 'isEditable', 'isInScaleRange', 'isModified',
    # 'isRefreshOnNotifyEnabled', 'isSignalConnected', 'isSpatial', 'isTemporary', 'isValid', 'isValidChanged',
    # 'isValidRasterFileName', 'isWidgetType', 'isWindowType', 'keywordList', 'killTimer', 'lastModified',
    # 'layerModified', 'legend', 'legendChanged', 'legendPlaceholderImage', 'legendSymbologyItems', 'legendUrl',
    # 'legendUrlFormat', 'listStylesInDatabase', 'loadDefaultMetadata', 'loadDefaultStyle', 'loadNamedMetadata',
    # 'loadNamedMetadataFromDatabase', 'loadNamedStyle', 'loadNamedStyleFromDatabase', 'loadSldStyle', 'mapTipTemplate',
    # 'mapTipTemplateChanged', 'mapTipsEnabled', 'mapTipsEnabledChanged', 'maximumScale', 'metaObject', 'metadata',
    # 'metadataChanged', 'metadataUri', 'metadataUrl', 'metadataUrlFormat', 'metadataUrlType', 'minimumScale',
    # 'moveToThread', 'name', 'nameChanged', 'objectName', 'objectNameChanged', 'opacity', 'opacityChanged',
    # 'originalXmlProperties', 'paletteAsPixmap', 'parent', 'pipe', 'previewAsImage', 'project', 'properties',
    # 'property', 'providerReadFlags', 'providerType', 'publicSource', 'pyqtConfigure', 'rasterType',
    # 'rasterUnitsPerPixelX', 'rasterUnitsPerPixelY', 'readCommonStyle', 'readCustomProperties', 'readLayerXml',
    # 'readOnly', 'readSld', 'readStyle', 'readStyleManager', 'readSymbology', 'readXml', 'recalculateExtents',
    # 'receivers', 'refreshOnNotifyMessage', 'reload', 'removeCustomProperty', 'removeEventFilter', 'renderer',
    # 'renderer3D', 'renderer3DChanged', 'rendererChanged', 'repaintRequested', 'request3DUpdate', 'resampleFilter',
    # 'resamplingStage', 'resolveReferences', 'saveDefaultMetadata', 'saveDefaultStyle', 'saveNamedMetadata',
    # 'saveNamedStyle', 'saveSldStyle', 'saveSldStyleV2', 'saveStyleToDatabase', 'selectionProperties', 'sender',
    # 'senderSignalIndex', 'serverProperties', 'setAbstract', 'setAttribution', 'setAttributionUrl',
    # 'setAutoRefreshEnabled', 'setAutoRefreshInterval', 'setAutoRefreshMode', 'setBlendMode', 'setContrastEnhancement',
    # 'setCrs', 'setCustomProperties', 'setCustomProperty', 'setDataProvider', 'setDataSource', 'setDataUrl',
    # 'setDataUrlFormat', 'setDefaultContrastEnhancement', 'setDependencies', 'setError', 'setExtent', 'setFlags',
    # 'setKeywordList', 'setLayerOrder', 'setLegend', 'setLegendPlaceholderImage', 'setLegendUrl', 'setLegendUrlFormat',
    # 'setMapTipTemplate', 'setMapTipsEnabled', 'setMaximumScale', 'setMetadata', 'setMetadataUrl',
    # 'setMetadataUrlFormat', 'setMetadataUrlType', 'setMinimumScale', 'setName', 'setObjectName', 'setOpacity',
    # 'setOriginalXmlProperties', 'setParent', 'setProperty', 'setProviderType', 'setRefreshOnNofifyMessage',
    # 'setRefreshOnNotifyEnabled', 'setRenderer', 'setRenderer3D', 'setResamplingStage', 'setScaleBasedVisibility',
    # 'setShortName', 'setSubLayerVisibility', 'setSubsetString', 'setTitle', 'setTransformContext', 'setValid',
    # 'shortName', 'showStatusMessage', 'signalsBlocked', 'source', 'startTimer', 'staticMetaObject', 'statusChanged',
    # 'styleChanged', 'styleLoaded', 'styleManager', 'styleURI', 'subLayers', 'subsetString', 'subsetStringChanged',
    # 'supportsEditing', 'temporalProperties', 'thread', 'timerEvent', 'timestamp', 'title', 'tr', 'transformContext',
    # 'trigger3DUpdate', 'triggerRepaint', 'type', 'undoStack', 'undoStackStyles', 'wgs84Extent', 'width',
    # 'willBeDeleted', 'writeCommonStyle', 'writeCustomProperties', 'writeLayerXml', 'writeSld', 'writeStyle',
    # 'writeStyleManager', 'writeSymbology', 'writeXml']

    rodal_geom = rodal_feat.geometry()
    rodal_extent = rodal_geom.boundingBox()
    print(f'Antes de ajustar a raster:')
    print(f'  Extensión del boundingbox del rodal (1) ({type(rodal_extent)}): {rodal_extent}')
    print(f'  Coord del rodal (min): {rodal_extent.xMinimum():0.1f} - {rodal_extent.yMinimum():0.1f}')
    print(f'  Coord del rodal (max): {rodal_extent.xMaximum():0.1f} - {rodal_extent.yMaximum():0.1f}')
    print(f'  Extensión del rodal: {rodal_extent.xMaximum() - rodal_extent.xMinimum():0.1f} x {rodal_extent.yMaximum() - rodal_extent.yMinimum():0.1f}')
    # print(dir(rodal_extent))
    # ['area', 'asPolygon', 'asWktCoordinates', 'asWktPolygon', 'buffered', 'center', 'combineExtentWith',
    #  'contains', 'distance', 'fromCenterAndSize', 'fromWkt', 'grow', 'height', 'include', 'intersect',
    #  'intersects', 'invert', 'isEmpty', 'isFinite', 'isNull', 'normalize', 'perimeter', 'scale', 'scaled',
    #  'set', 'setMinimal', 'setNull', 'setXMaximum', 'setXMinimum', 'setYMaximum', 'setYMinimum',
    #  'snappedToGrid', 'toBox3d', 'toRectF', 'toString', 'width', 'xMaximum', 'xMinimum', 'yMaximum', 'yMinimum']

    # rodal_extent = rodal_extent.snapToGrid(raster_layer.rasterUnitsPerPixelX(), raster_layer.rasterUnitsPerPixelY())

    usar_metodo1 = False
    # No está documentado por pyQgis
    if usar_metodo1:
        print()
        print('Metodo 1: bandStatistics (con coordenadas ajustadas a malla del raster)')

        # Obtener el tamaño de los píxeles del raster
        pixel_width = raster_layer.rasterUnitsPerPixelX()
        pixel_height = raster_layer.rasterUnitsPerPixelY()
        print(f'Pixel with height-> X: {pixel_width}; Y: {pixel_height}')

        # Ajustar las coordenadas de la extensión a la cuadrícula del raster
        adjusted_x_min = round(rodal_extent.xMinimum() / pixel_width) * pixel_width
        adjusted_y_min = round(rodal_extent.yMinimum() / pixel_height) * pixel_height
        adjusted_x_max = round(rodal_extent.xMaximum() / pixel_width) * pixel_width
        adjusted_y_max = round(rodal_extent.yMaximum() / pixel_height) * pixel_height

        # Crear un nuevo QgsRectangle ajustado
        adjusted_extent = QgsRectangle(adjusted_x_min, adjusted_y_min, adjusted_x_max, adjusted_y_max)

        # Si necesitas ajustar la geometría original, puedes crear una nueva geometría
        # Aquí se ajusta la geometría a la nueva extensión
        adjusted_geom = QgsGeometry.fromRect(adjusted_extent)

        print(f'Despues de ajustar a raster:')
        print(f'  Coord del rodal (min): {adjusted_extent.xMinimum():0.1f} - {adjusted_extent.yMinimum():0.1f}')
        print(f'  Coord del rodal (max): {adjusted_extent.xMaximum():0.1f} - {adjusted_extent.yMaximum():0.1f}')
        print(f'  Extensión del rodal: {adjusted_extent.xMaximum() - adjusted_extent.xMinimum():0.1f} x {adjusted_extent.yMaximum() - adjusted_extent.yMinimum():0.1f}')

        if (
                adjusted_extent.xMaximum() - adjusted_extent.xMinimum() > 10000
                or adjusted_extent.yMaximum() - adjusted_extent.yMinimum() > 10000
        ):
            print('Zona demasiado amplia; no se ha selecionado bien el rodal')
            print(f'rodal_geom ({type(rodal_geom)}): {rodal_geom}')
            print(dir(rodal_geom))
            adjusted_extent = QgsRectangle(
                328000,
                4764000,
                330000,
                4766000,
            )

        # https://qgis.org/pyqgis/3.34/analysis/QgsZonalStatistics.html
        # https://qgis.org/pyqgis/3.34/core/QgsDataProvider.html

        # Calcular el valor medio de los píxeles del ráster en el polígono
        # QgsRasterLayer.dataProvider
        #   https://qgis.org/pyqgis/3.34/core/QgsRasterLayer.html#qgis.core.QgsRasterLayer.dataProvider
        #     Returns the source data provider. Return type [QgsRasterDataProvider]
        raster_provider = raster_layer.dataProvider()
        # QgsRasterDataProvider:
        #   https://qgis.org/pyqgis/3.34/core/QgsRasterDataProvider.html#qgis.core.QgsRasterDataProvider
        #     No aparece el metodo bandStatistics()
        stats = raster_provider.bandStatistics(
            1,  # banda
            QgsRasterBandStats.Mean,
            # QgsRasterBandStats.All,
            adjusted_extent,
        )

        print(f'calcular_valor_medio_rodal-> Estadisticas de tipo: stats: {type(stats)}')
        # print(dir(stats))
        # ['All', 'Max', 'Mean', 'Min', 'None_', 'Range', 'Stats', 'StdDev', 'Sum', 'SumOfSquares',
        #  'bandNumber', 'contains', 'elementCount', 'extent', 'height', 'maximumValue', 'mean',
        #  'minimumValue', 'range', 'statsGathered', 'stdDev', 'sum', 'sumOfSquares', 'width']
        valor_medio = stats.mean
        print(f'valor_medio: {valor_medio}')
        # valor_max = stats.Max
        # valor_min1 = stats.Min
        # valor_min2 = stats.minimumValue
        # num_pixeles = stats.elementCount
        # rango_valores1 = stats.range
        # rango_valores2 = stats.Range
        # desv_std1 = stats.stdDev
        # desv_std2 = stats.StdDev
        # print(f'valor_max:   {valor_max}')
        # print(f'valor_min1:  {valor_min1}')
        # print(f'valor_min2:  {valor_min2}')
        # print(f'Rango1:      {rango_valores1}')
        # print(f'Rango2:      {rango_valores2}')
        # print(f'desv_std1:   {desv_std1}')
        # print(f'desv_std2:   {desv_std2}')
        # print(f'num_pixeles: {num_pixeles}')

    usar_metodo2 = True
    if usar_metodo2:
        # Obtengo anticipadamente el raster_array y raster_dataset
        def raster_to_numpy(raster_layer):
            iface.messageBar().pushMessage(
                title='dasoraster',
                text=f'Estamos trabajando para agilizar esta consulta. Por el momento tendrás que esperar entre medio y un minuto mientras se lee el raster de volúmenes de Castilla y León y se calculan los valores del polígono seleccionado. No pulses ninguna tecla o botón del ratón.',
                # showMore=f'',
                duration=20,
                level=Qgis.Warning,
            )
            usar_fichero_cocina = True
            if usar_fichero_cocina:
                # raster_path = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$\dasoLidar\PNOA2_2017 - 2021\variablesDasometricas\version_202410'
                raster_path = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$\dasoLidar\varios\cocina'
                raster_filename = 'dasoLidar_VolumenMadera_m3_ha.tif'
                raster_filepath = os.path.join(raster_path, raster_filename)
            else:
                # Obtener el proveedor de datos del ráster
                provider = raster_layer.dataProvider()
                raster_filepath = provider.dataSourceUri()
            print(f'Fichero de volumen: {raster_filepath}')
            print(f'Fichero disponible: {os.path.exists(raster_filepath)}')
            # Abrir el ráster usando GDAL
            raster_dataset = gdal.Open(raster_filepath)
            raster_band = raster_dataset.GetRasterBand(1)
            # Leer el ráster como un array de numpy
            raster_array = raster_band.ReadAsArray()
            return raster_array, raster_dataset

        def extraer_slice(raster_array, raster_dataset, rodal_geom):
            # Obtener las coordenadas del bounding box del polígono
            # coord_min_x, coord_max_x, coord_min_y, coord_max_y = rodal_geom.GetEnvelope()
            rodal_extent = rodal_geom.boundingBox()
            coord_min_x = rodal_extent.xMinimum()
            coord_max_x = rodal_extent.xMaximum()
            coord_min_y = rodal_extent.yMinimum()
            coord_max_y = rodal_extent.yMaximum()
            print(f'Coordenadas del rodal:')
            print(f'  Min X: {coord_min_x:0.1f}, Y: {coord_min_y:0.1f}')
            print(f'  Max X: {coord_max_x:0.1f}, Y: {coord_max_y:0.1f}')
            print(f"Extensión del rodal: {rodal_extent}")
            rodal_esq_sup_izda_x = coord_min_x
            rodal_esq_sup_izda_y = coord_max_y
            raster_esq_sup_izda_x = raster_dataset.GetGeoTransform()[0]
            raster_esq_sup_izda_y = raster_dataset.GetGeoTransform()[3]
            pixel_x = raster_dataset.GetGeoTransform()[1]  #  10
            pixel_y = raster_dataset.GetGeoTransform()[5]  #  -10
            print(f'raster_esq_sup_izda: {raster_esq_sup_izda_x:0.1f}, {raster_esq_sup_izda_y:0.1f}')
            print(f'rodal_esq_sup_izda:  {rodal_esq_sup_izda_x:0.1f}, {rodal_esq_sup_izda_y:0.1f}')

            offset_x = int((rodal_esq_sup_izda_x - raster_esq_sup_izda_x) / pixel_x)
            offset_y = int((rodal_esq_sup_izda_y - raster_esq_sup_izda_y) / pixel_y)
            rodal_num_pixels_x = math.ceil(coord_max_x / pixel_x) - math.floor(coord_min_x / pixel_x)  #  pixel_x = 10
            rodal_num_pixels_y = math.floor(coord_min_y / pixel_y) - math.ceil(coord_max_y / pixel_y)  #  pixel_y = -10
            print(f'Slice calculado por mí:')
            print(f'  X: {offset_x} : {offset_x + rodal_num_pixels_x}')
            print(f'  Y: {offset_y} : {offset_y + rodal_num_pixels_y}')

            # Convertir las coordenadas del bounding box a índices de píxeles
            gt = raster_dataset.GetGeoTransform()
            inv_gt = gdal.InvGeoTransform(gt)
            min_x, min_y = gdal.ApplyGeoTransform(inv_gt, rodal_extent.xMinimum(), rodal_extent.yMaximum())
            max_x, max_y = gdal.ApplyGeoTransform(inv_gt, rodal_extent.xMaximum(), rodal_extent.yMinimum())
            print(f'Posicion del rodal dentro del raster en términos de pixeles')
            print(f'Slice calculado con InvGeoTransform:')
            print(f'  X: {min_x} : {max_x}')
            print(f'  Y: {min_y} : {max_y}')
            min_x, max_x = int(round(min_x)), int(round(max_x))
            min_y, max_y = int(round(min_y)), int(round(max_y))
            print(f'Redondeadas y valores enteros:')
            print(f'  X: {min_x} : {max_x}')
            print(f'  Y: {min_y} : {max_y}')

            usar_mi_slice = True
            if usar_mi_slice:
                slice_array = raster_array[
                    offset_x: offset_x + rodal_num_pixels_x,
                    offset_y: offset_y + rodal_num_pixels_y
                ]
            else:
                slice_array = raster_array[
                    min_x: max_x,
                    min_y: max_y
                ]
            return slice_array

        def calcular_media_raster_en_poligono(
                rodal_geom,
                raster_array,
                raster_dataset,
                raster_layer,
            ):
            # Obtengo anticipadamente raster_array, raster_dataset, al pulsar el botón de consultar rodal
            if not raster_dataset:
                raster_array, raster_dataset = raster_to_numpy(raster_layer)
            slice_array = extraer_slice(raster_array, raster_dataset, rodal_geom)
            num_pixeles_dentro = 0
            num_pixeles_fuera = 0
            print(f'Esquina supizda X raster: {raster_dataset.GetGeoTransform()[0]}')
            print(f'Esquina supizda Y raster: {raster_dataset.GetGeoTransform()[3]}')

            pixel_x = raster_dataset.GetGeoTransform()[1]
            pixel_y = raster_dataset.GetGeoTransform()[5]
            print(f'Pixel X: {pixel_x}')
            print(f'Pixel Y: {pixel_y}')
            # print(f'rodal_geom de referencia: {rodal_geom}')
            rodal_extent = rodal_geom.boundingBox()
            print(f'BoundingBox: {rodal_extent}')
            coord_min_x = pixel_x * math.floor(rodal_extent.xMinimum() / pixel_x)
            coord_max_x = pixel_x * math.ceil(rodal_extent.xMaximum() / pixel_x)
            coord_min_y = pixel_y * math.floor(rodal_extent.yMinimum() / pixel_y)
            coord_max_y = pixel_y * math.ceil(rodal_extent.yMaximum() / pixel_y)
            print(f'Coordenadas del rodal ajustadas al pixel del ráster:')
            print(f'  Min X: {coord_min_x:0.1f}, Y: {coord_min_y:0.1f}')
            print(f'  Max X: {coord_max_x:0.1f}, Y: {coord_max_y:0.1f}')

            rodal_mask = np.zeros_like(slice_array, dtype=bool)
            print(f'Array de valores-> shape: {slice_array.shape}; dtype: {slice_array.dtype}')
            print(f'rodal_mask ->      shape: {rodal_mask.shape}; dtype: {rodal_mask.dtype})')
            if slice_array.shape[0] > 105 and slice_array.shape[1] > 105:
                print(slice_array[100:105, 100:105])
            for row in range(slice_array.shape[0]):
                for col in range(slice_array.shape[1]):
                    # x = raster_dataset.GetGeoTransform()[0] + (col + 0.5) * pixel_x
                    x = coord_min_x + ((col + 0.5) * pixel_x)
                    # y = raster_dataset.GetGeoTransform()[3] + (row + 0.5) * pixel_y
                    y = coord_max_y + ((row + 0.5) * pixel_y)
                    y_ = coord_min_y - ((row + 0.5) * pixel_y)
                    point = QgsPointXY(x, y)
                    if rodal_geom.contains(point):
                        num_pixeles_dentro += 1
                        rodal_mask[row, col] = True
                        if row % 50 == 0 and col % 50 == 0:
                            print(f'point {point} (y_: {x}, {y_}) dentro -> {slice_array[row, col]}')  #  // {slice_array[col, row]}
                    else:
                        num_pixeles_fuera += 1
                        if row % 50 == 0 and col % 50 == 0:
                            print(f'point {point} (y_: {x}, {y_}) fuera -> {slice_array[row, col]}')  #  // {slice_array[col, row]}
            print(f'num_pixeles_dentro: {num_pixeles_dentro}')
            print(f'num_pixeles_fuera:  {num_pixeles_fuera}')

            # Aplicar la máscara y calcular la media de los valores
            masked_values = slice_array[rodal_mask]
            if masked_values.size > 0:
                media_zonal = np.mean(masked_values)
                num_pixeles = masked_values.size
            else:
                media_zonal = None
                num_pixeles = 0

            return media_zonal, num_pixeles

        # Uso de la función
        rodal_geom = rodal_feat.geometry()
        media_zonal, num_pixeles = calcular_media_raster_en_poligono(
            rodal_geom,
            raster_array,
            raster_dataset,
            raster_layer,
        )
        print(f"El valor medio de los píxeles del ráster en el polígono es: {media_zonal} ({num_pixeles} pixeles)")

    usar_metodo3 = False
    if usar_metodo3:
        print()
        print('Metodo 3: rodal_block')
        # Calcular el tamaño del bloque en píxeles
        raster_extent = raster_layer.extent()
        x_res = raster_layer.width() / raster_extent.width()
        y_res = raster_layer.height() / raster_extent.height()
        print(f'Raster pixel:         {x_res} x {y_res}')
        print(f'Raster size (pixels): {raster_layer.width()} x {raster_layer.height()} metros')

        x_size = int((rodal_extent.xMaximum() - rodal_extent.xMinimum()) * x_res)
        y_size = int((rodal_extent.yMaximum() - rodal_extent.yMinimum()) * y_res)
        print(f'rodal_block size (pixeles): {x_size} x {y_size} pixeles')

        provider = raster_layer.dataProvider()
        # Obtener el bloque de datos ráster dentro del bounding box del polígono
        rodal_block = provider.block(1, rodal_extent, x_size, y_size)
        # rodal_block = provider.block(1, rodal_extent, raster_layer.width(), raster_layer.height())
        # stats2 = provider.bandStatistics(1, QgsRasterBandStats.All, rodal_extent, 0)

        print(f'Dimensiones del raster: {raster_layer.width()} x {raster_layer.height()} pixeles')
        print(f'Dimensiones del bloque: {rodal_block.width()} x {rodal_block.height()} pixeles')

        # Convertir el bloque a un array de numpy
        array = np.array(rodal_block.data(), dtype=float)
        try:
            if array.size == rodal_block.width() * rodal_block.height():
                array.resize([rodal_block.width(), rodal_block.height()])
                print(11)
                doble_banda = False
            elif array.size == rodal_block.width() * rodal_block.height() * 2:
                array.resize([rodal_block.width(), rodal_block.height(), 2])
                print(12)
                doble_banda = True
        except:
            print(f'array shape: {array.shape}; size: {array.size}; rodal_block: {rodal_block.width() * rodal_block.height()}; rodal_block x 2: {rodal_block.width() * rodal_block.height() * 2}')
            print('array None: revisar')
            return

        print(f'array.shape: {array.shape})')
        print(f'array: {array}')
        # Crear una máscara para los píxeles dentro del polígono
        # rodal_mask = np.zeros(array.shape, dtype=bool)
        rodal_mask = np.zeros([rodal_block.width(), rodal_block.height()], dtype=bool)
        print(f'rodal_mask.shape:  {rodal_mask.shape})')
        coord_min_x = x_res * math.floor(rodal_extent.xMinimum() / x_res)
        coord_max_x = x_res * math.ceil(rodal_extent.xMaximum() / x_res)
        coord_min_y = y_res * math.floor(rodal_extent.yMinimum() / y_res)
        coord_max_y = y_res * math.ceil(rodal_extent.yMaximum() / y_res)
        print(f'Coordenadas del rodal ajustadas al pixel del ráster:')
        print(f'  Min X: {coord_min_x:0.1f}, Y: {coord_min_y:0.1f}')
        print(f'  Max X: {coord_max_x:0.1f}, Y: {coord_max_y:0.1f}')

        num_pixeles_dentro = 0
        for row in range(rodal_mask.shape[0]):
            for col in range(rodal_mask.shape[1]):
                x = coord_min_x + ((col + 0.5) * rodal_block.width() / rodal_mask.shape[1])
                y = coord_max_y - ((row + 0.5) * rodal_block.height() / rodal_mask.shape[0])
                point = QgsPointXY(x, y)
                if rodal_geom.contains(point):
                    num_pixeles_dentro += 1
                    print(f'point {point} dentro de {rodal_geom}')
                    rodal_mask[row, col] = True

        print(f'num_pixeles_dentro: {num_pixeles_dentro}')

        # Aplicar la máscara y calcular la media de los valores
        try:
            masked_values = array[rodal_mask]
            print(f'1. masked_values.shape: {masked_values.shape}')
        except:
            masked_values = array[::0][rodal_mask]
            print(f'2. masked_values.shape: {masked_values.shape}')
        if masked_values.size > 0:
            media_zonal = np.mean(masked_values)
            num_pixeles = masked_values.size
        else:
            media_zonal = None
            num_pixeles = 0

        print(f'Valor medio: {media_zonal}')
        print(f'Num pixeles: {num_pixeles}')


    # # Crear una máscara para el polígono
    # rodal_mask = raster_layer.dataProvider().block(1, extent, raster_layer.width(), raster_layer.height())
    # rodal_mask.fill(0)
    # rodal_mask.setNoDataValue(0)
    #
    # # Obtener los valores de los píxeles dentro del polígono
    # values = []
    # for pixel in rodal_mask:
    #     if rodal_geom.contains(pixel):
    #         values.append(pixel)
    #
    # # Calcular la media de los valores
    # if values:
    #     media_zonal = sum(values) / len(values)
    #     num_pixeles = len(values)
    # else:
    #     media_zonal = -1
    #     num_pixeles = 0


    # if False:
    #     # Calcular las estadísticas zonales
    #     # https://qgis.org/pyqgis/master/analysis/QgsZonalStatistics.html
    #     zonal_stats = QgsZonalStatistics(
    #         polygonLayer=layer_rodales,
    #         rasterLayer=raster_layer,
    #         attributePrefix='rodal_',
    #         # prefix="zonal_",
    #         rasterBand=1,
    #         # band=1,
    #         statistics=QgsZonalStatistics.Mean,
    #         # rodal_feat.geometry(),
    #     )
    #     zonal_stats.calculateStatistics(None)
    #     print(f'calcular_valor_medio_rodal-> Estadisticas de tipo: stats: {type(zonal_stats)}')
    #     print(dir(zonal_stats))
    #     # Obtener el valor medio de los píxeles del ráster dentro del polígono
    #     media_zonal = rodal_feat["zonal_mean"]
    #     print(f'media_zonal: {media_zonal}')

    return media_zonal, num_pixeles

# ==============================================================================
def calcular_valor_medio_parcela(raster_layer, x_consulta, y_consulta, radio_parcela=15, consultar_circulo=True):
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
    rodal_block = provider.block(1, extent_explora_pixels, cols, rows)

    # Extraer los valores de los píxeles dentro del círculo
    valores_selec = []
    for i in range(rows):
        for j in range(cols):
            x_pixel = x_orig_explora_pixels + (j + 0.5) * raster_layer.rasterUnitsPerPixelX()
            y_pixel = y_orig_explora_pixels - (i + 0.5) * raster_layer.rasterUnitsPerPixelY()
            punto_pixel = QgsPointXY(x_pixel, y_pixel)
            if consultar_circulo:
                if consulta_geom.contains(QgsGeometry.fromPointXY(punto_pixel)):
                    valor = rodal_block.value(i, j)
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
                    valor = rodal_block.value(i, j)
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

