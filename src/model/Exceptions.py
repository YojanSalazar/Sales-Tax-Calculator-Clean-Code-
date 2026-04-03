class ErrorCalculoImpuesto(Exception):
    """Excepción personalizada para errores en el cálculo de impuestos."""
    def __str__(self):
        return f'Error: {self.message}'
    
class ErrorValorNegativoOCero(ErrorCalculoImpuesto):
    """Excepción para valores negativos o cero en el cálculo de impuestos."""
    def __init__(self, message="ERROR: el precio del producto no puede ser negativo ni cero"):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f'Error: {self.message}'
    


class ErrorImpuestoInvalido(ErrorCalculoImpuesto):
    """Excepción para tasas de impuestos no válidas."""
    def __init__(self, message="ERROR: el impuesto de IVA no puede superar el 19%"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'


    def __str__(self):
        return f'Error: {self.message}'

class ErrorOpcionInvalida(ErrorCalculoImpuesto):
    """Excepción para opciones de menú no válidas."""
    def __init__(self, message="Opción no válida. Por favor, seleccione una opción del menú."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'

class ErrorIVANegativo(ErrorCalculoImpuesto):
    """Excepción para tasas de IVA negativas."""
    def __init__(self, message="ERROR: el impuesto de IVA no puede ser negativo"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'

class ErrorParametrosLicores(ErrorCalculoImpuesto):
    def __init__(self, message="ERROR: parámetros de licores inválidos"):
        self.message = message
        super().__init__(self.message)

class ErrorParametrosBolsas(ErrorCalculoImpuesto):
    def __init__(self, message="ERROR: el número de bolsas debe ser positivo"):
        self.message = message
        super().__init__(self.message)