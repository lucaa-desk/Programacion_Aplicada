def _if(bool, func1, func2):
    func1() if bool else func2()


_if(True, lambda: print("True"), lambda: print("False"))  # Salida: "True"
_if(False, lambda: print("True"), lambda: print("False")) # Salida: "False"
