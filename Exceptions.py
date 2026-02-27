class TaxCalculationError(Exception):
    """Excepción personalizada para errores en el cálculo de impuestos."""
    pass


    def __str__(self):
        return f'Error: {self.message}'
    
class NegativeValueError(TaxCalculationError):
    """Excepción para valores negativos en el cálculo de impuestos."""
    def __init__(self, message="ERROR: el precio del producto no puede ser negativo"):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f'Error: {self.message}'
    


class InvalidTaxError(TaxCalculationError):
    """Excepción para tasas de impuestos no válidas."""
    def __init__(self, message="ERROR: el impuesto de IVA no puede superar el 19%"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'


class ZeroValueError(TaxCalculationError):
    """Excepción para valores de precio igual a cero."""
    def __init__(self, message="ERROR: el precio del producto no puede ser cero"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'

class InvalidOptionError(TaxCalculationError):
    """Excepción para opciones de menú no válidas."""
    def __init__(self, message="Opción no válida. Por favor, seleccione una opción del menú."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'