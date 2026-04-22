"""Interfaz gráfica con Kivy para la calculadora de impuestos de venta."""
 
import sys
sys.path.append("src")
 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
 
import model.app_logic as app_logic
from model import Exceptions
 
# ── Constantes ───────────────────────────────────────────────────────────────
TARIFA_BOLSA   = 75
TARIFA_LICORES = 342
 
PRODUCTOS = {
    "Shampoo":            {"iva": 0.19},
    "Dolex":              {"iva": 0.05},
    "Barra de Chocolate": {"iva": 0.05},
    "Canasta de Huevos":  {"iva": 0.00},
    "Whisky":             {"iva": 0.19, "licor": {"grado": 40, "volumen": 750}},
    "Cigarrillos":        {"inc": 0.10},
    "Cerveza":            {"iva": 0.19, "licor": {"grado": 10, "volumen": 650}},
}
 
 
class ImpuestosApp(App):
    def build(self):
        # Contenedor principal: dos columnas, igual que el profesor
        contenedor = GridLayout(cols=2, padding=20, spacing=10)
 
        # Fila 1: Producto
        contenedor.add_widget(Label(text="Producto"))
        self.spinner = Spinner(
            text="Seleccione un producto",
            values=list(PRODUCTOS.keys()),
            font_size=16,
        )
        contenedor.add_widget(self.spinner)
 
        # Fila 2: Precio
        contenedor.add_widget(Label(text="Precio del producto"))
        self.precio = TextInput(font_size=20, multiline=False)
        contenedor.add_widget(self.precio)
 
        # Fila 3: Bolsas
        contenedor.add_widget(Label(text="Número de bolsas"))
        self.bolsas = TextInput(font_size=20, multiline=False)
        contenedor.add_widget(self.bolsas)
 
        # Fila 4: Resultado y botón
        self.resultado = Label(text="")
        contenedor.add_widget(self.resultado)
 
        calcular = Button(text="Calcular", font_size=30)
        contenedor.add_widget(calcular)
 
        # Conectar botón con el callback, igual que el profesor
        calcular.bind(on_press=self.calcular)
 
        return contenedor
 
    def calcular(self, valor):
        try:
            self.validar()
 
            precio   = float(self.precio.text)
            bolsas   = int(self.bolsas.text)
            nombre   = self.spinner.text
            producto = PRODUCTOS[nombre]
 
            precio_producto = self.aplicar_impuesto(precio, producto)
            precio_bolsas   = app_logic.Calculate_bolsa(TARIFA_BOLSA, bolsas)
 
            total = precio_producto + precio_bolsas
            self.resultado.text = f"Total: ${total:,.2f}"
 
        except Exceptions.TaxCalculationError as e:
            self.mostrar_error(str(e))
        except ValueError:
            self.resultado.text = "Ingrese un número válido"
        except Exception as e:
            self.mostrar_error(str(e))
 
    def aplicar_impuesto(self, valor, producto):
        """Aplica el impuesto correspondiente según el tipo de producto."""
        if "licor" in producto:
            grado   = producto["licor"]["grado"]
            volumen = producto["licor"]["volumen"]
            valor   = app_logic.calculate_licores(valor, grado, TARIFA_LICORES, volumen)
 
        if "inc" in producto:
            return app_logic.calculte_impuesto_nacional_consumo(valor, producto["inc"])
 
        return app_logic.calculate_iva(valor, producto.get("iva", 0))
 
    def validar(self):
        """Verifica que los datos ingresados sean correctos antes de calcular."""
        if self.spinner.text not in PRODUCTOS:
            raise Exception("Seleccione un producto de la lista")
 
        if not self.precio.text:
            raise Exception("Ingrese el precio del producto")
 
        if not self.bolsas.text:
            raise Exception("Ingrese el número de bolsas")
 
    def mostrar_error(self, mensaje):
        """Abre una ventana emergente con el mensaje de error."""
        contenido = GridLayout(cols=1)
        contenido.add_widget(Label(text=mensaje))
        cerrar = Button(text="Cerrar")
        contenido.add_widget(cerrar)
 
        popup = Popup(title="Error", content=contenido, size_hint=(0.8, 0.4))
        cerrar.bind(on_press=popup.dismiss)
        popup.open()
 
 
if __name__ == "__main__":
    ImpuestosApp().run()