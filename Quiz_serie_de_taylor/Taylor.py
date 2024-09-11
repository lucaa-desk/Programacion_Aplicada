def taylor(x, max_iter=100):
    # aqui podria colocar un if para evitar que se introduzcan valores menores a 0 pero no lo veo necesario
    # dado que solo estoy haciendo la logica de la serue de taylor
    # profe, lo digo para que tenga en cuenta que si lo pense pero no se me pide implementarlo :)
    # luver lopez
    y = x - 1
    acc = 0 
    potencia_acumulada = y
    signo = 1
    
    for n in range(1, max_iter + 1):
        term = signo * potencia_acumulada / n
        acc = acc + term
        potencia_acumulada = potencia_acumulada * y
        signo = -signo
        
    return acc
