def Generador(f, a, x,Off_set):
  Apx = (-6.4 * x) + 64
  Fpx = (-5.17 * x) + 517.7
  ppx = x % Fpx
  if ppx < Fpx / 2:
    y = Apx
  else:
    y = Apx * -1
  return y + Off_set
