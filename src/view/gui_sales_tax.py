"""Interfaz gráfica mejorada con Kivy para la calculadora de impuestos."""

import sys
sys.path.append("src")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import model.app_logic as app_logic
from model import Exceptions

# Tamaño de ventana
Window.size = (500, 500)

# ── Constantes ─────────────────────────────────────────
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


class Fondo(BoxLayout):
    """Fondo con color suave"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class SalesTaxApp(App):
    def build(self):

        root = Fondo(orientation="vertical")

        # Contenedor centrado
        wrapper = BoxLayout(
            orientation="vertical",
            padding=[40, 80],
        )

        # Grid principal (YA CORREGIDO)
        contenedor = GridLayout(
            cols=2,
            spacing=15,
            size_hint=(1, 1)
        )

        # ── Título ─────────────────────────────
        titulo = Label(
            text="Calculadora de Impuestos",
            font_size=26,
            bold=True,
            size_hint=(1, 0.2),
            color=(0.1, 0.1, 0.1, 1)
        )

        wrapper.add_widget(titulo)

        # ── Estilos ───────────────────────────
        def label_estilo(texto):
            return Label(
                text=texto,
                font_size=16,
                color=(0.2, 0.2, 0.2, 1)
            )

        def input_estilo():
            return TextInput(
                font_size=18,
                multiline=False,
                padding=10,
                background_normal="",
                background_color=(1, 1, 1, 1),
                foreground_color=(0, 0, 0, 1)
            )

        # ── Campos ────────────────────────────
        contenedor.add_widget(label_estilo("Producto"))
        self.spinner = Spinner(
            text="Seleccione",
            values=list(PRODUCTOS.keys()),
            font_size=16,
            background_normal="",
            background_color=(0.8, 0.85, 0.95, 1),
            color=(0, 0, 0, 1)
        )
        contenedor.add_widget(self.spinner)

        contenedor.add_widget(label_estilo("Precio"))
        self.precio = input_estilo()
        contenedor.add_widget(self.precio)

        contenedor.add_widget(label_estilo("Bolsas"))
        self.bolsas = input_estilo()
        contenedor.add_widget(self.bolsas)

        # Resultado
        self.resultado = Label(
            text="",
            font_size=20,
            bold=True,
            color=(0.1, 0.4, 0.1, 1)
        )
        contenedor.add_widget(self.resultado)

        # Botón
        calcular = Button(
            text="Calcular",
            font_size=20,
            size_hint=(1, None),
            height=50,
            background_normal="",
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        contenedor.add_widget(calcular)

        calcular.bind(on_press=self.calcular)

        wrapper.add_widget(contenedor)
        root.add_widget(wrapper)

        return root

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
        if "licor" in producto:
            grado   = producto["licor"]["grado"]
            volumen = producto["licor"]["volumen"]
            valor   = app_logic.calculate_licores(valor, grado, TARIFA_LICORES, volumen)

        if "inc" in producto:
            return app_logic.calculte_impuesto_nacional_consumo(valor, producto["inc"])

        return app_logic.calculate_iva(valor, producto.get("iva", 0))

    def validar(self):
        if self.spinner.text not in PRODUCTOS:
            raise Exception("Seleccione un producto")

        if not self.precio.text:
            raise Exception("Ingrese el precio")

        if not self.bolsas.text:
            raise Exception("Ingrese las bolsas")

    def mostrar_error(self, mensaje):
        contenido = BoxLayout(orientation="vertical", padding=10, spacing=10)
        contenido.add_widget(Label(text=mensaje))

        cerrar = Button(
            text="Cerrar",
            size_hint=(1, 0.4),
            background_normal="",
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        contenido.add_widget(cerrar)

        popup = Popup(title="Error", content=contenido, size_hint=(0.7, 0.3))
        cerrar.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    SalesTaxApp().run()