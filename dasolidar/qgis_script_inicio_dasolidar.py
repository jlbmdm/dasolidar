# -*- coding: UTF-8 -*-
import os
import sys
import time
from datetime import datetime
import pathlib
import subprocess
import platform
import zipfile
# import shutil
# from shutil import copyfile

import numpy as np
import win32com.client

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsMessageLog,
    QgsGeometry,
    QgsProject,
    QgsSettings,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsRectangle,
    QgsPointXY,
)
from qgis.gui import (
    QgsDialog,
    QgsMapToolEmitPoint,
)
from qgis.utils import (
    iface,
    loadPlugin,
    startPlugin,
    plugins,
    unloadPlugin,
    findPlugins,
)
try:
    from qgis.utils import home_plugin_path
    # home_plugin_ok = True
except:
    home_plugin_path = os.path.join(os.environ['APPDATA'], 'QGIS/QGIS3/profiles/default/python/plugins')
    # home_plugin_ok = False
from qgis.PyQt.QtWidgets import (
    QDialog,
    QTextBrowser,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QDialogButtonBox,
    QCheckBox,
    QLineEdit,
    QTextEdit,
    QWidget,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QAction,
    QMessageBox,
    QMainWindow,
    # QGridLayout,
)
from qgis.PyQt.QtCore import Qt
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from PyQt5.QtCore import QSettings


# from qgis.gui import QgsHtmlAnnotationItem
# html_annotation = QgsHtmlAnnotationItem(QgsProject.instance().mapLayers().values())
# html_annotation.setHtml(intro_dasolidar)
# html_annotation.setMapPosition(QgsProject.instance().mapLayers().values().extent().center())
# QgsProject.instance().annotationManager().addAnnotation(html_annotation)


# ==============================================================================
def str_to_bool(s):
    return s.lower() in ['true', '1', 't', 'y', 'yes']

# ==============================================================================
mi_config = QgsSettings()
class Configuracion():
    def __init__(self):
        self.dl_usuario = mi_config.value('dasolidar/usuario', 'anonimo')
        self.dl_usos  = mi_config.value('dasolidar/usos', 123)
        self.dl_ventana_bienvenida = mi_config.value('dasolidar/dl_ventana_bienvenida', True)
        self.dl_message_bienvenida = mi_config.value('dasolidar/dl_message_bienvenida', True)

# ==============================================================================
config_class = Configuracion()
print(f'betaraster-> dl_ventana_bienvenida 1: ({type(config_class.dl_ventana_bienvenida)}) {config_class.dl_ventana_bienvenida}')
if type(config_class.dl_ventana_bienvenida) == str:
    config_class.dl_ventana_bienvenida = str_to_bool(config_class.dl_ventana_bienvenida)
print(f'betaraster-> dl_ventana_bienvenida 2: ({type(config_class.dl_ventana_bienvenida)}) {config_class.dl_ventana_bienvenida}')
# ==============================================================================

acceso_lidardata = True
# ==============================================================================
# Lo siguiente es código replicado en SIGMENA.py con tres diferencias:
#  No incluyo Los imports porque van arriba
#  No incluyo la función revisar_enlaces_directos
#  El chequeo se hace siempre en vez de un día a la semana o al mes
#  No existe listaId332_check
# ==============================================================================
# Inicio sigmena.py
# ==============================================================================
# Se revisan los enlaces directos del proyecto dasoLidar (se eliminan los que sobran y/o se actualizan si procede)
# Si Javi cambia algo en SIGMENA.py, aprovechar para:
#   Llevar los imports a su sitio (arriba)
#   Que no de error si no se encuentra un complemento chequeando
#     os.path.exists('O:/sigmena/utilidad/PROGRAMA/QGIS/Complementos/'+complementos_con_version[i][0]+'.zip')

# Este código es lento porque accede a diversos ficheros:
#  1. Escritorio del usuario para actualizar los enlaces directos si procede
#  2. Ficheros en \\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$:
#     versionDasolidar.txt -> Para ver si hay nueva versión de dasoraster
#     comlemento dasoraster.zip
#     Iconos y enlaces directos
#     En el caso del proyecto dasoLidar tb se ejecuta el bath de inicio
#  3. Ficheros en V:/MA_SCAYLE_VueloLidar/dasolidar:
#     dasolidar_install.log y lidarQgis.log para tener log de instalación y seguimiento de uso
#  4. Complemento O:/sigmena/utilidad/PROGRAMA/QGIS/Complementos/dasoraster.zip


# home_env = os.path.expanduser(os.environ['HOME'])
# HOME_DIR = str(pathlib.Path.home())

hoy_AAAAMMDD = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
# current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
EMAIL_DASOLIDAR1 = 'benmarjo@jcyl.es'
EMAIL_DASOLIDAR2 = 'dasolidar@gmail.com'
separador_dasolistas = '\t'
usuario_beta = False

#aux_path_old = r'\\repoarchivohm.jcyl.red/MADGMNSVPI_SCAYLEVueloLIDAR$/PNOA2/.aux/'
aux_path_new = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$\dasoLidar\varios\.aux'
scripts_path = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$\dasoLidar\varios\scripts'
lista_usuarios_actual_filename = os.path.join(aux_path_new, 'usuarios/usuariosLidar_versionActual.csv')
lista_usuarios_beta_filename = os.path.join(aux_path_new, 'usuarios/usuariosLidar_versionBeta.csv')
# Las listas de usuarios se leen de forma periodica (semanal, quinquenal o mensual) en lista_usuarios_dasolidar<>
versionDasolidar_filename = 'versionDasolidar.txt'
versionDasolidar_filepath = os.path.join(aux_path_new, versionDasolidar_filename)
fechasDasolidar_dict = {}
if os.path.exists(versionDasolidar_filepath):
    try:
        with open(versionDasolidar_filepath, 'r') as versionesDasolidar:
            fechasDasolidar_list = versionesDasolidar.readlines()
        for fechaDasolidar_line in fechasDasolidar_list:
            file_type = fechaDasolidar_line.split('\t')[0]
            file_date = fechaDasolidar_line.split('\t')[1]
            fechasDasolidar_dict[file_type] = file_date.rstrip('\n')
    except:
        pass

# usuario_psutil = psutil.users()[0].name
usuario_env = ''
usuario_profile = ''
try:
    usuario_login = os.getlogin()
    print(f'betaraster-> Usuario_login: {usuario_login}')
except:
    usuario_login = None
    try:
        usuario_env = os.environ.get('USERNAME')
        print(f'betaraster-> Usuario_env: {usuario_env}')
    except:
        usuario_env = None
        usuario_profile = os.path.expandvars("%userprofile%")[-8:].lower()
        print(f'betaraster-> Usuario_profile: {usuario_profile}')
if isinstance(usuario_login, str) and len(usuario_login) == 8:
    usuario_actual = usuario_login.lower()
elif isinstance(usuario_env, str) and len(usuario_env) == 8:
    usuario_actual = usuario_env.lower()
elif isinstance(usuario_profile, str) and len(usuario_profile) == 8:
    usuario_actual = usuario_profile.lower()
else:
    usuario_actual = 'anonimo'

# Se consulta la fecha se compara con las almacenadas en Qgis y se decide los procesos a lanzar
dia_de_la_semana = datetime.now().weekday()
dia_del_mes = datetime.now().day
settings = QSettings()
last_log = settings.value('dasoraster/last_log', '20241101', type=str)
if dia_del_mes == 1 or (last_log.isdigit and (int(hoy_AAAAMMDD) - int(last_log)) > 31):
    # Solo una vez al mes (a principios)
    actualizar_enlaces_directos = True
