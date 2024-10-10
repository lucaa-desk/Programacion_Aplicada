def count_sheep(sheep):
    return sum(1 for s in sheep if s == True)

sheep = [True,  True,  True,  False,
         True,  True,  True,  True,
         True,  False, True,  False,
         True,  False, False, True,
         True,  True,  True,  True,
         False, False, True,  True]

print(count_sheep(sheep))
