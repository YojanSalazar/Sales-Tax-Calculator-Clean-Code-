"""
Capa de Reglas de Negocio (Model).

Representa un producto con su tipo de impuesto dentro
de la Calculadora de Impuestos de Venta.
"""


class Producto:
    """
    Representa un producto con su configuración de impuesto.

    Atributos:
        nombre              (str)   : Identificador único del producto.
        tipo_impuesto       (str)   : 'IVA', 'INC', 'LICOR' o 'EXENTO'.
        porcentaje_impuesto (float) : Tasa decimal (ej. 0.19 para 19 %).
        grado_alcohol       (float) : Grados de alcohol; solo para licores.
        volumen_ml          (int)   : Volumen en ml; solo para licores.
    """

    TIPOS_VALIDOS = {"IVA", "INC", "LICOR", "EXENTO"}

    def __init__(
        self,
        nombre: str,
        tipo_impuesto: str,
        porcentaje_impuesto: float,
        grado_alcohol: float = 0.0,
        volumen_ml: int = 0,
    ):
        self.nombre = nombre
        self.tipo_impuesto = tipo_impuesto.upper()
        self.porcentaje_impuesto = porcentaje_impuesto
        self.grado_alcohol = grado_alcohol
        self.volumen_ml = volumen_ml

    def __repr__(self):
        return (
            f"Producto(nombre={self.nombre!r}, "
            f"tipo={self.tipo_impuesto!r}, "
            f"impuesto={self.porcentaje_impuesto})"
        )