else:
    actualizar_enlaces_directos = False

if dia_de_la_semana == 1 or (last_log.isdigit and (int(hoy_AAAAMMDD) - int(last_log)) > 7) or actualizar_enlaces_directos:
    # Solo los lunes (implica acceso a V:\)
    leer_lista_usuarios_dasolidar = True
    hacer_log_de_instalacion = True
    QSettings().setValue('/dasoraster/last_log', hoy_AAAAMMDD)
else:
    hacer_log_de_instalacion = False
    leer_lista_usuarios_dasolidar = False


def log_de_instalacion():
    dasolidar_list = []
    dasolidar_log = None
    lista_usuarios_activos = []
    lista_usuarios_grupo_activos = []
    unidad_v_path = 'V:/MA_SCAYLE_VueloLidar'
    log_path_1 = os.path.join(unidad_v_path, 'dasolidar')
    log_path_2 = 'O:/sigmena/utilidad/programa/QGIS/dasolidar'
    unidad_V_disponible = False
    log_path_ok = ''
    if os.path.isdir(unidad_v_path):
        if not os.path.isdir(log_path_1):
            try:
                os.mkdir(log_path_1)
                unidad_V_disponible = True
                log_path_ok = log_path_1
            except FileExistsError:
                # Esto no debiera de pasar nunca, indica que algo falla al acceder a la ubicacion de red
                print(f'betaraster-> El directorio "{log_path_1}" ya existe.')
            except Exception as e:
                unidad_V_disponible = False
                print(f'betaraster-> Error al crear el directorio: {log_path_1}')
                print(f'betaraster-> Error: {e}')
        else:
            unidad_V_disponible = True
            log_path_ok = log_path_1
    if not unidad_V_disponible:
        if not os.path.isdir(log_path_2):
            try:
                os.mkdir(log_path_2)
                log_path_ok = log_path_2
            except FileExistsError:
                print(f'betaraster-> El directorio "{log_path_2}" ya existe.')
            except Exception as e:
                print(f'betaraster-> Error al crear el directorio: {log_path_2}')
                print(f'betaraster-> Error: {e}')
        else:
            log_path_ok = log_path_2
    if log_path_ok:
        intall_log = 'dasolidar_install.log'
        log_filename = os.path.join(log_path_ok, intall_log)
        try:
            dasolidar_log = open(log_filename, mode='a+')
            dasolidar_log.seek(0)
            dasolidar_list = dasolidar_log.readlines()
        except:
            dasolidar_list = []
            dasolidar_log = None
    else:
        dasolidar_log = None
    for dasolidar_line in dasolidar_list:
        dasolidar_line = dasolidar_line.rstrip('\n')
        line_id = dasolidar_line.split(separador_dasolistas)[0]
        if line_id.startswith('nuevoUser332') or line_id.startswith('modifUser332'):
            usuario_activo = dasolidar_line.split(separador_dasolistas)[1]
            usuario_grupo = dasolidar_line.split(separador_dasolistas)[2]  #  actual, beta, pteDarDeAlta
            # usuario_fecha = dasolidar_line.split(separador_dasolistas)[3]  #  Ej.: 20241106
            if not usuario_activo in lista_usuarios_activos:
                lista_usuarios_activos.append(usuario_activo)
            if not [usuario_activo, usuario_grupo] in lista_usuarios_grupo_activos:
                lista_usuarios_grupo_activos.append([usuario_activo, usuario_grupo])

    return dasolidar_log, lista_usuarios_activos, lista_usuarios_grupo_activos

def lista_usuarios_dasolidar(
        dasolidar_log,
    ):
    if os.path.exists(lista_usuarios_actual_filename):
        # my_list = open(lista_usuarios_actual_filename, mode='r')
        try:
            with open(lista_usuarios_actual_filename, mode='r', encoding='utf-8') as my_list:
                listaUsers_versionActual = my_list.readlines()
                listaId332_versionActual = [usuario.split(separador_dasolistas)[0].lower() for usuario in listaUsers_versionActual]
            # print(f'betaraster-> Encoding UTF8 ok')
        except:
            try:
                with open(lista_usuarios_actual_filename, mode='r', encoding='cp1252') as my_list:
                    listaUsers_versionActual = my_list.readlines()
                    listaId332_versionActual = [usuario.split(separador_dasolistas)[0].lower() for usuario in listaUsers_versionActual]
                # print(f'betaraster-> Encoding cp1252 ok')
            except:
                print(f'betaraster-> Atencion: revisar caracteres no admitidos en {lista_usuarios_actual_filename}')
                listaId332_versionActual = []
    else:
        try:
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'\nAviso{separador_dasolistas}{usuario_actual}{separador_dasolistas}all{separador_dasolistas}{hoy_AAAAMMDD}No se encuentra {lista_usuarios_actual_filename}')
        except:
            pass
        listaId332_versionActual = []

    if os.path.exists(lista_usuarios_beta_filename):
        # my_list = open(lista_usuarios_beta_filename, mode='r')
        try:
            with open(lista_usuarios_beta_filename, mode='r', encoding='utf-8') as my_list:
                listaUsers_versionBeta = my_list.readlines()
                listaId332_versionBeta = [usuario.split(separador_dasolistas)[0].lower() for usuario in listaUsers_versionBeta]
            # print(f'betaraster-> Encoding UTF8 ok')
        except:
            try:
                with open(lista_usuarios_beta_filename, mode='r', encoding='cp1252') as my_list:
                    listaUsers_versionBeta = my_list.readlines()
                    listaId332_versionBeta = [usuario.split(separador_dasolistas)[0].lower() for usuario in listaUsers_versionBeta]
                # print(f'betaraster-> Encoding cp1252 ok')
            except:
                print(f'betaraster-> Atencion: revisar caracteres no admitidos en {lista_usuarios_beta_filename}')
                listaId332_versionBeta = []
    else:
        try:
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'\nAviso{separador_dasolistas}{usuario_actual}{separador_dasolistas}all{separador_dasolistas}{hoy_AAAAMMDD}No se encuentra {lista_usuarios_beta_filename}')
        except:
            pass
        listaId332_versionBeta = []
    return (listaId332_versionActual, listaId332_versionBeta)

def log_usuario_nuevo_modif(
        dasolidar_log,
        lista_usuarios_activos,
        lista_usuarios_grupo_activos,
        listaId332_versionBeta,
        listaId332_versionActual,
        dasoraster_sigmena_disponible,
    ):
    # usuario_nuevo = False
    # dasolidar_log.write(f'lista_usuarios_activos:\n{lista_usuarios_activos}\n')
    if usuario_actual in listaId332_versionBeta:
        if not usuario_actual in lista_usuarios_activos:
            # usuario_nuevo = True
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'nuevoUser332{separador_dasolistas}{usuario_actual}{separador_dasolistas}beta{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}{dasoraster_sigmena_disponible}\n')
        elif not [usuario_actual, 'beta'] in lista_usuarios_grupo_activos:
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'modifUser332{separador_dasolistas}{usuario_actual}{separador_dasolistas}beta{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}{dasoraster_sigmena_disponible}\n')
        else:
            pass
    elif usuario_actual in listaId332_versionActual:
        if not usuario_actual in lista_usuarios_activos:
            # usuario_nuevo = True
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'nuevoUser332{separador_dasolistas}{usuario_actual}{separador_dasolistas}actual{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}{dasoraster_sigmena_disponible}\n')
        elif not [usuario_actual, 'actual'] in lista_usuarios_grupo_activos:
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'modifUser332{separador_dasolistas}{usuario_actual}{separador_dasolistas}actual{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}{dasoraster_sigmena_disponible}\n')
        else:
            pass
    else:
        if not usuario_actual in lista_usuarios_activos:
            # usuario_nuevo = True
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'nuevoUser332{separador_dasolistas}{usuario_actual}{separador_dasolistas}pteDarDeAltal{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}{dasoraster_sigmena_disponible}\n')
        elif (
            not [usuario_actual, 'pteDarDeAlta'] in lista_usuarios_grupo_activos
            and not [usuario_actual, 'dadoDeBaja'] in lista_usuarios_grupo_activos
        ):
            if hacer_log_de_instalacion and dasolidar_log:
                dasolidar_log.write(f'modifUser332{separador_dasolistas}{usuario_actual}{separador_dasolistas}dadoDeBaja{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}{dasoraster_sigmena_disponible}\n')
        else:
            pass

