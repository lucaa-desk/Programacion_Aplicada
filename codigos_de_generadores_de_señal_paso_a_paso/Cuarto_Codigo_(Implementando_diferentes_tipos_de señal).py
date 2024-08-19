import math

def Generador_final(f, a, x,Off_set,Duty_cycle,Tipo_Onda):
  ##pongo mis lidas ecuaciones porque son para mapear la pantalla o sea de valor a pixel
  ##en teoria todas las señales usan esas ecuaciones solo cambiando la pendiente de los ciclos
  Apx = (-6.4*x)+64
  Fpx = (-5.17*x)+517.17
  ppx = x%Fpx
  if Tipo_Onda == "cuadrada"