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
    ## no pongo el a/2 como hizo el profe en clase (lo aclaro pa que no me baje profe :3)
    y = Apx +off_set
  else:
    y = (Apx * -1) +off_set
    
  return y