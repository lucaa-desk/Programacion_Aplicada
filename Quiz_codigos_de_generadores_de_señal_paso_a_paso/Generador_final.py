import math

def Generador_final(f, a, x,Off_set,Duty_cycle,Tipo_Onda):
  ##pongo mis lidas ecuaciones porque son para mapear la pantalla o sea de valor a   pixel
  ##en teoria todas las señales usan esas ecuaciones solo cambiando la pendiente     de los    ciclos
  Apx = (-6.4*x)+64
  Fpx = (-5.17*x)+517.17
  
  ppx = x%Fpx
  
  if Tipo_Onda == "cuadrada":
    
    if ppx < Fpx/2:
      y = Apx + Off_set
    else:
      y = (Apx*-1) + Off_set
    
  elif Tipo_Onda == "PWM":
    
    Limite_Ciclo = Fpx*(Duty_cycle/100)
    if ppx < Limite_Ciclo:
      y = Apx + Off_set
    else:
      y = (Apx*-1) +Off_set
      
  elif Tipo_Onda == "triangular":
    
    if ppx < Fpx/2:
      y = ((Apx/(Fpx/2))*ppx) + Off_set 
    else:
      y = (-Apx + (Apx/(Fpx/2))*(ppx-Fpx/2)) + Off_set
    
  elif Tipo_Onda == "sierra":
    y = ((Apx == Fpx)*ppx) + Off_set
    if ppx == Fpx:
      y = ((Apx * -1)) + Off_set
      
  elif Tipo_Onda == "cosenoidal":
    y = (Apx * math.cos(2*math.pi*(ppx/Fpx))) + Off_set

  
  return y
## aqui pido datos por teclado para probar la funcion
f = float(input("Ingrese la frecuencia de la señal: "))
a = float(input("Ingrese la amplitud de la señal: "))
x = float(input("Ingrese el valor de x: "))
Off_set = float(input("Ingrese el valor del off set: "))
Duty_cycle = float(input("Ingrese el valor del Duty Cycle: "))
Tipo_Onda = input("Ingrese el tipo de onda: ")

punto = Generador_final(f, a, x,Off_set,Duty_cycle,Tipo_Onda)

print(punto)