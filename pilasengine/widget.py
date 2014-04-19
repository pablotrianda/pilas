# -*- encoding: utf-8 -*-
import sys
from PyQt4 import QtGui

import fps

class Widget(QtGui.QWidget):
    """Representa el componente que contiene toda la escena de pilas.

    Este widget puede contenerse dentro de una ventana de PyQt, o
    dentro de un maquetado mas complejo, como la ventana del intérprete
    o un editor.
    """

    def __init__(self, pilas, ancho, alto):
        self.pilas = pilas
        super(Widget, self).__init__()
        self.setMinimumSize(200, 200)
        self.iniciar_interface(ancho, alto)

    def iniciar_interface(self, ancho, alto):
        self.painter = QtGui.QPainter()
        self.setMouseTracking(True)
        self.mouse_x = 0
        self.mouse_y = 0

        self.original_width = ancho
        self.original_height = alto
        self.escala = 1

        self.fps = fps.FPS(60)                   # 60 Cuadros por segundo.
        self.startTimer(1000/100.0)

    def obtener_centro_fisico(self):
        """Retorna el centro de la ventana en pixels."""
        return (self.original_width/2, self.original_height/2)

    def _realizar_actualizacion_logica(self):
        for _ in range(self.fps.actualizar()):
            self.pilas.realizar_actualizacion_logica()

    def procesar_error(self, e):
        print "Error:", e, "en", __file__
        sys.exit(1)

    def timerEvent(self, event):
        """Actualiza la simulación completa.

        Este método se llama automáticamente 100 veces por segundo, ya
        que se hace una llamada a 'startTimer' indicando esa frecuencia.
        """
        try:
            self._realizar_actualizacion_logica()
        except Exception, e:
            self.procesar_error(e)

        # Pide redibujar el widget (Qt llamará a paintEvent después).
        self.update()


    def _pintar_fondo(self):
        self.painter.setBrush(QtGui.QColor(200, 200, 200))
        size = self.size()
        w = size.width()
        h = size.height()
        self.painter.drawRect(0, 0, w - 1, h - 1)

    def paintEvent(self, e):
        self.painter.begin(self)
        self._pintar_fondo()
        self._dibujar_widget()
        self.painter.end()

    def resizeEvent(self, event):
        self._ajustar_canvas(self.width(), self.height())

    def _ajustar_canvas(self, w, h):
        escala_x = w / float(self.original_width)
        escala_y = h / float(self.original_height)
        escala = min(escala_x, escala_y)

        final_w = self.original_width * escala
        final_h = self.original_height * escala
        self.escala = escala

        x = w - final_w
        y = h - final_h

        self.setGeometry(x/2, y/2, final_w, final_h)
        self._centrar_canvas(w, h)

    def _centrar_canvas(self, w, h):
        dw = w - self.frameGeometry().width()
        dh = h - self.frameGeometry().height()
        self.move(dw / 2, dh / 2)

    def _dibujar_widget(self):
        self.painter.scale(self.escala, self.escala)

        # Suavizar efectos y transformaciones de imágenes.
        self.painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        self.pilas.realizar_dibujado(self.painter)