def instalacion_dasoraster(
        dasolidar_log,
        lista_usuarios_activos,
        lista_usuarios_grupo_activos,
        listaId332_versionBeta,
        listaId332_versionActual,
        dasoraster_filepath_sigmena
    ):
    global complementos_con_version
    if usuario_actual in listaId332_versionBeta and 'pluginBeta' in fechasDasolidar_dict.keys():
        dasoraster_version = fechasDasolidar_dict['pluginBeta']
    elif usuario_actual in listaId332_versionActual and 'pluginActual' in fechasDasolidar_dict.keys():
        dasoraster_version = fechasDasolidar_dict['pluginActual']
    else:
        dasoraster_version = 'v.0.0.0'

    dasoraster_filepath_dasolidar = os.path.join(scripts_path, 'dasoraster.zip')
    if os.path.isdir(scripts_path):
        dasoraster_filepath = dasoraster_filepath_dasolidar
    if not os.path.exists(dasoraster_filepath):
        dasoraster_filepath = dasoraster_filepath_sigmena

    if os.path.exists(dasoraster_filepath):
        instalar_dasoraster_con_el_resto = False
        if instalar_dasoraster_con_el_resto:
            complementos_con_version.extend([['dasoraster', dasoraster_version]])
        else:
            if os.path.isdir(home_plugin_path):
                # os.stat(home_plugin_path)
                versioninstalada = 'v.0.0.0'
                for x in findPlugins(home_plugin_path):
                    if x[0] == 'dasoraster':
                        versioninstalada=str(x[1].get('general',"version"))
                    if versioninstalada != dasoraster_version and dasoraster_version != 'v.0.0.0':
                        zip_ref_dasoraster = zipfile.ZipFile(dasoraster_filepath, 'r')
                        zip_ref_dasoraster.extractall(home_plugin_path)
                        zip_ref_dasoraster.close()
                        loadPlugin('dasoraster')
                        startPlugin('dasoraster')
                        try:  
                            QSettings().setValue('/PythonPlugins/dasoraster','true')
                        except:
                            pass
                            #pow

dasolidar_log = None
lista_usuarios_activos = []
lista_usuarios_grupo_activos = []
listaId332_check = ['benmarjo', 'dierabfr', 'monrodan']
if usuario_actual in listaId332_check or True:
   hacer_log_de_instalacion = True
   leer_lista_usuarios_dasolidar = True

if hacer_log_de_instalacion:
    (
        dasolidar_log,
        lista_usuarios_activos,
        lista_usuarios_grupo_activos
    ) = log_de_instalacion()

if leer_lista_usuarios_dasolidar:
    (
        listaId332_versionActual,
        listaId332_versionBeta
    ) = lista_usuarios_dasolidar(
        dasolidar_log,
    )
else:
    listaId332_versionActual = []
    listaId332_versionBeta = ['benmarjo', 'dierabfr', 'monrodan']

listaId332_versionAll = listaId332_versionActual.copy()
for mi_id332 in listaId332_versionBeta:
    if not mi_id332 in listaId332_versionAll:
        listaId332_versionAll.append(mi_id332)
for mi_id332 in listaId332_check:
    if not mi_id332 in listaId332_versionAll:
        listaId332_versionAll.append(mi_id332)

dasoraster_filepath_sigmena = 'O:/sigmena/utilidad/PROGRAMA/QGIS/Complementos/dasoraster.zip'
dasoraster_sigmena_disponible = os.path.exists(dasoraster_filepath_sigmena)
if not dasoraster_sigmena_disponible:
    try:
        if hacer_log_de_instalacion and dasolidar_log:
            dasolidar_log.write(f'Aviso:{separador_dasolistas}{usuario_actual}{separador_dasolistas}----{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}dasoraster no disponible en sigmena\n')
            dasolidar_log.write(f'Info:{separador_dasolistas}{usuario_actual}{separador_dasolistas}----{separador_dasolistas}{hoy_AAAAMMDD}{separador_dasolistas}dasoraster se lee (en todo caso) de la ubicacion de red\n')
    except:
        pass

if leer_lista_usuarios_dasolidar and hacer_log_de_instalacion:
    try:
        log_usuario_nuevo_modif(
            dasolidar_log,
            lista_usuarios_activos,
            lista_usuarios_grupo_activos,
            listaId332_versionBeta,
            listaId332_versionActual,
            dasoraster_sigmena_disponible,
        )
    except:
        pass
if leer_lista_usuarios_dasolidar and usuario_actual in listaId332_versionAll:
    try:
        instalacion_dasoraster(
            dasolidar_log,
            lista_usuarios_activos,
            lista_usuarios_grupo_activos,
            listaId332_versionBeta,
            listaId332_versionActual,
            dasoraster_filepath_sigmena,
        )
        if actualizar_enlaces_directos:
                pass
                # revisar_enlaces_directos(
                #     dasolidar_log,
                #     lista_usuarios_activos,
                #     lista_usuarios_grupo_activos,
                #     listaId332_versionBeta,
                #     listaId332_versionActual,
                # )
    except:
        pass

if hacer_log_de_instalacion and dasolidar_log:
    try:
        dasolidar_log.close()
    except:
        pass
# ==============================================================================
## Fin sigmena.py



