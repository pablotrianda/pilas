import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
ejes = pilas.actores.Ejes()
ejes.x = 100
ejes.y = 100

pilas.avisar("Ejes desplazados. Pulas F12 para ver los reales.")
pilas.ejecutar()
