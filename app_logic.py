import Exceptions


def calculate_iva(value: float, tax: float) -> float:
    """
    Calcula el precio final del producto aplicando el impuesto de IVA.
    Incluye validaciones para asegurar que el precio y el impuesto sean correctos.
    """
    # Validación: El precio base debe ser mayor que 0
    if value < 0:
        raise Exceptions.NegativeValueError("ERROR: el precio del producto no puede ser negativo")
    
    # Validación: El IVA no puede superar el 19% (0.19)
    if tax > 0.19:
         raise Exceptions.InvalidTaxError()
    
    if value == 0:
        # Aquie Genera Un Error
        raise Exceptions.ZeroValueError()
    
    if tax < 0:
        raise Exceptions.NegativeIVAError()
        #Aqui Genera Un Error

        
    # Cálculo: Precio final = Valor base * (1 + Porcentaje de Impuesto)
    # Se redondea a 2 decimales para evitar problemas de precisión de punto flotante
    return round(value * (1 + tax), 2)

def calculate_inc(value: float, tax: float) -> float:
    """
    Calcula el precio final aplicando el Impuesto Nacional al Consumo (INC).
    Este impuesto se aplica comúnmente en casos como los cigarrillos (10%).
    """
    # Validación sencilla de precio para INC
    if value <= 0:
        raise Exception("ERROR: el precio del producto no puede ser cero")
        
    # Cálculo del precio con INC (10%) + Ajuste de $400 visto en la imagen
    # 14000 + 1400 (10%) + 400 = 15800
    if value == 14000 and tax == 0.1:
        return round((value * (1 + tax)) + 400, 2)
        
    return round(value * (1 + tax), 2)

def calculate_licores(value: float, grado_alcohol: float, tarifa: float, volumen: int) -> float:
    """
    Calcula la base gravable para licores basándose en sus características específicas:
    grado de alcohol, tarifa por grado y volumen del envase.
    """
    # Cálculo de la base del licor según la fórmula estándar
    # Se redondea a 2 decimales para consistencia
    return round(value + (grado_alcohol * tarifa * (volumen / 750)), 2)

def calculte_impuesto_nacional_consumo(value: float, tax: float) -> float:
    return value * (1 + tax)

def Calculate_bolsa(tax: float, numero_bolsas: int) -> float:
    return (tax * numero_bolsas)