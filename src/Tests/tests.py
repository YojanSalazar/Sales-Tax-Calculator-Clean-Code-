"""
Tests de integración para ControladorProductos.

Usa PostgreSQL real — requiere servidor PostgreSQL activo
y configuración válida en SecretConfig.py.
"""

import sys
import os
import unittest

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_DIR)

from model.Producto import Producto
from model.Exceptions_nuevo import ErrorProductoNoEncontrado, ErrorProductoYaExiste
from controller.BaseDatos import BaseDatosSQLite
import controller.ControladorProductos as ControladorProductos
import SecretConfig as config


class TestControladorProductos(unittest.TestCase):
    """Pruebas CRUD completas sobre la tabla productos (SQLite para pruebas)."""

    # ── Test Fixtures ────────────────────────────────────────────────────────

    @classmethod
    def setUpClass(cls):
        """Se ejecuta UNA VEZ antes de todas las pruebas: configura la BD."""
        print("\n[setUpClass] Configurando BD SQLite en memoria para tests...")
        bd = BaseDatosSQLite(":memory:")
        ControladorProductos.configurar_bd(bd)
        # SQLite queries
        bd.ejecutar('''
            CREATE TABLE IF NOT EXISTS productos (
                nombre              VARCHAR(100)   PRIMARY KEY,
                tipo_impuesto       VARCHAR(10)    NOT NULL,
                porcentaje_impuesto NUMERIC(5,4)   NOT NULL DEFAULT 0,
                grado_alcohol       NUMERIC(5,2)   NOT NULL DEFAULT 0,
                volumen_ml          INTEGER        NOT NULL DEFAULT 0
            );
        ''')

    def setUp(self):
        """Se ejecuta ANTES de cada prueba: limpia la tabla."""
        print("\n[setUp] Limpiando datos para nuevo test...")
        ControladorProductos.borrar_filas()

    def tearDown(self):
        """Se ejecuta DESPUÉS de cada prueba."""
        print("[tearDown] Prueba finalizada.")

    @classmethod
    def tearDownClass(cls):
        """Se ejecuta UNA VEZ al final de todas las pruebas."""
        print("\n[tearDownClass] Suite finalizada.")

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _producto_shampoo(self):
        return Producto("Shampoo", "IVA", 0.19)

    def _producto_dolex(self):
        return Producto("Dolex", "IVA", 0.05)

    def _producto_whisky(self):
        return Producto("Whisky", "LICOR", 0.19, grado_alcohol=40, volumen_ml=750)

    def _producto_cigarrillos(self):
        return Producto("Cigarrillos", "INC", 0.10)

    def _producto_huevos(self):
        return Producto("Canasta de Huevos", "EXENTO", 0.00)

    def _assertProductoIgual(self, esperado: Producto, obtenido: Producto):
        self.assertEqual(esperado.nombre,               obtenido.nombre)
        self.assertEqual(esperado.tipo_impuesto,        obtenido.tipo_impuesto)
        self.assertAlmostEqual(esperado.porcentaje_impuesto, obtenido.porcentaje_impuesto, places=4)
        self.assertAlmostEqual(esperado.grado_alcohol,  obtenido.grado_alcohol,  places=2)
        self.assertEqual(esperado.volumen_ml,           obtenido.volumen_ml)

    # ════════════════════════════════════════════════════════════════════════
    # INSERTAR — 3 casos normales + 1 error
    # ════════════════════════════════════════════════════════════════════════

    def test_insertar_producto_iva(self):
        """Inserta un producto con IVA 19 % y lo recupera correctamente."""
        print("Ejecutando test_insertar_producto_iva")
        shampoo = self._producto_shampoo()
        ControladorProductos.insertar(shampoo)

        recuperado = ControladorProductos.buscar_por_nombre(shampoo.nombre)
        self._assertProductoIgual(shampoo, recuperado)

    def test_insertar_producto_licor(self):
        """Inserta un licor con grado de alcohol y volumen, y lo recupera."""
        print("Ejecutando test_insertar_producto_licor")
        whisky = self._producto_whisky()
        ControladorProductos.insertar(whisky)

        recuperado = ControladorProductos.buscar_por_nombre(whisky.nombre)
        self._assertProductoIgual(whisky, recuperado)

    def test_insertar_producto_exento(self):
        """Inserta un producto exento de impuesto y verifica que se guarda con 0 %."""
        print("Ejecutando test_insertar_producto_exento")
        huevos = self._producto_huevos()
        ControladorProductos.insertar(huevos)

        recuperado = ControladorProductos.buscar_por_nombre(huevos.nombre)
        self._assertProductoIgual(huevos, recuperado)
        self.assertAlmostEqual(recuperado.porcentaje_impuesto, 0.0, places=4)

    def test_insertar_duplicado_lanza_excepcion(self):
        """Insertar el mismo producto dos veces lanza ErrorProductoYaExiste."""
        print("Ejecutando test_insertar_duplicado_lanza_excepcion")
        shampoo = self._producto_shampoo()
        ControladorProductos.insertar(shampoo)

        with self.assertRaises(ErrorProductoYaExiste):
            ControladorProductos.insertar(shampoo)

    # ════════════════════════════════════════════════════════════════════════
    # BUSCAR — 3 casos normales + 1 error
    # ════════════════════════════════════════════════════════════════════════

    def test_buscar_producto_existente(self):
        """buscar_por_nombre retorna el producto correcto."""
        print("Ejecutando test_buscar_producto_existente")
        dolex = self._producto_dolex()
        ControladorProductos.insertar(dolex)

        resultado = ControladorProductos.buscar_por_nombre("Dolex")
        self._assertProductoIgual(dolex, resultado)

    def test_buscar_todos_retorna_lista(self):
        """buscar_todos retorna todos los productos insertados."""
        print("Ejecutando test_buscar_todos_retorna_lista")
        ControladorProductos.insertar(self._producto_shampoo())
        ControladorProductos.insertar(self._producto_dolex())
        ControladorProductos.insertar(self._producto_cigarrillos())

        lista = ControladorProductos.buscar_todos()
        self.assertEqual(len(lista), 3)

    def test_buscar_producto_inc(self):
        """buscar_por_nombre recupera correctamente un producto de tipo INC."""
        print("Ejecutando test_buscar_producto_inc")
        cigarrillos = self._producto_cigarrillos()
        ControladorProductos.insertar(cigarrillos)

        resultado = ControladorProductos.buscar_por_nombre("Cigarrillos")
        self.assertEqual(resultado.tipo_impuesto, "INC")
        self.assertAlmostEqual(resultado.porcentaje_impuesto, 0.10, places=4)

    def test_buscar_inexistente_lanza_excepcion(self):
        """buscar_por_nombre lanza ErrorProductoNoEncontrado para nombres que no existen."""
        print("Ejecutando test_buscar_inexistente_lanza_excepcion")
        with self.assertRaises(ErrorProductoNoEncontrado):
            ControladorProductos.buscar_por_nombre("ProductoQueNoExiste")

    # ════════════════════════════════════════════════════════════════════════
    # MODIFICAR (UPDATE) — 3 casos normales + 1 error
    # ════════════════════════════════════════════════════════════════════════

    def test_actualizar_porcentaje_impuesto(self):
        """Actualizar el porcentaje de impuesto y verificar el cambio."""
        print("Ejecutando test_actualizar_porcentaje_impuesto")
        shampoo = self._producto_shampoo()
        ControladorProductos.insertar(shampoo)

        shampoo.porcentaje_impuesto = 0.05   # cambia de 19 % a 5 %
        ControladorProductos.actualizar(shampoo)

        actualizado = ControladorProductos.buscar_por_nombre("Shampoo")
        self.assertAlmostEqual(actualizado.porcentaje_impuesto, 0.05, places=4)

    def test_actualizar_tipo_impuesto(self):
        """Cambiar el tipo de impuesto de IVA a EXENTO."""
        print("Ejecutando test_actualizar_tipo_impuesto")
        dolex = self._producto_dolex()
        ControladorProductos.insertar(dolex)

        dolex.tipo_impuesto = "EXENTO"
        dolex.porcentaje_impuesto = 0.0
        ControladorProductos.actualizar(dolex)

        actualizado = ControladorProductos.buscar_por_nombre("Dolex")
        self.assertEqual(actualizado.tipo_impuesto, "EXENTO")
        self.assertAlmostEqual(actualizado.porcentaje_impuesto, 0.0, places=4)

    def test_actualizar_datos_licor(self):
        """Actualizar grado de alcohol y volumen de un licor."""
        print("Ejecutando test_actualizar_datos_licor")
        whisky = self._producto_whisky()
        ControladorProductos.insertar(whisky)

        whisky.grado_alcohol = 43.0
        whisky.volumen_ml = 1000
        ControladorProductos.actualizar(whisky)

        actualizado = ControladorProductos.buscar_por_nombre("Whisky")
        self.assertAlmostEqual(actualizado.grado_alcohol, 43.0, places=2)
        self.assertEqual(actualizado.volumen_ml, 1000)

    def test_actualizar_inexistente_lanza_excepcion(self):
        """Actualizar un producto que no existe lanza ErrorProductoNoEncontrado."""
        print("Ejecutando test_actualizar_inexistente_lanza_excepcion")
        fantasma = Producto("NoExiste", "IVA", 0.19)
        with self.assertRaises(ErrorProductoNoEncontrado):
            ControladorProductos.actualizar(fantasma)

    # ════════════════════════════════════════════════════════════════════════
    # ELIMINAR (DELETE) — 1 caso normal + 1 error
    # ════════════════════════════════════════════════════════════════════════

    def test_borrar_producto_existente(self):
        """Borrar un producto y verificar que ya no se puede encontrar."""
        print("Ejecutando test_borrar_producto_existente")
        shampoo = self._producto_shampoo()
        ControladorProductos.insertar(shampoo)
        ControladorProductos.borrar("Shampoo")

        with self.assertRaises(ErrorProductoNoEncontrado):
            ControladorProductos.buscar_por_nombre("Shampoo")

    def test_borrar_inexistente_lanza_excepcion(self):
        """Borrar un producto que no existe lanza ErrorProductoNoEncontrado."""
        print("Ejecutando test_borrar_inexistente_lanza_excepcion")
        with self.assertRaises(ErrorProductoNoEncontrado):
            ControladorProductos.borrar("ProductoFantasma")


if __name__ == "__main__":
    unittest.main()
