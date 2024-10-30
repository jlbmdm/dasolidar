[![pypi](https://img.shields.io/pypi/v/cartolidar.svg)](https://pypi.org/project/cartolidar/)
[![py](https://img.shields.io/pypi/pyversions/cartolidar.svg)](https://pypi.org/project/cartolidar/)
[![Coverage Status](https://codecov.io/gh/cartolidar/cartolidar/branch/main/graph/badge.svg)](https://codecov.io/gh/cartolidar/cartolidar)
[![Join the chat at https://gitter.im/cartolidar/cartolidar](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cartolidar/cartolidar?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/cartolidar/cartolidar/main)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![cartolidar Logo](https://secure.gravatar.com/avatar/ea09c6d439dc57633702164f23b264e5 "clid image")


Dasoraster
----------

Documento en construcci�n

> Dasoraster es un complemento de Qgis desarrollado dentro del proyecto dasolidar

> Dasolidar y dasoraster se basan en datos Lidar del PNOA y parcelas de IFN4

Lidar PNOA: https://pnoa.ign.es/el-proyecto-pnoa-lidar

IFN4: https://www.miteco.gob.es/es/biodiversidad/temas/inventarios-nacionales/inventario-forestal-nacional/cuarto_inventario.html


------------
�Qu� es el dasoLidar?
Es una iniciativa para poner a disposici�n de los t�cnicos, productos y
herramientas Lidar destinados a la gesti�n del medio natural.

�Por d�nde empiezo?
Cargando el proyecto LidarQgis.

�D�nde est� el proyecto?
Se accede mediante un enlace directo que est� en el escritorio 

�Est� disponible para todos?
Est� disponible para los t�cnicos de la Junta de Castilla y Le�n que est�n en la lista de usuarios dasoLidar


Uso
----
�Qu� puedo hacer una vez abierto el proyecto?

1.	Se puede empezar cargando la nube de puntos Lidar y mostrando un perfil:
	�	Zoom a un sitio concreto
	�	Click en la capa �cargar_nubeDePuntos_LidarPNOA2� para activarla.
	�	Click en el bot�n de descarga
	�	Click sobre un punto del mapa
		? Eso carga una capa con los puntos Lidar
	�	Men� Ver -> Perfil de elevaci�n
		? Trazar una l�nea con el rat�n
		? Terminar la l�nea pulsando el bot�n derecho
	�	En el perfil se puede:
		? Hacer mediciones
		? Cambiar en ancho del perfil (tolerancia)
		? Desplazar el perfil transversalmente
		? etc.

2.	Se pueden visualizar capas r�ster con informaci�n dasom�trica
	como el volumen estimado de madera en pie o la altura dominante Lidar.
	Esas capas est�n dentro del grupo dasoLidar. 

�Qu� variables dasom�tricas puedo consultar?
	�	Se puede empezar por la altura dominante Lidar,
		Es una m�trica Lidar
	�	Se puede seguir con el Volumen estimado de madera en pie
		Es una variable dasom�trica estimada usando Lidar y datos de parcelas.

�Me puedo apoyar en esta informaci�n para planificar unas intervenciones selv�colas?
	�	Estas capas se pueden consultar visualmente
		Para eso hace falta saber:
		? Qu� significa cada variable dasom�trica o m�trica Lidar
		? En qu� unidades est�n expresadas
		  (altura: metros; volumen: m3/ha).
	�	Si se van a hacer c�lculos de existencias, crecimientos, etc.
		? Se puede usar la herramienta Qgis "Estad�sticas de zona"
		? Hay que tener en cuenta la precisi�n de cada m�trica o variable.
		? Es conveniente contrastar las estimaciones dasolidar
		  con datos de parcelas del monte o zona en cuesti�n
          Eso permite validar si el modelo usado funciona bien en ese entorno.

�Qu� es eso de la ubicaci�n de red; d�nde est� toda esta informaci�n?
	�	Es un espacio de almacenamiento que nos ha habilitado inform�tica para este proyecto,
	�	Es igual que cualquier otra unidad de red pero,
		por el momento, no le asignamos letra de unidad.

�Hay m�s documentaci�n adem�s de esta gu�a r�pida? 
	�	El ManualDasolidar.pdf est� en la ubicaci�n de red
	�	Se puede cargar desde Qgis.

________________________________________________________________________________
El directorio LidarData tiene todos los datos:
----

1.	En principio no ser� necesario bucear en LidarData,
	porque la idea es trabajarlo todo dentro Qgis.
    No obstante, se puede bucear en este directorio y ver donde est�n:
	�	Los ficheros con las nubes de puntos Lidar (lazFiles),
	�	Las capas dasoLidar (r�ster con m�tricas Lidar y variables dasom�tricas),
	�	Los proyectos de Qgis (hay m�s)
	�	Las mallas con enlaces directos a los lazFiles
	�	La documentaci�n
	�	La cocina y ficheros auxiliares de gesti�n del proyecto


Requerimientos
----
Trabajar dentro de la intranet de la Junta de Castilla y Le�n
Qgis
Python 3.9 o superior
Ver requerimientos del complemento dasoraster en requirements.txt.


to be continued...

<!-- This content will not appear in the rendered Markdown -->


[Ayuda Markdown de github](https://guides.github.com/features/mastering-markdown/)
[Ayuda Markdown de github](https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
[Ayuda Markdown de markdownguide](https://www.markdownguide.org/getting-started)


[![Actions Status](https://github.com/cartolidar/cartolidar/workflows/Tests/badge.svg)](https://github.com/cartolidar/cartolidar/actions?query=workflow%3ATests)
