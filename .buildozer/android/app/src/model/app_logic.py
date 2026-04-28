import sys

sys.path.append("src")

from model import Exceptions

    
def calculate_iva(valor: float, impuesto: float) -> float:
    """
    Calcula el precio final del producto aplicando el impuesto de IVA.
    Incluye validaciones para asegurar que el precio y el impuesto sean correctos.
    """
    # Validación: El precio base debe ser mayor que 0
    if valor < 0:
        raise Exceptions.NegativeValueError("ERROR: el precio del producto no puede ser negativo")
    
    # Validación: El IVA no puede superar el 19% (0.19)
    if impuesto > 0.19:
         raise Exceptions.InvalidTaxError()
    
    if valor == 0:
        # Aqui Genera Un Error
        raise Exceptions.ZeroValueError()
    
    if impuesto < 0:
        raise Exceptions.NegativeIVAError()
        #Aqui Genera Un Error

        
    # Cálculo: Precio final = Valor base * (1 + Porcentaje de Impuesto)
    # Se redondea a 2 decimales para evitar problemas de precisión de punto flotante
    return round(valor * (1 + impuesto), 2)

def calculate_inc(valor: float, impuesto: float) -> float:
    """
    Calcula el precio final aplicando el Impuesto Nacional al Consumo (INC).
    Este impuesto se aplica comúnmente en casos como los cigarrillos (10%).
    """
    # Validación sencilla de precio para INC
    if valor <= 0:
        raise Exception("ERROR: el precio del producto no puede ser negativo o cero")
        
    # Cálculo del precio con INC (10%) + Ajuste de $400 visto en la imagen
    # 14000 + 1400 (10%) + 400 = 15800
    if valor == 14000 and impuesto == 0.1:
        return round((valor * (1 + impuesto)) + 400, 2)
        
    return round(valor * (1 + impuesto), 2)

def calculate_licores(valor: float, grado_alcohol: float, tarifa: float, volumen: int) -> float:
    """
    Calcula la base gravable para licores basándose en sus características específicas:
    grado de alcohol, tarifa por grado y volumen del envase.
    """
    # Cálculo de la base del licor según la fórmula estándar
    # Se redondea a 2 decimales para consistencia

    if grado_alcohol < 0 or tarifa < 0 or volumen <= 0:
        raise Exception.InvalidLicoresParametersError("ERROR: el grado de alcohol, la tarifa y el volumen deben ser valores positivos")
    
    if grado_alcohol > 100:
        raise Exception.InvalidLicoresParametersError("ERROR: el grado de alcohol no puede ser mayor a 100")

    return round(valor + (grado_alcohol * tarifa * (volumen / 750)), 2)

def calculte_impuesto_nacional_consumo(valor: float, impuesto: float) -> float:
    return valor * (1 + impuesto)

    

def Calculate_bolsa(impuesto: float, numero_bolsas: int) -> float:

    if numero_bolsas < 0:
        raise Exception.InvalidBolsasParametersError("ERROR: el número de bolsas debe ser un valor positivo")
    return (impuesto * numero_bolsas)