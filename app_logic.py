def calculate_iva(value: float, tax: float) -> float:
    return value * (1 + tax)

def calculate_licores(value: float, grado_alcohol: float, tarifa: float, volumen: int) -> float:
    return value + (grado_alcohol * tarifa * (volumen / 750))

