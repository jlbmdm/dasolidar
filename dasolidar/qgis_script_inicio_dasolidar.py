# -*- coding: UTF-8 -*-
import os
import sys
import subprocess

import numpy as np

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
from qgis.utils import iface
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

# ==============================================================================
html_path = r'D:\_clid\pyqgis'
# ==============================================================================
intro_dasolidar_html_filename = 'dasolidar_intro.html'
intro_dasolidar_html_filepath = os.path.join(html_path, intro_dasolidar_html_filename) 
intro_dasolidar_html_obj = open(intro_dasolidar_html_filepath)
intro_dasolidar_html_read = intro_dasolidar_html_obj.read()
# ==============================================================================
intro_dasolidar_txt_filename = 'dasolidar_intro.txt'
intro_dasolidar_txt_filepath = os.path.join(html_path, intro_dasolidar_txt_filename) 
intro_dasolidar_txt_obj = open(intro_dasolidar_txt_filepath)
intro_dasolidar_txt_read = intro_dasolidar_txt_obj.read()
# ==============================================================================

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
        self.dl_mostrar_ventana_bienvenida = mi_config.value('dasolidar/mostrar_ventana_bienvenida', True)
        self.dl_mostrar_message_bienvenida = mi_config.value('dasolidar/mostrar_message_bienvenida', True)



# ==============================================================================
config_class = Configuracion()
print(f'dl_mostrar_ventana_bienvenida 1: ({type(config_class.dl_mostrar_ventana_bienvenida)}) {config_class.dl_mostrar_ventana_bienvenida}')
if type(config_class.dl_mostrar_ventana_bienvenida) == str:
    config_class.dl_mostrar_ventana_bienvenida = str_to_bool(config_class.dl_mostrar_ventana_bienvenida)
print(f'dl_mostrar_ventana_bienvenida 2: ({type(config_class.dl_mostrar_ventana_bienvenida)}) {config_class.dl_mostrar_ventana_bienvenida}')
# ==============================================================================


class VentanaAsistente(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Aquí puedes escribir una consulta o pedir que se ejecute una acción')
        # self.setFixedSize(500, 200)  #  Dimensiones XX, YY
        # self.setGeometry(100, 100, 700, 400)
        self.resize(600, 200)  #  Ancho y alto en píxeles
        self.center()

        # ======================================================================
        # Layout horizontal para el texto
        self.texto_layout = QVBoxLayout()
        # Mensaje de texto
        self.mi_texto = QLabel('Escribe tu consulta o petición:')
        self.mi_texto.setAlignment(Qt.AlignLeft)
        self.texto_layout.addWidget(self.mi_texto)

        # # Ventana de texto con tamaño fijo
        # self.text_input = QLineEdit(self)
        self.text_input = QTextEdit(self)
        self.text_input.setFixedSize(550, 100)  # Establece el tamaño (ancho, alto) en píxeles
        self.texto_layout.addWidget(self.text_input)

        # ======================================================================
        # botones_layout = QHBoxLayout()
        # # Añadir botones
        # # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html
        # self.consulta_button = QPushButton('Enviar consulta')
        # self.accion_button = QPushButton('Ejecutar acción')
        # self.cancel_button = QPushButton('Cancelar')
        # ======================================================================
        # Botones de Consulta, Acción y Cancelar
        self.buttonBox = QDialogButtonBox()
        # self.send_button = self.buttonBox.addButton('Enviar', QDialogButtonBox.AcceptRole)
        self.consulta_button = self.buttonBox.addButton('Enviar consulta', QDialogButtonBox.AcceptRole)
        self.accion_button = self.buttonBox.addButton('Ejecutar acción', QDialogButtonBox.AcceptRole)
        self.cancel_button = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        # Conectar los botones a sus funciones
        self.consulta_button.clicked.connect(self.lanzar_consulta)
        self.accion_button.clicked.connect(self.lanzar_accion)
        self.cancel_button.clicked.connect(self.reject)
        # # Añadir los botones al layout horizontal
        # botones_layout.addWidget(self.consulta_button)
        # botones_layout.addWidget(self.accion_button)
        # botones_layout.addWidget(self.cancel_button)
        # ======================================================================

        # ======================================================================
        # Checkbox por si pido autorización para guardar la conaulta o petición en la base de datos
        self.checkbox = QCheckBox('Guardar consulta o petición.')
        self.checkbox.setChecked(True)
        self.texto_layout.addWidget(self.checkbox)
        # ======================================================================

        # Añadir el layout de botones al layout principal
        # self.texto_layout.addLayout(botones_layout)
        self.texto_layout.addWidget(self.buttonBox)

        # Establecer el layout principal
        self.setLayout(self.texto_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_text(self):
        return self.text_input.toPlainText()

    def lanzar_consulta(self):
        print('---> lanzar_consulta')
        self.button_pressed = 'consulta'
        self.accept()
        print(self.text_input.toPlainText(), 'consulta')
        # return (self.text_input.toPlainText(), 'consulta')

    def lanzar_accion(self):
        print('---> lanzar_accion')
        self.button_pressed = 'accion'
        self.accept()
        print(self.text_input.toPlainText(), 'accion')
        # return (self.text_input.toPlainText(), 'accion')


# ==============================================================================
class VentanaUsarRaster(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Herramientas raster dasolidar')
        self.resize(300, 150)  # Ancho y alto en píxeles

        # Layout vertical para el contenido
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Texto de la ventana
        label = QLabel('Esta utilidad estará disponible próximamente')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum)
        layout.addItem(spacer)

        # Botón Ok
        ok_button = QPushButton('Ok')
        ok_button.setFixedSize(100, 20)
        ok_button.clicked.connect(self.accept)
        # layout.addWidget(ok_button)

        # Alineación del botón Ok al centro
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        button_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout)

        self.setLayout(layout)



# ==============================================================================
class VentanaCargarLasFile(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cargar nube de puntos (lasFile)')
        self.resize(300, 150)  # Ancho y alto en píxeles

        # Layout vertical para el contenido
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Texto de la ventana
        label = QLabel('Esta utilidad estará disponible próximamente')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum)
        layout.addItem(spacer)

        # Botón Ok
        ok_button = QPushButton('Ok')
        ok_button.setFixedSize(100, 20)
        ok_button.clicked.connect(self.accept)
        # layout.addWidget(ok_button)

        # Alineación del botón Ok al centro
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        button_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout)


        self.setLayout(layout)


