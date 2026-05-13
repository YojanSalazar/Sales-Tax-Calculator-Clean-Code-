"""Lógica de negocio para el cálculo de impuestos de venta."""

import sys
sys.path.append("src")

from model.Exceptions_nuevo import (
    ErrorValorNegativoOCero,
    ErrorImpuestoInvalido,
    ErrorIVANegativo,
    ErrorParametrosLicores,
    ErrorParametrosBolsas,
)

TARIFA_BOLSA = 75
TARIFA_LICORES = 342


def calcular_iva(valor: float, impuesto: float) -> float:
    """
    Calcula el precio final aplicando IVA.

    Validaciones:
        - valor > 0
        - 0 <= impuesto <= 0.19
    """
    if valor <= 0:
        raise ErrorValorNegativoOCero()
    if impuesto < 0:
        raise ErrorIVANegativo()
    if impuesto > 0.19:
        raise ErrorImpuestoInvalido()

    return round(valor * (1 + impuesto), 2)


def calcular_impuesto_nacional_consumo(valor: float, impuesto: float) -> float:
    """
    Calcula el precio final aplicando el Impuesto Nacional al Consumo (INC).
    Se usa principalmente para cigarrillos (10 %).
    """
    if valor <= 0:
        raise ErrorValorNegativoOCero()

    return round(valor * (1 + impuesto), 2)


def calcular_licores(valor: float, grado_alcohol: float, tarifa: float, volumen: int) -> float:
    """
    Calcula la base gravable para licores.

    Fórmula: valor_base + (grado × tarifa × volumen / 750)
    """
    if grado_alcohol < 0 or tarifa < 0 or volumen <= 0:
        raise ErrorParametrosLicores()
    if grado_alcohol > 100:
        raise ErrorParametrosLicores()

    return round(valor + (grado_alcohol * tarifa * (volumen / 750)), 2)


def calcular_bolsa(numero_bolsas: int, tarifa: float = TARIFA_BOLSA) -> float:
    """Calcula el costo total por bolsas plásticas."""
    if numero_bolsas < 0:
        raise ErrorParametrosBolsas()

    return round(tarifa * numero_bolsas, 2)


def calcular_precio_final(valor: float, producto: dict, numero_bolsas: int = 0) -> float:
    """
    Orquesta el cálculo completo del precio final de un producto,
    incluyendo su impuesto y el cargo por bolsas.

    producto es un dict con claves: tipo_impuesto, porcentaje_impuesto,
    grado_alcohol (opcional), volumen_ml (opcional).
    """
    tipo = producto.get("tipo_impuesto", "EXENTO").upper()

    if tipo == "LICOR":
        base = calcular_licores(
            valor,
            producto.get("grado_alcohol", 0),
            TARIFA_LICORES,
            producto.get("volumen_ml", 750),
        )
        precio = calcular_iva(base, producto.get("porcentaje_impuesto", 0.19))

    elif tipo == "INC":
        precio = calcular_impuesto_nacional_consumo(
            valor, producto.get("porcentaje_impuesto", 0.10)
        )

    elif tipo == "IVA":
        precio = calcular_iva(valor, producto.get("porcentaje_impuesto", 0))

    else:  # EXENTO
        precio = round(valor, 2)

    return round(precio + calcular_bolsa(numero_bolsas), 2)