# ==============================================================================
class VentanaBienvenidaPrimerosPasos(QDialog):
    def __init__(self, parent=None, contenido_ventana='primeros_pasos'):
        super().__init__(parent)
        print(f'betaraster-> -> Instanciando VentanaBienvenidaPrimerosPasos con contenido_ventana = {contenido_ventana}')
        self.ok = True
        if contenido_ventana == 'bienvenida':
            self.setWindowTitle('Bienvenido al proyecto dasolidar: productos y herramientas Lidar para la gestión del medio natural en Castilla y León')
            self.resize(900, 830)  #  Ancho y alto en píxeles
        elif contenido_ventana == 'primeros_pasos':
            self.setWindowTitle('Primeros pasos con dasolidar y el proyecto lidarQgis: productos y herramientas Lidar para la gestión del medio natural en Castilla y León')
            self.resize(950, 600)  #  Ancho y alto en píxeles
        else:
            self.setWindowTitle('Productos y herramientas Lidar para la gestión del medio natural en Castilla y León')
            self.resize(950, 600)  #  Ancho y alto en píxeles
        # self.setFixedSize(500, 200)  #  Dimensiones XX, YY
        # self.setGeometry(100, 100, 700, 400)
        self.center()

        # ======================================================================
        # html_path = r'D:\_clid\pyqgis'
        lidarData_path = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$'
        html_path = os.path.join(lidarData_path, r'dasoLidar\doc\ayudaDasolidar')
        # ======================================================================
        if os.path.isdir(lidarData_path):
            dl_bienvenida_html_filename = 'dasolidar_bienvenida.html'
            acceso_lidardata = True
        else:
            dl_bienvenida_html_filename = 'dasolidar_sin_acceso.html'
            acceso_lidardata = False
            print(f'betaraster-> No hay acceso_lidardata. dl_bienvenida_html_filename: {dl_bienvenida_html_filename}')

        dl_bienvenida_html_filepath = os.path.join(html_path, dl_bienvenida_html_filename) 
        if os.path.exists(dl_bienvenida_html_filepath):
            dl_bienvenida_html_obj = open(dl_bienvenida_html_filepath)
            dl_bienvenida_html_read = dl_bienvenida_html_obj.read()
        else:
            print(f'betaraster-> No existe dl_bienvenida_html_filepath: {dl_bienvenida_html_filepath}')
            dl_bienvenida_html_read = None
        # ======================================================================
        dl_primeros_pasos_html_filename = 'dasolidar_primeros_pasos.html'
        dl_primeros_pasos_html_filepath = os.path.join(html_path, dl_primeros_pasos_html_filename) 
        if os.path.exists(dl_primeros_pasos_html_filepath):
            dl_primeros_pasos_html_obj = open(dl_primeros_pasos_html_filepath)
            dl_primeros_pasos_html_read = dl_primeros_pasos_html_obj.read()
        else:
            print(f'betaraster-> No existe dl_primeros_pasos_html_filepath: {dl_primeros_pasos_html_filepath}')
            dl_primeros_pasos_html_read = None
        # ======================================================================

        # ======================================================================
        # Layout horizontal para el texto
        main_layout = QVBoxLayout()
        # ======================================================================
        mostrar_ventana_inicio = False
        self.mi_html = QTextBrowser()
        if contenido_ventana == 'bienvenida' or not acceso_lidardata:
            if dl_bienvenida_html_read:
                self.mi_html.setHtml(dl_bienvenida_html_read)
                mostrar_ventana_inicio = True
        elif contenido_ventana == 'primeros_pasos':
            if dl_primeros_pasos_html_read:
                self.mi_html.setHtml(dl_primeros_pasos_html_read)
                mostrar_ventana_inicio = True
        else:
            if dl_primeros_pasos_html_read:
                self.mi_html.setHtml(dl_primeros_pasos_html_read)
                mostrar_ventana_inicio = True
        # Ajusto el scroll para mostrar la parte superior
        # self.mi_html.verticalScrollBar().setValue(0)  #  Lo hago abajo
        if mostrar_ventana_inicio:
            main_layout.addWidget(self.mi_html)
        else:
            print(f'betaraster-> No semuestra mi_html: {type(self.mi_html)}')
        # Ajusto el scroll para mostrar la parte superior
        self.mi_html.verticalScrollBar().setValue(0)
        # ======================================================================
        # Layout horizontal para el checkbox y el botón 'Ok'

        checkbox_layout = QHBoxLayout()
        if contenido_ventana == 'bienvenida':
            checkbox_layout.setAlignment(Qt.AlignLeft)
        else:
            checkbox_layout.setAlignment(Qt.AlignCenter)
        if contenido_ventana == 'bienvenida' or contenido_ventana == 'primeros_pasos':
            # Checkbox desmarcado por defecto
            if contenido_ventana == 'bienvenida' or not acceso_lidardata:
                self.mostrar_checkbox = QCheckBox('Volver a mostrar esta ventana al iniciar este proyecto.')
            elif contenido_ventana == 'primeros_pasos':
                self.mostrar_checkbox = QCheckBox('Mostrar la ventana de bienvenida al iniciar este proyecto.')
            else:
                self.mostrar_checkbox = QCheckBox('Mostrar la ventana de bienvenida al iniciar este proyecto.')
            try:
                self.mostrar_checkbox.setChecked(config_class.dl_ventana_bienvenida)
            except (Exception) as mi_error:
                print(f'betaraster-> Error en setChecked {mi_error}')
                self.mostrar_checkbox.setChecked(True)
        else:
            self.mostrar_checkbox = None
        self.ok_button = QPushButton('Ok')
        self.ok_button.clicked.connect(self.accept)
        if contenido_ventana == 'bienvenida' or contenido_ventana == 'primeros_pasos':
            # main_layout.addWidget(self.mostrar_checkbox)
            checkbox_layout.addWidget(self.mostrar_checkbox)
        checkbox_layout.addWidget(self.ok_button)
        checkbox_layout.setAlignment(self.ok_button, Qt.AlignCenter)
        main_layout.addLayout(checkbox_layout)
        # ======================================================================

        # ======================================================================
        if contenido_ventana != 'bienvenida':
            # Establecer el layout principal
            self.setLayout(main_layout)
            return
        # ======================================================================

        # ======================================================================
        if mostrar_ventana_inicio:
            self.mi_label = QLabel(
                'Si se desactiva esta casilla, la documentación seguirá disponible'
                ' en los botones [Primeros pasos con dasolidar] y [Manual de consulta],'
                ' (barra de mensajes del canvas).\n'
                # '\nAdemás, próximamente, se habilitará un asistente para facilitar las consultas'
                'Además, el complemento dasoraster ofrece acceso a toda la documentación.'
            )
        else:
            self.mi_label = QLabel(
                'No se ha encontrado el documento de bienvenida o no está disponible.\n'
                'Esto puede ser debido a que se está iniciando este proyecto\n'
                'desde fuera de la intranet de la Junta de Castilla y León.\n'
                'En este caso, no hay acceso a las unidades de red con las que trabaja este proyecto.\n'
                'Para más información, consulte la documentación del proyecto dasolidar\n'
                'o remita un correo a dasolidar@gmail.com.'
            )
        self.mi_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.mi_label)
        # ======================================================================

        # ======================================================================
        # botones_layout_1 = QHBoxLayout()
        # self.ok_button = QPushButton('Ok')
        # self.ok_button.clicked.connect(self.accept)
        # botones_layout_1.addWidget(self.ok_button)
        # self.cancel_button = QPushButton('Cancelar')
        # self.cancel_button.clicked.connect(self.reject)
        # botones_layout_1.addWidget(self.cancel_button)
        # main_layout.addLayout(botones_layout_1)
        # ======================================================================

        # Marco para el texto y los botones
        marco_layout = QVBoxLayout()
        marco_widget = QWidget()
        marco_widget.setLayout(marco_layout)
        # marco_widget.setStyleSheet('border: 1px solid black; padding: 10px;')

        # Añadir espacio encima de la línea horizontal
        # spacer = QSpacerItem(1, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer = QSpacerItem(10, 10, QSizePolicy.Minimum)
        marco_layout.addItem(spacer)

        # Texto con marco
        # self.mi_label = QLabel('Si quieres consultar el manual dasolidar o iniciar el Asistente de consultas pulsa el correspondiente botón')
        mensaje_inferior1 = 'Puedes cerrar esta ventana, estos dos botones también seguirán disponibles.'
        self.mi_label_inf1 = QLabel(mensaje_inferior1)
        # self.mi_label.setAlignment(Qt.AlignLeft)
        self.mi_label_inf1.setAlignment(Qt.AlignCenter)
        self.mi_label_inf1.setStyleSheet('font-size: 12px; font-weight: bold;')  # Letra más grande y en negrita
        # self.mi_label.setStyleSheet('border: 1px solid black; padding: 10px;')
        marco_layout.addWidget(self.mi_label_inf1)
        if False:
            mensaje_inferior2 = 'Además de los mencionados botones el complemento dasoraster ofrece acceso a toda la documentación'
            self.mi_label_inf2 = QLabel(mensaje_inferior2)
            self.mi_label_inf2.setAlignment(Qt.AlignCenter)
            self.mi_label_inf2.setStyleSheet('font-size: 11px;')  # Letra normal
            marco_layout.addWidget(self.mi_label_inf2)
        if False:
            # Línea horizontal
            linea_horizontal2 = QFrame()
            linea_horizontal2.setFrameShape(QFrame.HLine)
            linea_horizontal2.setFrameShadow(QFrame.Sunken)
            marco_layout.addWidget(linea_horizontal2)
        # ======================================================================

        if acceso_lidardata:
            # Línea horizontal
            linea_horizontal1 = QFrame()
            linea_horizontal1.setFrameShape(QFrame.HLine)
            linea_horizontal1.setFrameShadow(QFrame.Sunken)
            marco_layout.addWidget(linea_horizontal1)

            # Layout horizontal para los botones
            botones_layout_2 = QHBoxLayout()
            # Añadir botones
            # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html
            self.infografia_button = QPushButton('Primeros pasos dasolidar')
            self.manual_button = QPushButton('Manual de consulta dasolidar')
            # self.ldata_button = QPushButton('Explorar LidarData')
            # self.asista_button = QPushButton('Asistente')
            # self.lasfile_button = QPushButton('cargar nube de puntos')
            # self.raster_button = QPushButton('Herramientas raster')

            self.infografia_button.setStyleSheet('font-size: 14px; font-weight: bold;')
            self.manual_button.setStyleSheet('font-size: 14px; font-weight: bold;')
            # self.ldata_button.setStyleSheet('font-size: 14px; font-weight: bold;')
            # self.asista_button.setStyleSheet('font-size: 14px; font-weight: bold;')
            # self.lasfile_button.setStyleSheet('font-size: 14px; font-weight: bold;')
            # self.raster_button.setStyleSheet('font-size: 14px; font-weight: bold;')

            # Conectar los botones a sus funciones
            # self.infografia_button.clicked.connect(self.primeros_pasos)
            self.infografia_button.clicked.connect(mostrar_ventana_bienvenida_primeros_pasos)
            self.manual_button.clicked.connect(mostrar_manual_dasolidar)
            # self.ldata_button.clicked.connect(self.mostrar_explorar_ldata)
            # self.asista_button.clicked.connect(
            #     # self.dasolidar_IA_consulta_ejecucion
            #     lambda event: self.dasolidar_IA_consulta_ejecucion(
            #         # mi_evento=event,
            #         # botones_disponibles='consulta_bengi',
            #         botones_disponibles='sugerencia_consulta_bengi',
            #     )
            # )
            # self.lasfile_button.clicked.connect(self.cargar_lasfile)
            # self.raster_button.clicked.connect(self.herramientas_raster)

            # Añadir los botones al layout horizontal
            botones_layout_2.addWidget(self.infografia_button)
            botones_layout_2.addWidget(self.manual_button)
            # botones_layout_2.addWidget(self.ldata_button)
            # botones_layout_2.addWidget(self.asista_button)
            # botones_layout_2.addWidget(self.lasfile_button)
            # botones_layout_2.addWidget(self.raster_button)
            # ======================================================================
            marco_layout.addLayout(botones_layout_2)
            # # Añadir el layout de botones al layout principal
            # main_layout.addLayout(botones_layout_2)
        # # ======================================================================
        main_layout.addWidget(marco_widget)
        # # ======================================================================
        # Establecer el layout principal
        self.setLayout(main_layout)
        # # ======================================================================
        # Ajusto el scroll para mostrar la parte superior
        self.mi_html.verticalScrollBar().setValue(0)
        # # ======================================================================

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())