# ==============================================================================
class VentanaBienvenida(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Productos y herramientas Lidar para la gestión del medio natural')
        # self.setFixedSize(500, 200)  #  Dimensiones XX, YY
        # self.setGeometry(100, 100, 700, 400)
        self.resize(950, 600)  #  Ancho y alto en píxeles
        self.center()

        # ======================================================================
        # Layout horizontal para el texto
        texto_layout = QVBoxLayout()
        usar_html = True
        if usar_html:
            self.mi_texto = QTextBrowser()
            self.mi_texto.setHtml(intro_dasolidar_html_read)
        else:
            self.mi_texto = QLabel(intro_dasolidar_txt_read)
            self.mi_texto.setAlignment(Qt.AlignLeft)
        texto_layout.addWidget(self.mi_texto)
        # ======================================================================

        # ======================================================================
        # Layout horizontal para el checkbox y el botón 'Ok'
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignLeft)
        # Checkbox desmarcado por defecto
        self.checkbox = QCheckBox('Volver a mostrar esta ventana al iniciar este proyecto.')
        try:
            self.checkbox.setChecked(config_class.dl_mostrar_ventana_bienvenida)
        except (Exception) as mi_error:
            print(f'Error en setChecked {mi_error}')
            self.checkbox.setChecked(True)
        # ======================================================================

        self.ok_button = QPushButton('Ok')
        self.ok_button.clicked.connect(self.accept)
        # texto_layout.addWidget(self.checkbox)
        checkbox_layout.addWidget(self.checkbox)
        checkbox_layout.addWidget(self.ok_button)
        texto_layout.addLayout(checkbox_layout)
        # ======================================================================

        self.mi_label = QLabel('Si se desactiva esta casilla la ventana estará disponible en el botón [Bienvenido a dasolidar] de la barra de mensajes en la parte superior del panel del mapa')
        self.mi_label.setAlignment(Qt.AlignLeft)
        texto_layout.addWidget(self.mi_label)

        # ======================================================================

        # ======================================================================
        # botones_layout_1 = QHBoxLayout()
        # self.ok_button = QPushButton('Ok')
        # self.ok_button.clicked.connect(self.accept)
        # botones_layout_1.addWidget(self.ok_button)

        # self.cancel_button = QPushButton('Cancelar')
        # self.cancel_button.clicked.connect(self.reject)
        # botones_layout_1.addWidget(self.cancel_button)

        # texto_layout.addLayout(botones_layout_1)
        # ======================================================================

        # Marco para el texto y los botones
        marco_layout = QVBoxLayout()
        marco_widget = QWidget()
        marco_widget.setLayout(marco_layout)
        # marco_widget.setStyleSheet('border: 1px solid black; padding: 10px;')

        # Añadir espacio encima de la línea horizontal
        # spacer = QSpacerItem(1, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum)
        marco_layout.addItem(spacer)

        # Línea horizontal
        linea_horizontal = QFrame()
        linea_horizontal.setFrameShape(QFrame.HLine)
        linea_horizontal.setFrameShadow(QFrame.Sunken)
        marco_layout.addWidget(linea_horizontal)

        # Texto con marco
        self.mi_label = QLabel('Si quieres iniciar el Asistente dasolidar o  cargar una nube de puntos o mostrar una capa ráster Pulsa el correspondiente botón')
        # self.mi_label.setAlignment(Qt.AlignLeft)
        self.mi_label.setAlignment(Qt.AlignCenter)
        self.mi_label.setStyleSheet('font-size: 12px; font-weight: bold;')  # Letra más grande y en negrita
        # self.mi_label.setStyleSheet('border: 1px solid black; padding: 10px;')
        marco_layout.addWidget(self.mi_label)

        # ======================================================================
        # Layout horizontal para los botones
        botones_layout_2 = QHBoxLayout()
        # Añadir botones
        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html
        self.asista_button = QPushButton('Asistente')
        self.lasfile_button = QPushButton('Nube de puntos')
        self.raster_button = QPushButton('Herramientas raster')
        self.ldata_button = QPushButton('Explorar LidarData')

        self.asista_button.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.lasfile_button.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.raster_button.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.ldata_button.setStyleSheet('font-size: 14px; font-weight: bold;')

        # Conectar los botones a sus funciones
        self.asista_button.clicked.connect(self.asistente)
        self.lasfile_button.clicked.connect(self.cargar_lasfile)
        self.raster_button.clicked.connect(self.herramientas_raster)
        self.ldata_button.clicked.connect(self.explorar_ldata)
        # Añadir los botones al layout horizontal
        botones_layout_2.addWidget(self.asista_button)
        botones_layout_2.addWidget(self.lasfile_button)
        botones_layout_2.addWidget(self.raster_button)
        botones_layout_2.addWidget(self.ldata_button)
        # ======================================================================
        marco_layout.addLayout(botones_layout_2)
        # # Añadir el layout de botones al layout principal
        # texto_layout.addLayout(botones_layout_2)
        # # ======================================================================


        texto_layout.addWidget(marco_widget)

        # Establecer el layout principal
        self.setLayout(texto_layout)

    def asistente(self):
        print('---> asistente')
        mostrar_asistente()

    def cargar_lasfile(self):
        print('---> cargar_lasfile')
        dialog = VentanaCargarLasFile()
        rpta_ok = dialog.exec_()
        print(f'Rpta de cargar_lasfile: {rpta_ok}')
        # if rpta_ok == QDialog.Accepted:
        #     consulta_usuario = dialog.get_text()
        #     boton_pulsado = dialog.button_pressed
        #     print('Texto de consulta o petición:', consulta_usuario)
        #     print('Botón pulsado:', boton_pulsado)
        # else:
        #     print('Consulta o petición canceladas')



    def herramientas_raster(self):
        print('---> herramientas_raster')
        dialog = VentanaUsarRaster()
        rpta_ok = dialog.exec_()
        print(f'Rpta de herramientas_raster: {rpta_ok}')

        # Parámetros de entrada
        capa_VCC = 'VCC____IFNxPNOA2'
        capa_raster_vcc = QgsProject.instance().mapLayersByName(capa_VCC)
        if capa_raster_vcc:
            capa_raster = capa_raster_vcc[0]  # Usar la capa 'VCC' si está cargada
        else:
            capa_raster = iface.activeLayer()  # Usar la capa activa si 'VCC' no está cargada
            print(f'Capa {capa_VCC} no encontrada; se consulta la capa activa: {capa_raster.name()}')
        x_consulta = 333500  #  Coordenada X del punto de consulta
        y_consulta = 4749700  #  Coordenada Y del punto de consulta
        mi_radio = 15  #  Radio en unidades de la capa ráster
        
        # Llamar a la función
        calcular_valor_medio(capa_raster, x_consulta, y_consulta, mi_radio)
        



    def explorar_ldata(self):
        print('---> explorar_ldata')
        ldata_path = r'\\repoarchivohm.jcyl.red\MADGMNSVPI_SCAYLEVueloLIDAR$'
        rpta_ok = subprocess.Popen(f'explorer "{ldata_path}"')
        print(f'Rpta de explorar_ldata: {type(rpta_ok)}')  #  <class 'subprocess.Popen'>
        print(f'Directorio explorado: {rpta_ok.args}')
        print(f'Respuesta: {rpta_ok.returncode}')
        # print(dir(rpta_ok))
        [
            '__class__', '__class_getitem__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_timeout', '_child_created', '_close_pipe_fds', '_closed_child_pipe_fds', '_communicate', '_communication_started', '_execute_child', '_filter_handle_list', '_get_devnull', '_get_handles', '_handle', '_input', '_internal_poll', '_make_inheritable', '_on_error_fd_closer', '_readerthread', '_remaining_time', '_sigint_wait_secs', '_stdin_write', '_translate_newlines', '_wait', '_waitpid_lock',
            'args', 'communicate', 'encoding', 'errors', 'kill', 'pid',
            'pipesize', 'poll', 'returncode', 'send_signal', 'stderr', 'stdin',
            'stdout', 'terminate', 'text_mode', 'universal_newlines', 'wait'
         ]

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



