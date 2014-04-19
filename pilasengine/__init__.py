# -*- encoding: utf-8 -*-
import sys
import os
import datetime

from pilasengine import escenas
from pilasengine import imagenes
from pilasengine import actores
from pilasengine import utils

import widget

PATH = os.path.dirname(os.path.abspath(__file__))
INTERPRETE_PATH = os.path.dirname(sys.argv[0])


class Pilas(object):
    """Representa el area de juego de pilas, el componente principal.

    El objeto pilas se inicializa cuando llamamos a la función
    ``pilasengine.iniciar()``. El objeto que se retorna es un
    objeto de esta clase.

    Internamente, este objeto será el que representa la ventana
    principal. Es es contenedor de la escena, el punto de contrucción
    de los actores y quien mantiene con "vida" el juego completo.
    """

    def __init__(self, ancho=640, alto=480, titulo='pilas-engine'):
        self.log("Iniciando pilas con una ventana de ", ancho, "x", alto)
        self.actores = actores.Actores(self)
        self.escenas = escenas.Escenas(self)
        self.imagenes = imagenes.Imagenes(self)
        self.escenas.Normal()
        self.widget = widget.Widget(self, ancho, alto)
        self.utils = utils.Utils(self)

    def obtener_widget(self):
        return self.widget

    def obtener_centro_fisico(self):
        """Retorna el centro de la ventana en pixels."""
        return self.widget.obtener_centro_fisico()

    def obtener_escena_actual(self):
        return self.escenas.obtener_escena_actual()

    def realizar_actualizacion_logica(self):
        self.escenas.realizar_actualizacion_logica()

    def realizar_dibujado(self, painter):
        self.escenas.realizar_dibujado(painter)

    def log(self, *mensaje):
        "Muestra un mensaje de prueba sobre la consola."
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        mensaje = map(lambda x: str(x), mensaje)
        print(":: %s :: %s " %(hora, " ".join(mensaje)))

    def obtener_ruta_al_recurso(self, ruta):
        """Busca la ruta a un archivo de recursos.

        Los archivos de recursos (como las imagenes) se buscan en varios
        directorios (ver docstring de image.load), así que esta
        función intentará dar con el archivo en cuestión.

        :param ruta: Ruta al archivo (recurso) a inspeccionar.
        """
        self.log("Buscando ruta al recurso:", ruta)

        dirs = ['./', '/../data', 'data',
                PATH, INTERPRETE_PATH,
                PATH + '/data', INTERPRETE_PATH + '/data',
                PATH + '/../data', INTERPRETE_PATH + '/../data'
               ]

        for x in dirs:
            full_path = os.path.join(x, ruta)

            if os.path.exists(full_path):
                return full_path

        # Si no ha encontrado el archivo lo reporta.
        raise IOError("El archivo '%s' no existe." % (ruta))

def iniciar(ancho=640, alto=480, titulo='Pilas'):
    """
    Inicia la ventana principal del juego con algunos detalles de funcionamiento.

    Ejemplo de invocación:

        >>> pilas.iniciar(ancho=320, alto=240)

    .. image:: images/iniciar_320_240.png

    Parámetros:

    :ancho: el tamaño en pixels para la ventana.
    :alto: el tamaño en pixels para la ventana.
    :titulo: el titulo a mostrar en la ventana.
    """
    pilas = Pilas(ancho=ancho, alto=alto, titulo=titulo)
    return pilas