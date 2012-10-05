# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

from pilas import actores, camara, colisiones, control, escenas, eventos, fisica, \
    tareas
from pilas.escena import gestor, escena_normal
import pytweener



class Mundo(object):
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.
    """

    def __init__(self, motor, ancho, alto, titulo, fps=60, gravedad=(0, -10), pantalla_completa=False):
        self.gestor_escenas = gestor.Gestor()

        self.motor = motor
        self.motor.iniciar_ventana(ancho, alto, titulo, pantalla_completa, self.gestor_escenas)

        self.gravedad = gravedad
        self.control = control.Control()

    def crear_motor_fisica(self):
        return fisica.crear_motor_fisica(self.motor.obtener_area(), gravedad=self.gravedad)

    def reiniciar(self):
        self.gestor_escenas.limpiar()
        self.gestor_escenas.cambiar_escena(escena_normal.EscenaNormal())

    def terminar(self):
        self.motor.terminar()

    def ejecutar_bucle_principal(self, ignorar_errores=False):
        "Mantiene en funcionamiento el motor completo."
        self.motor.ejecutar_bucle_principal(self, ignorar_errores)

    def agregar_tarea_una_vez(self, time_out, function, *params):
        return self.gestor_escenas.escena_actual().tareas.una_vez(time_out, function, params)

    def agregar_tarea_siempre(self, time_out, function, *params):
        return self.gestor_escenas.escena_actual().tareas.siempre(time_out, function, params)

    def agregar_tarea(self, time_out, funcion, *parametros):
        return self.gestor_escenas.escena_actual().tareas.condicional(time_out, funcion, parametros)

    def deshabilitar_sonido(self, estado=True):
        self.motor.deshabilitar_sonido(estado)

    def deshabilitar_musica(self, estado=True):
        self.motor.deshabilitar_musica(estado)

    def get_tareas_deprecated(self):
        print "CUIDADO: Acceder al atributo 'tareas' esta desaconsejado."
        print "\t utilice en su lugar: pilas.utils.agregar_tarea, agregar_tarea_una_vez o agregar_tarea_siempre"
        return self.gestor_escenas.escena_actual().tareas

    def get_camara_deprecated(self):
        print "CUIDADO: Acceder al atributo 'camara' esta desaconsejado."
        print "\t utilice en su lugar: pilas.escena_actual().camara"
        return self.gestor_escenas.escena_actual().camara

    tareas = property(get_tareas_deprecated)
    camara = property(get_camara_deprecated)
