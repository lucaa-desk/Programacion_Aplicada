## esto es el mismo "Primer Codigo" pero agregando la variable Off set que reposiciona la onda un poco mas arriba o abajo segun quiera el usuario 

def Generador(f, a, x,Off_set):
  Apx = (-6.4 * x) + 64
  Fpx = (-5.17 * x) + 517.7
  ppx = x % Fpx
  if ppx < Fpx / 2:
    y = Apx
  else:
    y = Apx * -1
  return y + Off_set

## aqui pido datos por teclado para probar la funcion
f = float(input("Ingrese la frecuencia de la señal: "))
a = float(input("Ingrese la amplitud de la señal: "))
x = float(input("Ingrese el valor de x: "))
Off_set = float(input("Ingrese el valor del off set: "))

punto = Generador(f, a, x,Off_set)

## probado, si da un punto :)

print(punto)
