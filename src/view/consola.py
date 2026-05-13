"""
Interfaz de consola para la Calculadora de Impuestos de Venta.

Permite: insertar, buscar, actualizar y eliminar productos,
además de calcular el precio final con impuestos.
"""

import sys
sys.path.append("src")

from model.Producto import Producto
from model.app_logic_nuevo import calcular_precio_final
from model.Exceptions_nuevo import (
    ErrorProductoNoEncontrado,
    ErrorProductoYaExiste,
    ErrorCalculoImpuesto,
    ErrorOpcionInvalida,
)
import controller.ControladorProductos as ControladorProductos


# ── Helpers de entrada ───────────────────────────────────────────────────────

def leer_str(mensaje: str) -> str:
    return input(mensaje).strip()


def leer_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("  Valor inválido, ingrese un número decimal.")


def leer_int(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("  Valor inválido, ingrese un número entero.")


def leer_tipo_impuesto() -> str:
    tipos = {"1": "IVA", "2": "INC", "3": "LICOR", "4": "EXENTO"}
    print("  Tipos de impuesto:")
    for k, v in tipos.items():
        print(f"    {k}. {v}")
    while True:
        opcion = input("  Seleccione tipo (1-4): ").strip()
        if opcion in tipos:
            return tipos[opcion]
        print("  Opción inválida.")


def leer_datos_producto(nombre: str = None) -> Producto:
    """Solicita los campos de un Producto al usuario."""
    if nombre is None:
        nombre = leer_str("  Nombre del producto : ")

    tipo = leer_tipo_impuesto()
    porcentaje = leer_float("  Porcentaje impuesto (ej. 0.19 para 19%): ")

    grado, volumen = 0.0, 0
    if tipo == "LICOR":
        grado = leer_float("  Grado de alcohol    : ")
        volumen = leer_int("  Volumen en ml       : ")

    return Producto(nombre, tipo, porcentaje, grado, volumen)


# ── Opciones del menú ────────────────────────────────────────────────────────

def insertar_producto():
    print("\n── Insertar producto ──")
    try:
        producto = leer_datos_producto()
        ControladorProductos.insertar(producto)
        print(f"  ✓ Producto '{producto.nombre}' insertado correctamente.")
    except ErrorProductoYaExiste as e:
        print(f"  ✗ {e}")
    except ErrorCalculoImpuesto as e:
        print(f"  ✗ {e}")


def buscar_producto():
    print("\n── Buscar producto ──")
    nombre = leer_str("  Nombre a buscar: ")
    try:
        p = ControladorProductos.buscar_por_nombre(nombre)
        print(f"\n  Nombre    : {p.nombre}")
        print(f"  Impuesto  : {p.tipo_impuesto}  ({p.porcentaje_impuesto * 100:.1f} %)")
        if p.tipo_impuesto == "LICOR":
            print(f"  Grado     : {p.grado_alcohol}°")
            print(f"  Volumen   : {p.volumen_ml} ml")
    except ErrorProductoNoEncontrado as e:
        print(f"  ✗ {e}")


def listar_productos():
    print("\n── Listado de productos ──")
    productos = ControladorProductos.buscar_todos()
    if not productos:
        print("  No hay productos registrados.")
        return
    print(f"  {'Nombre':<25} {'Tipo':<8} {'Impuesto':>10}")
    print("  " + "-" * 47)
    for p in productos:
        print(f"  {p.nombre:<25} {p.tipo_impuesto:<8} {p.porcentaje_impuesto*100:>9.1f}%")


def actualizar_producto():
    print("\n── Actualizar producto ──")
    nombre = leer_str("  Nombre del producto a actualizar: ")
    try:
        ControladorProductos.buscar_por_nombre(nombre)   # verifica que existe
        print("  Ingrese los nuevos datos:")
        producto = leer_datos_producto(nombre=nombre)
        ControladorProductos.actualizar(producto)
        print(f"  ✓ Producto '{nombre}' actualizado correctamente.")
    except ErrorProductoNoEncontrado as e:
        print(f"  ✗ {e}")


def eliminar_producto():
    print("\n── Eliminar producto ──")
    nombre = leer_str("  Nombre del producto a eliminar: ")
    confirmacion = leer_str(f"  ¿Seguro que desea eliminar '{nombre}'? (s/n): ")
    if confirmacion.lower() != "s":
        print("  Operación cancelada.")
        return
    try:
        ControladorProductos.borrar(nombre)
        print(f"  ✓ Producto '{nombre}' eliminado correctamente.")
    except ErrorProductoNoEncontrado as e:
        print(f"  ✗ {e}")


def calcular_precio():
    print("\n── Calcular precio final ──")
    nombre = leer_str("  Nombre del producto: ")
    try:
        p = ControladorProductos.buscar_por_nombre(nombre)
        precio_base = leer_float("  Precio base         : $")
        bolsas = leer_int("  Número de bolsas    : ")

        producto_dict = {
            "tipo_impuesto": p.tipo_impuesto,
            "porcentaje_impuesto": p.porcentaje_impuesto,
            "grado_alcohol": p.grado_alcohol,
            "volumen_ml": p.volumen_ml,
        }
        total = calcular_precio_final(precio_base, producto_dict, bolsas)
        print(f"\n  Precio final (con impuestos y bolsas): ${total:,.2f}")
    except ErrorProductoNoEncontrado as e:
        print(f"  ✗ {e}")
    except ErrorCalculoImpuesto as e:
        print(f"  ✗ {e}")


# ── Menú principal ───────────────────────────────────────────────────────────

OPCIONES = {
    "1": ("Insertar producto",   insertar_producto),
    "2": ("Buscar producto",     buscar_producto),
    "3": ("Listar productos",    listar_productos),
    "4": ("Actualizar producto", actualizar_producto),
    "5": ("Eliminar producto",   eliminar_producto),
    "6": ("Calcular precio",     calcular_precio),
    "0": ("Salir",               None),
}


def mostrar_menu():
    print("\n" + "═" * 40)
    print("   CALCULADORA DE IMPUESTOS DE VENTA")
    print("═" * 40)
    for clave, (descripcion, _) in OPCIONES.items():
        print(f"  {clave}. {descripcion}")
    print("═" * 40)


def main():
    ControladorProductos.crear_tabla()
    print("Bienvenido a la Calculadora de Impuestos de Venta.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            print("¡Hasta luego!")
            break

        if opcion in OPCIONES:
            _, accion = OPCIONES[opcion]
            accion()
        else:
            print(f"  ✗ {ErrorOpcionInvalida()}")


if __name__ == "__main__":
    main()
