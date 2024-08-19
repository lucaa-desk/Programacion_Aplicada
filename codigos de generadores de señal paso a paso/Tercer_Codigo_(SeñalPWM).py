def generador_PWM(f,a,x,off_set,Duty_cycle):
  ##las ecuaciones que encontre desde antes
  Apx = (-6.4 * x) + 64
  Fpx = (-5.17 * x) + 517.7
  ppx = x % Fpx
  ##esto si es nuevo y es para tener en cuenta el ciclo util por eso es PWM
  Limite_Ciclo = Fpx * (Duty_cycle/100)
  ##ahora es iff para que el programa sepa si el ciclo va arriba o abajo
  if ppx < Limite_Ciclo:
    y = Apx +off_set
  else:
    y = (Apx * -1) +off_set
    
  return y