# Copia de la versión de dasoraster
# ==============================================================================
class VentanaAsistente(QDialog):
    def __init__(self, parent=None, botones_disponibles='sugerencia_consulta_bengi'):
        print(f'betaraster-> Instanciando VentanaAsistente con botones_disponibles = {botones_disponibles}')
        super().__init__(parent)

        # botones_disponibles='consulta_bengi'
        # botones_disponibles='sugerencia_consulta_bengi'
        # botones_disponibles='sugerencia_consulta_bengi_vega'
        # botones_disponibles='sugerencia_consultas_ejecucion'

        print(f'betaraster-> botones_disponibles: {botones_disponibles}')
        if botones_disponibles == 'consulta_bengi':
            self.setWindowTitle('Disponible próximamente: aquí podrás escribir consultas.')
        elif botones_disponibles == 'sugerencia_consulta_bengi':
            self.setWindowTitle('Disponible próximamente: aquí podrás escribir consultas y sugerencias.')
        elif botones_disponibles == 'sugerencia_consultas_ejecucion':
            self.setWindowTitle('Disponible próximamente: aquí podrás escribir una consulta o pedir que se ejecute una acción')
        else:
            self.setWindowTitle('Disponible próximamente: aquí podrás escribir consultas.')
        # self.setFixedSize(500, 200)  #  Dimensiones XX, YY
        # self.setGeometry(100, 100, 700, 400)
        self.resize(600, 200)  #  Ancho y alto en píxeles
        self.center()

        # ======================================================================
        # Layout horizontal para el texto
        self.main_layout = QVBoxLayout()
        # Mensaje de texto
        self.mi_texto = QLabel('Escribe tu consulta o petición:')
        self.mi_texto.setAlignment(Qt.AlignLeft)
        self.main_layout.addWidget(self.mi_texto)

        # # Ventana de texto con tamaño fijo
        # self.text_input = QLineEdit(self)
        self.text_input = QTextEdit(self)
        self.text_input.setFixedSize(550, 100)  # Establece el tamaño (ancho, alto) en píxeles
        self.main_layout.addWidget(self.text_input)

        # ======================================================================
        # botones_layout = QHBoxLayout()
        # # Añadir botones
        # # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html
        # ======================================================================
        # Botones de Consulta, Acción y Cancelar
        self.buttonBox = QDialogButtonBox()
        # self.send_button = self.buttonBox.addButton('Enviar', QDialogButtonBox.AcceptRole)
        # ======================================================================

        # ======================================================================
        if botones_disponibles == 'consulta_bengi':
            self.consulta_bengi_button = self.buttonBox.addButton('Enviar consulta', QDialogButtonBox.AcceptRole)
            self.consulta_bengi_button.setToolTip("Haz clic aquí para enviar una consulta al equipo dasolidar.")
            self.consulta_bengi_button.clicked.connect(
                lambda event: self.lanzar_sugerencia_consulta_accion(
                    mi_evento=event,
                    tipo_consulta='bengi',
                )
            )
            self.consulta_bengi_button.setEnabled(True)
        elif botones_disponibles.startswith('sugerencia_consulta_bengi'):
            self.sugerencia_button = self.buttonBox.addButton('Enviar sugerencia', QDialogButtonBox.AcceptRole)
            self.sugerencia_button.setToolTip("Haz clic aquí para enviar una sugerencia o petición al equipo dasolidar.")
            self.sugerencia_button.clicked.connect(
                lambda event: self.lanzar_sugerencia_consulta_accion(
                    mi_evento=event,
                    tipo_consulta='sugerencia',
                )
            )
            self.sugerencia_button.setEnabled(True)
            if botones_disponibles =='sugerencia_consulta_bengi':
                self.consulta_bengi_button = self.buttonBox.addButton('Enviar consulta', QDialogButtonBox.AcceptRole)
                self.consulta_bengi_button.setToolTip("Haz clic aquí para enviar una consulta al equipo dasolidar.")
                self.consulta_bengi_button.clicked.connect(
                    lambda event: self.lanzar_sugerencia_consulta_accion(
                        mi_evento=event,
                        tipo_consulta='bengi',
                    )
                )
            elif botones_disponibles == 'sugerencia_consulta_bengi_vega':
                self.consulta_bengi_button = self.buttonBox.addButton('Consultar a humanos', QDialogButtonBox.AcceptRole)
                self.consulta_bengi_button.setToolTip("Haz clic aquí para enviar una consulta al equipo dasolidar.")
                self.consulta_vega_button = self.buttonBox.addButton('Consultar a Vega', QDialogButtonBox.AcceptRole)
                if usuario_beta:
                    self.consulta_vega_button.setToolTip("Haz clic aquí para enviar una consulta a Vega (IA).")
                else:
                    self.consulta_vega_button.setToolTip("Opción solo disponible para alfa testers.")
                self.consulta_bengi_button.clicked.connect(
                    lambda event: self.lanzar_sugerencia_consulta_accion(
                        mi_evento=event,
                        tipo_consulta='bengi',
                    )
                )
                self.consulta_bengi_button.setEnabled(True)
                self.consulta_vega_button.clicked.connect(
                    lambda event: self.lanzar_sugerencia_consulta_accion(
                        mi_evento=event,
                        tipo_consulta='vega',
                    )
                )
                if usuario_beta:
                    self.consulta_vega_button.setEnabled(True)
                else:
                    self.consulta_vega_button.setEnabled(False)
            self.consulta_bengi_button.setEnabled(True)
        elif botones_disponibles == 'sugerencia_consultas_ejecucion':
            self.sugerencia_button = self.buttonBox.addButton('Enviar sugerencia', QDialogButtonBox.AcceptRole)
            self.sugerencia_button.setToolTip("Haz clic aquí para enviar una sugerencia o petición al equipo dasolidar.")
            self.consulta_bengi_button = self.buttonBox.addButton('Consultar a humanos', QDialogButtonBox.AcceptRole)
            self.consulta_bengi_button.setToolTip("Haz clic aquí para enviar una consulta al equipo dasolidar.")
            self.consulta_vega_button = self.buttonBox.addButton('Consultar a Vega', QDialogButtonBox.AcceptRole)
            if usuario_beta:
                self.consulta_vega_button.setToolTip("Haz clic aquí para enviar una consulta a Vega (IA).")
            else:
                self.consulta_vega_button.setToolTip("Opción solo disponible para alfa testers.")
            self.accion_button = self.buttonBox.addButton('Ejecutar acción', QDialogButtonBox.AcceptRole)
            if usuario_beta:
                self.accion_button.setToolTip("Haz clic aquí para pedir a Vega que ejecute una acción. Pidelo con lenguaje natural, como lo harías a tu compañero de trabajo.")
            else:
                self.consulta_vega_button.setToolTip("Opción solo disponible para alfa testers.")
            self.sugerencia_button.clicked.connect(
                lambda event: self.lanzar_sugerencia_consulta_accion(
                    mi_evento=event,
                    tipo_consulta='sugerencia',
                )
            )
            self.consulta_bengi_button.clicked.connect(
                lambda event: self.lanzar_sugerencia_consulta_accion(
                    mi_evento=event,
                    tipo_consulta='bengi',
                )
            )
            self.consulta_vega_button.clicked.connect(
                lambda event: self.lanzar_sugerencia_consulta_accion(
                    mi_evento=event,
                    tipo_consulta='vega',
                )
            )
            self.accion_button.clicked.connect(
                # self.lanzar_accion
                lambda event: self.lanzar_sugerencia_consulta_accion(
                    mi_evento=event,
                    tipo_consulta='accion',
                )

            )

            self.sugerencia_button.setEnabled(True)
            self.consulta_bengi_button.setEnabled(True)
            if usuario_beta:
                self.consulta_vega_button.setEnabled(True)
                self.accion_button.setEnabled(True)
            else:
                self.consulta_vega_button.setEnabled(False)
                self.accion_button.setEnabled(False)
        else:
            self.consulta_bengi_button = self.buttonBox.addButton('Enviar consulta', QDialogButtonBox.AcceptRole)
            self.consulta_bengi_button.clicked.connect(
                lambda event: self.lanzar_sugerencia_consulta_accion(
                    mi_evento=event,
                    tipo_consulta='bengi',
                )
            )
            self.consulta_bengi_button.setEnabled(True)
        self.cancel_button = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.cancel_button.clicked.connect(self.reject)
        # ======================================================================

        # ======================================================================
        # Checkbox por si pido autorización para guardar la conaulta o petición en la base de datos
        self.guardar_consulta_checkbox = QCheckBox('Guardar sugerencia, petición, consulta o ejecución en fichero de texto para que esté a disposición de todos los usuarios.')
        self.guardar_consulta_checkbox.setChecked(True)
        self.main_layout.addWidget(self.guardar_consulta_checkbox)
        # ======================================================================

        # Añadir el layout de botones al layout principal
        # self.main_layout.addLayout(botones_layout)
        self.main_layout.addWidget(self.buttonBox)

        # Establecer el layout principal
        self.setLayout(self.main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_text(self):
        return self.text_input.toPlainText()

    def guardar_consulta(
            self,
            tipo_consulta,
        ):
        if tipo_consulta == 'bengi' or tipo_consulta == 'vega':
            clase_consulta = 'consulta'
        elif tipo_consulta == 'accion':
            clase_consulta = tipo_consulta
        else:
            clase_consulta = tipo_consulta

        unidad_v_path = 'V:/MA_SCAYLE_VueloLidar'
        mensajes_path = os.path.join(unidad_v_path, 'dasoraster')
        if os.path.isdir(unidad_v_path):
            if os.path.isdir(mensajes_path):
                unidad_V_disponible = True
            else:
                try:
                    os.mkdir(mensajes_path)
                    unidad_V_disponible = True
                except FileExistsError:
                    # Esto no debiera de pasar nunca, indica que algo falla al acceder a la ubicacion de red
                    unidad_V_disponible = False
                    print(f'betaraster-> El directorio "{mensajes_path}" ya existe.')
                except Exception as e:
                    unidad_V_disponible = False
                    print(f'betaraster-> Error al crear el directorio: {mensajes_path}')
                    print(f'betaraster-> Error: {e}')
        else:
            unidad_V_disponible = False
        if unidad_V_disponible:
            hoy_AAAAMMDD = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
            ahora_HHMMSS = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
            msg_filename = os.path.join(mensajes_path, f'{clase_consulta}s.dsl')
            try:
                msg_obj = open(msg_filename, mode='a+')
                msg_obj.seek(0)
                msg_previo = msg_obj.readlines()
            except Exception as e:
                print(f'betaraster-> Error al crear o abrir el fichero de mensajes: {msg_filename}')
                print(f'betaraster-> Error: {e}')
                msg_obj = None
                msg_previo = []
        else:
            msg_obj = None
            msg_previo = []
        msg_guardado_ok = False
        if msg_obj:
            texto_codificado_consulta = f'COD332\t{usuario_actual}\t{hoy_AAAAMMDD}\t{ahora_HHMMSS}\t{self.text_input.toPlainText()}\n'
            try:
                msg_obj.write(texto_codificado_consulta)
                msg_obj.close()
                msg_guardado_ok = True
                if (tipo_consulta == 'sugerencia' or tipo_consulta == 'bengi') and False:
                    QMessageBox.information(
                        iface.mainWindow(),
                        f'{clase_consulta} dasolidar',
                        f'Muchas gracias por tu {clase_consulta}.'
                        f'\nIntentaremos responder lo antes posible.'
                        f'\nLo haremos preferentemente por correo electrónico.'
                        f'\nTu e-mail: {usuario_actual}@jcyl.es'
                    )
            except Exception as e:
                print(f'betaraster-> Error al guardar el mensaje en {msg_filename}')
                print(f'betaraster-> Error: {e}')
        print(f'betaraster-> msg_guardado_ok: {msg_guardado_ok}')
        if tipo_consulta == 'sugerencia' or tipo_consulta == 'bengi':
            if not msg_guardado_ok:
                QMessageBox.information(
                    iface.mainWindow(),
                    f'{clase_consulta} dasolidar',
                    f'No ha sido posible registrar tu {clase_consulta}.'
                    f'\nEsta utilidad solo funciona dentro de la intranet de la JCyL.'
                    f'\nSi quieres hacer una {clase_consulta} puedes enviar'
                    f'\nun correo electrónico a {EMAIL_DASOLIDAR2}'
                )

    def enviar_consulta(
            self,
            tipo_consulta,
        ):
        if tipo_consulta == 'bengi' or tipo_consulta == 'vega':
            clase_consulta = 'consulta'
        else:
            clase_consulta = tipo_consulta
        hoy_AAAAMMDD = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        ahora_HHMMSS = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.To = EMAIL_DASOLIDAR1
            mail.Subject = f'dsld_{clase_consulta}_{usuario_actual}'
            texto_codificado_consulta = f'COD332\t{usuario_actual}\t{hoy_AAAAMMDD}\t{ahora_HHMMSS}\n{self.text_input.toPlainText()}\n'
            mail.Body = texto_codificado_consulta
            mail.Send()
            print(f'betaraster-> Mensaje enviado ok a {EMAIL_DASOLIDAR1}')
            mail = outlook.CreateItem(0)
            mail.To = EMAIL_DASOLIDAR2
            mail.Subject = f'dsld_{clase_consulta}_{usuario_actual}'
            texto_codificado_consulta = f'COD332\t{usuario_actual}\t{hoy_AAAAMMDD}\t{ahora_HHMMSS}\n{self.text_input.toPlainText()}\n'
            mail.Body = texto_codificado_consulta
            mail.Send()
            print(f'betaraster-> Mensaje enviado ok a {EMAIL_DASOLIDAR2}')
            iface.messageBar().pushMessage(
                title='dasoraster',
                text=f'Se ha enviado un correo electrónico con tu {clase_consulta} a {EMAIL_DASOLIDAR1}',
                # showMore=f'',
                duration=5,
                level=Qgis.Info,
            )
            if tipo_consulta == 'sugerencia' or tipo_consulta == 'bengi':
                QMessageBox.information(
                    iface.mainWindow(),
                    f'{clase_consulta} dasolidar',
                    f'Muchas gracias por tu {clase_consulta}.'
                    f'\nIntentaremos responder lo antes posible.'
                    f'\nLo haremos preferentemente por correo electrónico.'
                    f'\nTu e-mail: {usuario_actual}@jcyl.es'
                )

        except Exception as mi_error:
            print(f'betaraster-> Ocurrió un error al enviar el mail: {mi_error}')
            QMessageBox.information(
                iface.mainWindow(),
                f'{clase_consulta} dasolidar',
                f'No ha sido posible registrar tu {clase_consulta}.'
                f'\nEsta utilidad solo funciona dentro de la intranet de la JCyL.'
                f'\nSi quieres hacer una {clase_consulta} puedes enviar'
                f'\nun correo electrónico a {EMAIL_DASOLIDAR1}'
            )

    def lanzar_sugerencia_consulta_accion(
            self,
            mi_evento=None,
            mi_boton=None,
            tipo_consulta='bengi'
        ):
        if tipo_consulta == 'bengi' or tipo_consulta == 'vega':
            clase_consulta = 'consulta'
        else:
            clase_consulta = tipo_consulta
        print(f'betaraster-> lanzar_sugerencia_consulta_accion -> tipo_consulta {tipo_consulta}')
        self.button_pressed = f'consulta_{tipo_consulta}'
        self.accept()
        print(f'betaraster-> Botón presionado: {self.button_pressed}. Texto introducido: {self.text_input.toPlainText()}')
        print(f'betaraster-> guardar_consulta_checkbox: {self.guardar_consulta_checkbox.isChecked()}')
        if tipo_consulta == 'sugerencia' or tipo_consulta == 'bengi' or tipo_consulta == 'vega':
            guardar_consultas_en_txt = True
            enviar_consultas_por_mail = True
            if self.guardar_consulta_checkbox.isChecked() and guardar_consultas_en_txt:
                self.guardar_consulta(tipo_consulta)
            if enviar_consultas_por_mail and tipo_consulta != 'accion':
                self.enviar_consulta(tipo_consulta)
        if tipo_consulta == 'vega':
            QMessageBox.information(
                iface.mainWindow(),
                f'Consulta dasolidar <{clase_consulta}>',
                f'Esta utilidad estará disponible próximamente\n\nGracias por la consulta.'
            )
        if tipo_consulta == 'accion':
            QMessageBox.information(
                iface.mainWindow(),
                f'Acción dasolidar <{clase_consulta}>',
                f'Esta utilidad estará disponible próximamente.'
            )
        # return (self.text_input.toPlainText(), 'consulta')

    # def lanzar_accion(self):
    #     print(f'betaraster-> lanzar_accion')
    #     self.button_pressed = 'accion'
    #     self.accept()
    #     print(self.text_input.toPlainText(), 'accion')
    #     QMessageBox.information(
    #         iface.mainWindow(),
    #         'Petición dasolidar',
    #         f'Gracias por la petición.\nEsta utilidad estará disponible próximamente'
    #     )
    #     # return (self.text_input.toPlainText(), 'accion')


# ==============================================================================
# ==============================================================================
def mostrar_ventana_bienvenida_primeros_pasos(
        mi_evento=None,
        mi_boton=None,
        contenido_ventana='primeros_pasos'
    ):
    global config_class
    print(f'betaraster-> Se va a instanciar VentanaBienvenidaPrimerosPasos desde mostrar_ventana_bienvenida_primeros_pasos')
    dialog = VentanaBienvenidaPrimerosPasos(contenido_ventana=contenido_ventana)
    if dialog.ok:
        rpta_ok = dialog.exec_()
    if rpta_ok == QDialog.Accepted and dialog.mostrar_checkbox:
        if dialog.mostrar_checkbox.isChecked():
            # print(f'betaraster-> Seguir mostrando la ventana de bienvenida')
            config_class.dl_ventana_bienvenida = True
            config_class.dl_message_bienvenida = True
        else:
            # print(f'betaraster-> No mostrar la ventana de bienvenida')
            config_class.dl_ventana_bienvenida = False
            config_class.dl_message_bienvenida = True
        mi_config.setValue('dasolidar/dl_ventana_bienvenida', config_class.dl_ventana_bienvenida)
        mi_config.setValue('dasolidar/dl_message_bienvenida', config_class.dl_message_bienvenida)

# ==============================================================================
def mostrar_manual_dasolidar():
    # ruta_manual = os.path.dirname(__file__)
    ruta_manual = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$\dasoLidar\doc\ayudaDasolidar'
    pdf_path = os.path.join(ruta_manual, 'manualDasoLidar.pdf')
    if os.path.exists(pdf_path):
        print(f'betaraster-> pdf_path_ok: {pdf_path}')
        if platform.system() == 'Windows':
            os.startfile(pdf_path)
    else:
        print(f'betaraster-> Fichero no disponible: {pdf_path}')


# ==============================================================================
def mostrar_explorar_ldata(
        mi_evento=None,
        explorar_directorio='',
):
    print(f'betaraster-> ---> explorar_ldata')
    ldata_path = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$'
    target_path = os.path.join(ldata_path, explorar_directorio)
    if os.path.exists(target_path):
        print(f'betaraster-> Directorio disponible ok: {target_path}')
    else:
        print(f'betaraster-> Directorio no accesible: {target_path}')
        iface.messageBar().pushMessage(
            title='dasoraster',
            text=f'No hay acceso a la unidad de red {target_path}.',
            showMore=f'Esto puede ser debido a:\n  1. El usuario {config_class.dl_usuario} no está dado de alta en la lista de usuarios del proyecto dasolidar\n  2. Se está trabajando fuera de la intranet de la Junta de Castilla y León.\n\nEste recurso solo está disponible para los usuarios del proyecto dasolidar con acceso a la intranet de la Junta de Castilla y León',
            duration=30,
            level=Qgis.Warning,
        )
        return
    try:
        rpta_ok = subprocess.Popen(f'explorer "{target_path}"')
    except Exception as mi_error:
        print(f'betaraster-> Ocurrió un error al abrir el explorador de Windows: {mi_error}')

    # print(f'betaraster-> Rpta de explorar_ldata: {type(rpta_ok)}')  #  <class 'subprocess.Popen'>
    print(f'betaraster-> Directorio explorado: {rpta_ok.args}')
    print(f'betaraster-> Respuesta: {rpta_ok.returncode}')


# ==============================================================================
def dasolidar_IA_consulta_ejecucion(
        mi_evento=None,
        mi_boton=None,
        # botones_disponibles='consulta_bengi',
        # botones_disponibles='sugerencia_consulta_bengi',
        botones_disponibles='sugerencia_consultas_ejecucion'
    ):
    print(f'betaraster-> dasolidar_IA_consulta_ejecucion ok 1. botones_disponibles: {type(botones_disponibles)} {botones_disponibles}')
    rpta_ok = 0
    try:
        dialog = VentanaAsistente(parent=None, botones_disponibles=botones_disponibles)
        rpta_ok = dialog.exec_()
    except Exception as e:
        print(f'betaraster-> Ocurrió un error al mostrar la ventana 1: {e}')
        iface.messageBar().pushMessage(
            title='dasoraster',
            text=f'Ha ocurrido un error al lanzar el cuadro de diálogo del asistente. Contacta con benmarjo@jcyl.es para reportar este error.',
            duration=30,
            level=Qgis.Warning,
        )
        return
    # Esto siguiente sobra; lo dejo just in case
    print(f'betaraster-> Rpta de mostrar_asistente 1: {rpta_ok}')
    if rpta_ok == QDialog.Accepted:
        consulta_usuario = dialog.get_text()
        boton_pulsado = dialog.button_pressed
        print(f'betaraster-> Texto de consulta o petición (1):', consulta_usuario)
        print(f'betaraster-> Botón pulsado:', boton_pulsado)
    else:
        print(f'betaraster-> Consulta o petición canceladas')


# ==============================================================================
# Asegúrate de que QGIS esté inicializado
if False:
    QgsApplication.setPrefixPath('C:/OSGeo4W/bin', True)
    qgs = QgsApplication([], False)
    qgs.initQgis()


# ==============================================================================
def checquear_message_bar(text):
    current_message = iface.messageBar().currentItem()
    if current_message and False:
        print(f'betaraster-> Se oculta este messageBar: {current_message.title()} {current_message.text()}')
        current_message.hide()
        current_message.show()

    # Verificar si el mensaje actual contiene el texto
    if current_message:
        if text in current_message.text():
            return True
        elif (
            'SIGMENA:' in current_message.title()
            or 'Actualizada la cartografía SIGPAC' in current_message.text()
            or 'Actualizada la cartograf�a SIGPAC' in current_message.text()
            or 'Se ha leído correctamente la contraseña' in current_message.text()
        ):
            print(f'betaraster-> Se retira este messageBar: {current_message.title()} {current_message.text()}')
            current_message.dismiss()
            return checquear_message_bar(text)
    return False


# ==============================================================================
def mostrar_messagebar_bienvenida():
    # https://qgis.org/pyqgis/master/gui/QgsMessageBar.html
    # https://qgis.org/pyqgis/master/gui/QgsMessageBarItem.html#qgis.gui.QgsMessageBarItem
    print(f'betaraster-> mostrar_messagebar_bienvenida-> se conecta el boton con mostrar_ventana_bienvenida_primeros_pasos')

    titulo_mensaje = '¿Por dónde empiezo? '
    texto_mensaje = f'\t\t\t\t\t\t\t\t\t\tPulsa alguno de los siguientes botones.'
    if not checquear_message_bar(texto_mensaje[-30:]):
        mi_widget = iface.messageBar().createMessage(
            title=titulo_mensaje,
            # text=f'Pulsa el botón [Primeros pasos con dasolidar] para mostrar la ayuda rápida.',
            text=texto_mensaje,
        )
        mi_widget.setLevel(Qgis.Info)
        # mi_widget.setDuration(30)
        mi_button1 = QPushButton(mi_widget)
        mi_button2 = QPushButton(mi_widget)
        mi_button3 = QPushButton(mi_widget)
        mi_button4 = QPushButton(mi_widget)
        mi_button5 = QPushButton(mi_widget)
        mi_button1.setText('Primeros pasos con dasolidar')
        mi_button2.setText('Manual de consulta')
        mi_button3.setText('Explorar lidarData')
        mi_button4.setText('Asistente dasolidar')
        mi_button5.setText('Curso Lidar')
        # mi_button1.pressed.connect(mostrar_html_qt)
        # mi_button1.pressed.connect(mostrar_html_qgs)
        mi_button1.pressed.connect(
            mostrar_ventana_bienvenida_primeros_pasos
            # lambda event: mostrar_ventana_bienvenida_primeros_pasos(
            #     mi_evento=event,
            #     contenido_ventana='primeros_pasos'
            # )
        )
        mi_button2.pressed.connect(mostrar_manual_dasolidar)
        mi_button3.pressed.connect(mostrar_explorar_ldata)
        mi_button4.pressed.connect(
            dasolidar_IA_consulta_ejecucion
            # lambda event: dasolidar_IA_consulta_ejecucion(
            #     mi_evento=event,
            #     botones_disponibles='sugerencia_consultas_ejecucion'
            # )
        )
        mi_button5.pressed.connect(
            lambda: mostrar_explorar_ldata(
                explorar_directorio=r'dasoLidar\varios\cursoLidar'
            )
        )
        # ==============================================================================
        mi_widget.layout().addWidget(mi_button1)
        mi_widget.layout().addWidget(mi_button2)
        mi_widget.layout().addWidget(mi_button3)
        mi_widget.layout().addWidget(mi_button4)
        mi_widget.layout().addWidget(mi_button5)
        iface.messageBar().pushWidget(mi_widget, Qgis.Info)


# ==============================================================================
def arranque_dasolidar():
    if config_class.dl_ventana_bienvenida or not acceso_lidardata:
        mostrar_ventana_bienvenida_primeros_pasos(
            contenido_ventana='bienvenida'
        )
    if config_class.dl_message_bienvenida:
        mostrar_messagebar_bienvenida()

if __name__ == '__main__':
    arranque_dasolidar()
    # QgsMessageLog.logMessage('Carga dasolidar ok', level=Qgis.Info)
