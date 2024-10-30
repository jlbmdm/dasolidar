[![pypi](https://img.shields.io/pypi/v/cartolidar.svg)](https://pypi.org/project/cartolidar/)
[![py](https://img.shields.io/pypi/pyversions/cartolidar.svg)](https://pypi.org/project/cartolidar/)
[![Coverage Status](https://codecov.io/gh/cartolidar/cartolidar/branch/main/graph/badge.svg)](https://codecov.io/gh/cartolidar/cartolidar)
[![Join the chat at https://gitter.im/cartolidar/cartolidar](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cartolidar/cartolidar?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/cartolidar/cartolidar/main)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![cartolidar Logo](https://secure.gravatar.com/avatar/ea09c6d439dc57633702164f23b264e5 "clid image")


Dasoraster
----------

Documento en construcción

> Dasoraster es un complemento de Qgis desarrollado dentro del proyecto dasolidar

> Dasolidar y dasoraster se basan en datos Lidar del PNOA y parcelas de IFN4

Lidar PNOA: https://pnoa.ign.es/el-proyecto-pnoa-lidar

IFN4: https://www.miteco.gob.es/es/biodiversidad/temas/inventarios-nacionales/inventario-forestal-nacional/cuarto_inventario.html


------------
¿Qué es el dasoLidar?
Es una iniciativa para poner a disposición de los técnicos, productos y
herramientas Lidar destinados a la gestión del medio natural.

¿Por dónde empiezo?
Cargando el proyecto LidarQgis.

¿Dónde está el proyecto?
Se accede mediante un enlace directo que está en el escritorio 

¿Está disponible para todos?
Está disponible para los técnicos de la Junta de Castilla y León que están en la lista de usuarios dasoLidar


Uso
----
¿Qué puedo hacer una vez abierto el proyecto?

1.	Se puede empezar cargando la nube de puntos Lidar y mostrando un perfil:
	•	Zoom a un sitio concreto
	•	Click en la capa “cargar_nubeDePuntos_LidarPNOA2” para activarla.
	•	Click en el botón de descarga
	•	Click sobre un punto del mapa
		? Eso carga una capa con los puntos Lidar
	•	Menú Ver -> Perfil de elevación
		? Trazar una línea con el ratón
		? Terminar la línea pulsando el botón derecho
	•	En el perfil se puede:
		? Hacer mediciones
		? Cambiar en ancho del perfil (tolerancia)
		? Desplazar el perfil transversalmente
		? etc.

2.	Se pueden visualizar capas ráster con información dasométrica
	como el volumen estimado de madera en pie o la altura dominante Lidar.
	Esas capas están dentro del grupo dasoLidar. 

¿Qué variables dasométricas puedo consultar?
	•	Se puede empezar por la altura dominante Lidar,
		Es una métrica Lidar
	•	Se puede seguir con el Volumen estimado de madera en pie
		Es una variable dasométrica estimada usando Lidar y datos de parcelas.

¿Me puedo apoyar en esta información para planificar unas intervenciones selvícolas?
	•	Estas capas se pueden consultar visualmente
		Para eso hace falta saber:
		? Qué significa cada variable dasométrica o métrica Lidar
		? En qué unidades están expresadas
		  (altura: metros; volumen: m3/ha).
	•	Si se van a hacer cálculos de existencias, crecimientos, etc.
		? Se puede usar la herramienta Qgis "Estadísticas de zona"
		? Hay que tener en cuenta la precisión de cada métrica o variable.
		? Es conveniente contrastar las estimaciones dasolidar
		  con datos de parcelas del monte o zona en cuestión
          Eso permite validar si el modelo usado funciona bien en ese entorno.

¿Qué es eso de la ubicación de red; dónde está toda esta información?
	•	Es un espacio de almacenamiento que nos ha habilitado informática para este proyecto,
	•	Es igual que cualquier otra unidad de red pero,
		por el momento, no le asignamos letra de unidad.

¿Hay más documentación además de esta guía rápida? 
	•	El ManualDasolidar.pdf está en la ubicación de red
	•	Se puede cargar desde Qgis.

________________________________________________________________________________
El directorio LidarData tiene todos los datos:
----

1.	En principio no será necesario bucear en LidarData,
	porque la idea es trabajarlo todo dentro Qgis.
    No obstante, se puede bucear en este directorio y ver donde están:
	•	Los ficheros con las nubes de puntos Lidar (lazFiles),
	•	Las capas dasoLidar (ráster con métricas Lidar y variables dasométricas),
	•	Los proyectos de Qgis (hay más)
	•	Las mallas con enlaces directos a los lazFiles
	•	La documentación
	•	La cocina y ficheros auxiliares de gestión del proyecto


Requerimientos
----
Trabajar dentro de la intranet de la Junta de Castilla y León
Qgis
Python 3.9 o superior
Ver requerimientos del complemento dasoraster en requirements.txt.


to be continued...

<!-- This content will not appear in the rendered Markdown -->


[Ayuda Markdown de github](https://guides.github.com/features/mastering-markdown/)
[Ayuda Markdown de github](https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
[Ayuda Markdown de markdownguide](https://www.markdownguide.org/getting-started)


[![Actions Status](https://github.com/cartolidar/cartolidar/workflows/Tests/badge.svg)](https://github.com/cartolidar/cartolidar/actions?query=workflow%3ATests)
