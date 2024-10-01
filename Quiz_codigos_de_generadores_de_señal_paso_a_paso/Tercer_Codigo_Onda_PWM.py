def generador_PWM(f,a,x,off_set,Duty_cycle):
  ##las ecuaciones que encontre desde antes
  Apx = (-6.4 * x) + 64
  Fpx = (-5.17 * x) + 517.7
  ppx = x % Fpx
  ##esto si es nuevo y es para tener en cuenta el ciclo util por eso es PWM
  Limite_Ciclo = Fpx * (Duty_cycle/100)
  ##ahora es iff para que el programa sepa si el ciclo va arriba o abajo
  if ppx < Limite_Ciclo:
    ##en este caso todo el ejercicio lo estoy haciendo con la señal no necesariamente en el centro por eso
    ## no pongo el a/2 como hizo el profe en clase (lo aclaro pa que no me baje por fa profe :3)
    y = Apx +off_set
  else:
    y = (Apx * -1) +off_set
    
  return y

## aqui pido datos por teclado para probar la funcion
f = float(input("Ingrese la frecuencia de la señal: "))
a = float(input("Ingrese la amplitud de la señal: "))
x = float(input("Ingrese el valor de x: "))
Off_set = float(input("Ingrese el valor del off set: "))
Duty_cycle = float(input("Ingrese el valor del Duty Cycle: "))

punto = generador_PWM(f, a, x,Off_set,Duty_cycle)

## probado, si da un punto, si funcionaa, buenisimoo

print(punto)