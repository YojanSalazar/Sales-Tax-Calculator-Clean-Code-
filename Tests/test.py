import unittest
import sys

sys.path.append("src")

import model.Exceptions as Exceptions
import model.app_logic as app_logic

class TestCalculatorTax(unittest.TestCase):
    # Casos normales.

    def test_normal1(self):
    # ENTRADAS
    # Verifica que el cálculo del IVA del 19% funcione
    # correctamente para un producto con precio base.   

        valor: float = 20000
        impuesto = 19 / 100


        valor_calculado = app_logic.calcular_iva(valor, impuesto)

        valor_esperado = 23800

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)
    
    def test_normal2(self):
    # ENTRADAS
    # Verifica el cálculo del IVA del 5% aplicado a un
    # producto con un precio base específico.

        valor: float = 5800
        impuesto = 5/100

        valor_calculado = app_logic.calcular_iva(valor, impuesto)

        valor_esperado = 6090

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)
    
    def test_normal3(self):
    # ENTRADAS
    # Verifica que el cálculo del IVA del 19% funcione
    # correctamente para un producto con precio base.
        valor: float = 4000
        impuesto = 19 / 100

        valor_calculado = app_logic.calcular_iva(valor, impuesto)

        valor_esperado = 4760

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)

    def test_excento(self):
    #Caso exento de impuestos, el valor calculado debe ser igual al valor ingresado.
    # ENTRADAS
    # Verifica que cuando un producto está exento de IVA
    # el valor final sea igual al valor base.
  
        valor = 18000
        impuesto = 0

        valor_calculado = app_logic.calcular_iva(valor, impuesto)
        valor_esperado = 18000

        self.assertEqual(valor_calculado, valor_esperado)

    def test_licores(self):
    #Caso de calculo de licores, se espera
    # ENTRADAS
    # Verifica el cálculo del impuesto aplicado a licores.
    # Primero se calcula la base gravable del licor y luego
    # se aplica el IVA correspondiente.

        valor = 112000
        impuesto = 19/100
        grado = 40
        volumen = 750
        tarifa = 342

        calcular_licor = app_logic.calcular_licores(valor, grado, tarifa, volumen)

        valor_calculado = app_logic.calcular_iva(calcular_licor, impuesto)
        valor_esperado = 149559.2

        self.assertAlmostEqual(valor_calculado, valor_esperado, 2)
    
    def test_impuesto_nacional_consumo(self):
    # ENTRADAS
    # Verifica el cálculo del Impuesto Nacional al Consumo
    # aplicado a un producto específico.

        valor = 14000
        impuesto = 10/100

        calcular_licor = app_logic.calculte_impuesto_nacional_consumo(valor, impuesto)

        valor_esperado = 15400

        self.assertAlmostEqual(calcular_licor, valor_esperado, 2)
    
    def test_bolsa(self):
    # Impuesto de bolsa, se espera que el valor calculado sea igual al valor ingresado mas el impuesto.
    # ENTRADAS
    # Verifica el cálculo del impuesto por bolsas plásticas
    # multiplicando el valor del impuesto por el número
    # de bolsas utilizadas.

        impuesto = 75
        numero_bolsas = 10
        
        calcular_bolsa = app_logic.calcular_bolsa(impuesto, numero_bolsas)

        valor_esperado = 750

        self.assertAlmostEqual(calcular_bolsa, valor_esperado, 2)
    
    def test_error_negativo(self):
    #Caso de valor negativo, se espera que el valor calculado sea igual al valor ingresado.
    # ENTRADAS
    # Verifica que el sistema lance una excepción cuando
    # se intenta calcular un impuesto con un valor negativo
    # para el precio del producto.

        valor = -10000
        impuesto = 19/100

        with self.assertRaises(Exceptions.NegativeValueError):
            app_logic.calcular_iva(valor, impuesto)
    
    def test_error_compra(self):
    #Caso de valor igual a 0, se espera que el valor calculado sea igual al mensaje de error.
    # ENTRADAS
    # Verifica que el sistema lance una excepción cuando
    # el valor del producto es igual a cero.

        valor = 0
        impuesto = 19/100
        
        with self.assertRaises(Exceptions.ZeroValueError):
            app_logic.calcular_iva(valor, impuesto)
            app_logic.calculte_impuesto_nacional_consumo(valor, impuesto)
            app_logic.calcular_bolsa(impuesto, 10)

    def test_error_IVA(self):
    # Caso de IVA mayor al permitido, se espera que el valor calculado sea igual al mensaje de error.
    # ENTRADAS
    # Verifica que el sistema lance una excepción cuando
    # el porcentaje de IVA supera el valor permitido.
        
        valor = 10000
        impuesto = 20 /100

        with self.assertRaises(Exceptions.InvalidTaxError):
            app_logic.calcular_iva(valor, impuesto)      
    

    def test_errror_IVA_negativo(self):
    # Caso de IVA negativo, se espera que el valor calculado sea igual al mensaje de error.
    # ENTRADAS
    # Verifica que el sistema lance una excepción cuando
    # el porcentaje de IVA ingresado es negativo.

        valor = 10000
        impuesto = -10 /100

        with self.assertRaises(Exceptions.NegativeIVAError):
            app_logic.calcular_iva(valor, impuesto)
    

if __name__ == "__main__":
    unittest.main()