# ==============================================================================
def mostrar_ventana_bienvenida():
    global config_class
    dialog = VentanaBienvenida()
    rpta_ok = dialog.exec_()
    if rpta_ok == QDialog.Accepted:
        print('OK presionado')
        if dialog.checkbox.isChecked():
            print('Seguir mostrando la ventana de bienvenida')
            config_class.dl_mostrar_ventana_bienvenida = True
            config_class.dl_mostrar_message_bienvenida = True
        else:
            print('No mostrar la ventana de bienvenida')
            config_class.dl_mostrar_ventana_bienvenida = False
            config_class.dl_mostrar_message_bienvenida = True
        mi_config.setValue('dasolidar/mostrar_ventana_bienvenida', config_class.dl_mostrar_ventana_bienvenida)
        mi_config.setValue('dasolidar/mostrar_message_bienvenida', config_class.dl_mostrar_message_bienvenida)
        # print(f'dl_mostrar_ventana_bienvenida 3: ({type(config_class.dl_mostrar_ventana_bienvenida)}) {config_class.dl_mostrar_ventana_bienvenida}')
    else:
        print('Cancelar presionado')


# ==============================================================================
def mostrar_asistente():
    dialog = VentanaAsistente()
    rpta_ok = dialog.exec_()
    print(f'Rpta de mostrar_asistente: {rpta_ok}')
    if rpta_ok == QDialog.Accepted:
        consulta_usuario = dialog.get_text()
        boton_pulsado = dialog.button_pressed
        print('Texto de consulta o petición:', consulta_usuario)
        print('Botón pulsado:', boton_pulsado)
    else:
        print('Consulta o petición canceladas')



