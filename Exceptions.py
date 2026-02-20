class TaxCalculationError(Exception):
    """Excepción personalizada para errores en el cálculo de impuestos."""
    pass

class NegativeValueError(TaxCalculationError):
    """Excepción para valores negativos en el cálculo de impuestos."""
    def __init__(self, message="ERROR: el precio del producto no puede ser negativo"):
        self.message = message
        super().__init__(self.message)
