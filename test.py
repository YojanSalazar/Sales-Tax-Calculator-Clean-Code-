import unittest
import app_logic

class TestCalculatorTax(unittest.TestCase):
    
    # --- Casos Normales ---
    
    def test_normal1(self):
        """Caso Normal: Shampoo (IVA 19%)"""
        valor: float = 20000
        tax = 19 / 100
        valor_calculado = app_logic.calculate_iva(valor, tax)
        valor_esperado = 23800
        self.assertAlmostEqual(valor_calculado, valor_esperado, places=2)
    
    def test_normal2(self):
        """Caso Normal 2: Dolex (IVA 5%)"""
        valor: float = 5800
        tax = 5 / 100
        valor_calculado = app_logic.calculate_iva(valor, tax)
        valor_esperado = 6090
        self.assertAlmostEqual(valor_calculado, valor_esperado, places=2)

    def test_normal3(self):
        """Caso Normal 3: Barra Chocolate (IVA 19%)"""
        valor: float = 4000
        tax = 19 / 100
        valor_calculado = app_logic.calculate_iva(valor, tax)
        valor_esperado = 4760
        self.assertAlmostEqual(valor_calculado, valor_esperado, places=2)

    # --- Casos Excepcionales ---

    def test_excento(self):
        """Producto Exento: Canasta de Huevos (N/A)"""
        valor = 18000
        tax = 0
        valor_calculado = app_logic.calculate_iva(valor, tax)
        valor_esperado = 18000
        self.assertEqual(valor_calculado, valor_esperado)

    def test_licores(self):
        """Licores: Whisky Johnny Walker (Licores + IVA 19%)"""
        valor = 112000
        tax = 19 / 100
        grado = 40
        volumen = 750
        tarifa = 342
        # Primero calculamos la base con la lógica de licores
        base_licor = app_logic.calculate_licores(valor, grado, tarifa, volumen)
        # Luego aplicamos el IVA sobre esa base
        valor_calculado = app_logic.calculate_iva(base_licor, tax)
        valor_esperado = 149559.2
        # La precisión de 2 decimales es suficiente para valores monetarios
        self.assertAlmostEqual(valor_calculado, valor_esperado, places=2)

    def test_cigarrillos(self):
        """Cigarrillos: INC 10%"""
        valor = 14000
        tax = 10 / 100
        valor_calculado = app_logic.calculate_inc(valor, tax)
        valor_esperado = 15800
        self.assertAlmostEqual(valor_calculado, valor_esperado, places=2)

    # --- Casos de Error ---

    def test_error_precio_negativo(self):
        """Error: Precio Negativo"""
        valor = -10000
        tax = 19 / 100
        resultado = app_logic.calculate_iva(valor, tax)
        self.assertEqual(resultado, "ERROR: el precio debe ser mayor que 0")

    def test_error_compra_cero(self):
        """Error: Precio Cero"""
        valor = 0
        tax = 0
        resultado = app_logic.calculate_iva(valor, tax)
        self.assertEqual(resultado, "ERROR: el precio del producto no puede ser cero")

    def test_error_impuesto_iva_alto(self):
        """Error: Impuesto IVA alto (> 19%)"""
        valor = 20000
        tax = 30 / 100
        resultado = app_logic.calculate_iva(valor, tax)
        self.assertEqual(resultado, "ERROR: el iva no puede superar el 19%")

if __name__ == "__main__":
    unittest.main()