# ==============================================================================
# Asegúrate de que QGIS esté inicializado
if False:
    QgsApplication.setPrefixPath('C:/OSGeo4W/bin', True)
    qgs = QgsApplication([], False)
    qgs.initQgis()


# ==============================================================================
def mostrar_html_qt():
    # dialog = QDialog(buttons=QDialogButtonBox.StandardButtons)
    dialog = QDialog()

    dialog.setWindowTitle('Bienvenido a dasolidar')
    layout = QVBoxLayout()
    text_browser = QTextBrowser()
    text_browser.setHtml(intro_dasolidar_html_read)
    layout.addWidget(text_browser)
    dialog.setLayout(layout)
    dialog.exec_()


# ==============================================================================
def mostrar_html_qgs():
    # https://qgis.org/pyqgis/3.34/gui/QgsDialog.html
    main_window = iface.mainWindow()
    dialog = QgsDialog(main_window,
                       fl=Qt.WindowFlags(),
                       buttons=QDialogButtonBox.Ok | QDialogButtonBox.Close,
                       orientation=Qt.Horizontal)
    text_browser = QTextBrowser()
    text_browser.setHtml(intro_dasolidar_html_read)
    # dialog.addWidget(text_browser)
    dialog.resize(600, 400)
    dialog.show()


# ==============================================================================
def checquear_message_bar(text):
    current_message = iface.messageBar().currentItem()
    if current_message and False:
        print(f'Se oculta este messageBar: {current_message.title()} {current_message.text()}')
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
            print(f'Se retira este messageBar: {current_message.title()} {current_message.text()}')
            current_message.dismiss()
            return checquear_message_bar(text)
    return False


