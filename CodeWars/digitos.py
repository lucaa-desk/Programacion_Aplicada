def digitize(n):
    return [int(digit) for digit in str(n)][::-1]

n = 35231
print(digitize(n))  # Salida: [1, 3, 2, 5, 3]
