import unittest

import app_logic

class TestCalculatorTax(unittest.TestCase):
        

    def test_normal1(self):
        valor: float = 20000
        tax = 19 / 100


        valor_calculado = app_logic.calculate_iva(valor, tax)

        valor_esperado = 23800

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)
    
    def test_normal2(self):
        valor: float = 5800
        tax = 5/100

        valor_calculado = app_logic.calculate_iva(valor, tax)

        valor_esperado = 6090

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)

    def test_excento(self):
        valor = 18000
        tax = 0

        valor_calculado = app_logic.calculate_iva(valor, tax)
        valor_esperado = 18000

        self.assertEqual(valor_calculado, valor_esperado)

    def test_licores(self):
        valor = 112000
        tax = 19/100
        grado = 40
        volumen = 750
        tarifa = 342

        calular_licor = app_logic.calculate_licores(valor, grado, tarifa, volumen)

        valor_calculado = app_logic.calculate_iva(calular_licor, tax)
        valor_esperado = 149559.2

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)
    



if __name__ == "__main__":
    unittest.main()