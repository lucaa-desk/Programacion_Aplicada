##la ecuacion que encontre para pasar de amplitud a pixeles verticales es = (-6.4x+64)
## y para frecuencia a pixeles horizontales es = (-5.17x)+517.7


def Generador(f, a, x):
  Apx = (-6.4 * x) + 64
  Fpx = (-5.17 * x) + 517.7
  ppx = x % Fpx
  if ppx < Fpx / 2:
    y = Apx
  else:
    y = Apx * -1
  return y

## aqui pido datos por teclado para probar la funcion
f = float(input("Ingrese la frecuencia de la señal: "))
a = float(input("Ingrese la amplitud de la señal: "))
x = float(input("Ingrese el valor de x: "))

print("y")


## basicamente la funcion traduce una pareja de pixeles en una pareja de valores de la funcion y luego usa ppx para (segun el periodo) determinar si la ampltud va+
## arriba o abajo, ya que pues es una señal cuadrada, si la frecuencia es menor a la mitad, la amplitud va arriba, si no , abajo
## el primer codigo es este, en otro archivo agrego el off_Set
##subo los codigos paso por paso para demostrar todo el proceso :)