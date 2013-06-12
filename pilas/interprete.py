# -*- coding: utf-8 -*-
import sys

try:
    from PyQt4 import QtCore, QtGui
    from interprete_base import Ui_InterpreteDialog
except:
    print "ERROR: No se encuentra pyqt"
    Ui_InterpreteDialog = object
    pass

import pilas
import utils

try:
    sys.path.append(utils.obtener_ruta_al_recurso('../lanas'))
except IOError, e:
    pass

try:
    import lanas
except ImportError, e:
    print e


import os

if os.environ.has_key('lanas'):
    del os.environ['lanas']

class VentanaInterprete(Ui_InterpreteDialog):

    def setupUi(self, main):
        self.main = main
        Ui_InterpreteDialog.setupUi(self, main)
        scope = self._insertar_ventana_principal_de_pilas()
        self._insertar_consola_interactiva(scope)
        pilas.utils.centrar_ventana(main)


        # F7 Modo informacion de sistema
        self.definir_icono(self.pushButton_6, 'iconos/f07.png')
        self.pushButton_6.connect(self.pushButton_6, QtCore.SIGNAL("clicked()"), self.cambia_boton_f7)

        # F8 Modo puntos de control
        self.definir_icono(self.pushButton_5, 'iconos/f08.png')
        self.pushButton_5.connect(self.pushButton_5, QtCore.SIGNAL("clicked()"), self.cambia_boton_f8)

        # F9 Modo radios de colision
        self.definir_icono(self.pushButton_4, 'iconos/f09.png')
        self.pushButton_4.connect(self.pushButton_4, QtCore.SIGNAL("clicked()"), self.cambia_boton_f9)

        # F10 Modo areas de colision
        self.definir_icono(self.pushButton_3, 'iconos/f10.png')
        self.pushButton_3.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.cambia_boton_f10)

        # F11 Modo fisica
        self.definir_icono(self.pushButton_2, 'iconos/f11.png')
        self.pushButton_2.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.cambia_boton_f11)

        # F12 Modo depuracion de posicion
        self.definir_icono(self.pushButton, 'iconos/f12.png')
        self.pushButton.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.cambia_boton_f12)

    def definir_icono(self, boton, ruta):
        icon = QtGui.QIcon();
        icon.addFile(pilas.utils.obtener_ruta_al_recurso(ruta), QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        boton.setIcon(icon)
        boton.setText('')

    def cambia_boton_f7(self):
        status = self.pushButton_6.isChecked()
        pilas.atajos.definir_modos(info=status)

    def cambia_boton_f8(self):
        status = self.pushButton_5.isChecked()
        pilas.atajos.definir_modos(puntos_de_control=status)

    def cambia_boton_f9(self):
        status = self.pushButton_4.isChecked()
        pilas.atajos.definir_modos(radios=status)

    def cambia_boton_f10(self):
        status = self.pushButton_3.isChecked()
        pilas.atajos.definir_modos(areas=status)

    def cambia_boton_f11(self):
        status = self.pushButton_2.isChecked()
        pilas.atajos.definir_modos(fisica=status)

    def cambia_boton_f12(self):
        status = self.pushButton.isChecked()
        pilas.atajos.definir_modos(posiciones=status)

    def raw_input(self, mensaje):
        text, state = QtGui.QInputDialog.getText(self, "raw_input", mensaje)
        return str(text)

    def input(self, mensaje):
        text, state = QtGui.QInputDialog.getText(self, "raw_input", mensaje)
        return eval(str(text))

    def _insertar_ventana_principal_de_pilas(self):
        pilas.iniciar(usar_motor='qtsugar', ancho=640, alto=400)

        mono = pilas.actores.Mono()

        ventana = pilas.mundo.motor.ventana
        canvas = pilas.mundo.motor.canvas
        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()

        self.canvas.addWidget(ventana)
        self.canvas.setCurrentWidget(ventana)
        return {'pilas': pilas, 'mono': mono, 'self': self}

    def _insertar_consola_interactiva(self, scope):
        codigo_inicial = [
                'import pilas',
                '',
                'pilas.iniciar()',
                'mono = pilas.actores.Mono()',
                ]

        consola = lanas.interprete.Ventana(self.splitter, scope, "\n".join(codigo_inicial))
        self.console.addWidget(consola)
        self.console.setCurrentWidget(consola)

def main(parent=None, do_raise=False):
    dialog = QtGui.QDialog(parent)
    dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
    ui = VentanaInterprete()
    ui.setupUi(dialog)

    if do_raise:
        dialog.show()
        dialog.raise_()

    dialog.exec_()
