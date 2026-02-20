import unittest

import app_logic



class TestCalculatorTax(unittest.TestCase):
    # Casos normales.

    def test_normal1(self):
        # ENTRADAS

        valor: float = 20000
        tax = 19 / 100


        valor_calculado = app_logic.calculate_iva(valor, tax)

        valor_esperado = 23800

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)
    
    def test_normal2(self):
        # ENTRADAS

        valor: float = 5800
        tax = 5/100

        valor_calculado = app_logic.calculate_iva(valor, tax)

        valor_esperado = 6090

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)

    def test_excento(self):
        #Caso exento de impuestos, el valor calculado debe ser igual al valor ingresado.
        # ENTRADAS
  
        valor = 18000
        tax = 0

        valor_calculado = app_logic.calculate_iva(valor, tax)
        valor_esperado = 18000

        self.assertEqual(valor_calculado, valor_esperado)

    def test_licores(self):
        #Caso de calculo de licores, se espera
        # ENTRADAS

        valor = 112000
        tax = 19/100
        grado = 40
        volumen = 750
        tarifa = 342

        calular_licor = app_logic.calculate_licores(valor, grado, tarifa, volumen)

        valor_calculado = app_logic.calculate_iva(calular_licor, tax)
        valor_esperado = 149559.2

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)
    
    def test_impuesto_nacional_consumo(self):
        # ENTRADAS
        valor = 14000
        tax = 10/100

        calular_licor = app_logic.calculte_impuesto_nacional_consumo(valor, tax)

        valor_esperado = 15400

        self.assertAlmostEqual(calular_licor, valor_esperado, 2)
    
    def test_bolsa(self):
        # Impuesto de bolsa, se espera que el valor calculado sea igual al valor ingresado mas el impuesto.
         # ENTRADAS
        valor = 1000
        tax = 75
        numero_bolsas = 10
        
        calular_bolsa = app_logic.Calculate_bolsa(valor, tax, numero_bolsas)

        valor_esperado = 1750

        self.assertAlmostEqual(calular_bolsa, valor_esperado, 2)
    
    def test_error_negativo(self):
        #Caso de valor negativo, se espera que el valor calculado sea igual al valor ingresado.
        # ENTRADAS

        valor = -10000
        tax = 19/100

        with self.assertRaises(Exception):
            app_logic.calculate_iva(valor, tax)
    
    def test_error_compra(self):
    #Caso de valor igual a 0, se espera que el valor calculado sea igual al mensaje de error.
        # ENTRADAS
        
        valor = 0
        tax = 19/100
        

        with self.assertRaises(Exception):
            app_logic.calculate_iva(valor, tax)
            app_logic.calculte_impuesto_nacional_consumo(valor, tax)
            app_logic.Calculate_bolsa(valor, tax, 10)

    def test_error_IVA(self):
    # Caso de IVA mayor al permitido, se espera que el valor calculado sea igual al mensaje de error.
        # ENTRADAS
        valor = 10000
        tax = 20 /100

        with self.assertRaises(Exception):
            app_logic.calculate_iva(valor, tax)      
    

        
    



if __name__ == "__main__":
    unittest.main()