"""Módulo de interfaz de consola para la calculadora de impuestos de venta."""

import sys
sys.path.append("src")

import model.app_logic as app_logic
from model import Exceptions


TARIFA_BOLSA = 75
TARIFA_LICORES = 342

PRODUCTOS = {
    "1": {"nombre": "Shampoo",             "iva": 0.19},
    "2": {"nombre": "Dolex",               "iva": 0.05},
    "3": {"nombre": "Barra de Chocolate",  "iva": 0.05},
    "4": {"nombre": "Canasta de Huevos",   "iva": 0.00},
    "5": {"nombre": "Whisky",              "iva": 0.19, "licor": {"grado": 40, "volumen": 750}},
    "6": {"nombre": "Cigarrillos",         "inc": 0.10},
    "7": {"nombre": "Cerveza",             "iva": 0.19, "licor": {"grado": 10, "volumen": 650}},
}


def leer_float(mensaje: str) -> float:
    """Lee un número decimal desde consola, reintentando si el valor no es válido."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Valor inválido, ingrese un número.")


def leer_int(mensaje: str) -> int:
    """Lee un número entero desde consola, reintentando si el valor no es válido."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Valor inválido, ingrese un número entero.")


def calcular_precio_con_impuesto(valor: float, producto: dict) -> float:
    """Aplica el impuesto correspondiente al producto (IVA, INC o licores)."""
    if "licor" in producto:
        grado = producto["licor"]["grado"]
        volumen = producto["licor"]["volumen"]
        valor = app_logic.calculate_licores(valor, grado, TARIFA_LICORES, volumen)

    if "inc" in producto:
        return app_logic.calculte_impuesto_nacional_consumo(valor, producto["inc"])

    return app_logic.calculate_iva(valor, producto.get("iva", 0))


def procesar_compra(opcion: str) -> None:
    """Solicita los datos al usuario y muestra el precio final con impuestos."""
    producto = PRODUCTOS[opcion]

    valor = leer_float(f"Ingrese el precio de {producto['nombre']}: ")
    numero_bolsas = leer_int("Ingrese el número de bolsas: ")

    precio_producto = calcular_precio_con_impuesto(valor, producto)
    precio_bolsas = app_logic.Calculate_bolsa(TARIFA_BOLSA, numero_bolsas)

    total = precio_producto + precio_bolsas
    print(f"\nPrecio final (con impuestos y bolsas): ${total:.2f}\n")


def mostrar_menu() -> None:
    """Muestra el menú de productos disponibles."""
    print("\nMENU — Productos disponibles:\n")
    for clave, producto in PRODUCTOS.items():
        print(f"  {clave}. {producto['nombre']}")
    print("  0. Salir\n")


def main() -> None:
    """Función principal que controla el flujo del programa."""
    print("Bienvenido a la Calculadora de Impuestos de Venta.\n")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            print("Gracias por usar el programa. ¡Hasta luego!")
            break

        if opcion in PRODUCTOS:
            try:
                procesar_compra(opcion)
            except Exceptions.ErrorCalculoImpuesto as e:
                print(f"\nError en el cálculo: {e}\n")
        else:
            print(Exceptions.ErrorOpcionInvalida())


if __name__ == "__main__":
    main()