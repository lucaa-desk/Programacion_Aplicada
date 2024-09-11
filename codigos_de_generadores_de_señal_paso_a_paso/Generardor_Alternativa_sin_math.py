##funcion para hacer lo que casi hace la libreria de math por si no se puede usar math
def NoCoseno(x):
  ##voy a usar la serie de taylor que creo es lo mas cercano a la realdidad
  xCuadrada = x*x
  return (1-(xCuadrada/2)+(xCuadrada*xCuadrada/24))


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
    pi = 3.1416
    Conversor = 2*pi*(ppx/Fpx)
    y = Apx * NoCoseno(Conversor) + Off_set
    
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

##la diferencia es muy pequeña en la respuesta de coseno :)