# ==============================================================================
def mostrar_messagebar_bienvenida():
    # https://qgis.org/pyqgis/master/gui/QgsMessageBar.html
    # https://qgis.org/pyqgis/master/gui/QgsMessageBarItem.html#qgis.gui.QgsMessageBarItem

    titulo_mensaje = '¿Por dónde empiezo? '
    texto_mensaje = f'\t\t\t\t\t\t\t\t\t\tPulsa alguno de los siguientes botones.'
    if not checquear_message_bar(texto_mensaje[-30:]):
        mi_widget = iface.messageBar().createMessage(
            title=titulo_mensaje,
            # text=f'Pulsa el botón [Bienvenido a dasolidar] para mostrar la ayuda rápida.',
            text=texto_mensaje,
        )
        mi_widget.setLevel(Qgis.Info)
        # mi_widget.setDuration(30)
        mi_button1 = QPushButton(mi_widget)
        mi_button2 = QPushButton(mi_widget)
        mi_button1.setText('Bienvenido a dasolidar')
        mi_button2.setText('Asistente dasolidar')
        # mi_button1.pressed.connect(mostrar_html_qt)
        # mi_button1.pressed.connect(mostrar_html_qgs)
        mi_button1.pressed.connect(mostrar_ventana_bienvenida)
        mi_button2.pressed.connect(mostrar_asistente)
        # ==============================================================================
        mi_widget.layout().addWidget(mi_button1)
        mi_widget.layout().addWidget(mi_button2)
        iface.messageBar().pushWidget(mi_widget, Qgis.Info)


if False:
    iface.messageBar().pushMessage(
        title='dasolidar',
        text='Bienvenido al proyecto dasolidar',
        showMore=f'Información sobre el proyecto dasolidar:{intro_dasolidar_txt_read}',
        level=Qgis.Info,
        duration=10,
    )


# ==============================================================================
def calcular_valor_medio(capa_raster, x_consulta, y_consulta, mi_radio):
    # Obtener la capa ráster
    raster_layer = capa_raster

    # Crear un rectángulo de consulta (buffer)
    consulta_rect = QgsRectangle(x_consulta - mi_radio, y_consulta - mi_radio, x_consulta + mi_radio, y_consulta + mi_radio)

    # Obtener los datos ráster dentro del rectángulo de consulta
    provider = raster_layer.dataProvider()
    extent = consulta_rect
    rows = int(extent.height() / raster_layer.rasterUnitsPerPixelY())
    cols = int(extent.width() / raster_layer.rasterUnitsPerPixelX())
    block = provider.block(1, extent, cols, rows)


    # Extraer los valores de los píxeles dentro del círculo
    valores_circulo = []
    for i in range(rows):
        for j in range(cols):
            x_pixel = extent.xMinimum() + j * raster_layer.rasterUnitsPerPixelX()
            y_pixel = extent.yMaximum() - i * raster_layer.rasterUnitsPerPixelY()
            distancia = np.sqrt((x_pixel - x_consulta)**2 + (y_pixel - y_consulta)**2)
            if distancia <= mi_radio:
                valor = block.value(i, j)
                if valor != provider.sourceNoDataValue(1):  # Ignorar valores NoData
                    valores_circulo.append(valor)

    # Extraer los valores de los píxeles dentro del cuadrado
    valores_cuadrado = []
    for i in range(rows):
        for j in range(cols):
            valor = block.value(i, j)
            if valor != provider.sourceNoDataValue(1):  # Ignorar valores NoData
                valores_cuadrado.append(valor)

    valores_selec = valores_circulo

    # Calcular el valor medio
    if valores_selec:
        valor_medio = np.mean(valores_selec)
        print(f'Valor medio: {valor_medio}')
    else:
        print('No se encontraron valores válidos en el área de consulta.')



# ==============================================================================
def arranque_dasolidar():
    if config_class.dl_mostrar_ventana_bienvenida:
        # Llama a la función para mostrar el diálogo
        mostrar_ventana_bienvenida()
    if config_class.dl_mostrar_message_bienvenida:
        # Muestra el messageBar de la parte superior del canvas
        mostrar_messagebar_bienvenida()

arranque_dasolidar()

QgsMessageLog.logMessage('Carga dasolidar ok', level=Qgis.Info)

if __name__ == '__main__':
    pass
