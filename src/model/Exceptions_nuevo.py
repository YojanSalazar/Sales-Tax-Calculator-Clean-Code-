"""Excepciones personalizadas para la Calculadora de Impuestos de Venta."""


class ErrorCalculoImpuesto(Exception):
    """Base para todos los errores de la aplicación."""

    def __str__(self):
        return f"Error: {self.message}"


class ErrorValorNegativoOCero(ErrorCalculoImpuesto):
    """El precio del producto no puede ser negativo ni cero."""

    def __init__(self, message="El precio del producto no puede ser negativo ni cero"):
        self.message = message
        super().__init__(self.message)


class ErrorImpuestoInvalido(ErrorCalculoImpuesto):
    """El porcentaje de IVA supera el máximo permitido (19 %)."""

    def __init__(self, message="El impuesto de IVA no puede superar el 19 %"):
        self.message = message
        super().__init__(self.message)


class ErrorIVANegativo(ErrorCalculoImpuesto):
    """El porcentaje de IVA no puede ser negativo."""

    def __init__(self, message="El impuesto de IVA no puede ser negativo"):
        self.message = message
        super().__init__(self.message)


class ErrorParametrosLicores(ErrorCalculoImpuesto):
    """Parámetros inválidos para el cálculo de licores."""

    def __init__(self, message="Parámetros de licores inválidos"):
        self.message = message
        super().__init__(self.message)


class ErrorParametrosBolsas(ErrorCalculoImpuesto):
    """El número de bolsas no puede ser negativo."""

    def __init__(self, message="El número de bolsas debe ser mayor o igual a cero"):
        self.message = message
        super().__init__(self.message)


class ErrorOpcionInvalida(ErrorCalculoImpuesto):
    """Opción de menú no reconocida."""

    def __init__(self, message="Opción no válida. Seleccione una opción del menú"):
        self.message = message
        super().__init__(self.message)


class ErrorProductoNoEncontrado(ErrorCalculoImpuesto):
    """El producto buscado no existe en la base de datos."""

    def __init__(self, nombre: str = ""):
        self.message = f"Producto no encontrado: '{nombre}'"
        super().__init__(self.message)


class ErrorProductoYaExiste(ErrorCalculoImpuesto):
    """Se intenta insertar un producto cuyo nombre ya está registrado."""

    def __init__(self, nombre: str = ""):
        self.message = f"Ya existe un producto con el nombre: '{nombre}'"
        super().__init__(self.message)
