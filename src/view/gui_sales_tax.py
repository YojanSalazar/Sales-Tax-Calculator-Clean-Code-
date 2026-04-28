"""Interfaz gráfica con Kivy para la calculadora de impuestos."""

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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle

import model.app_logic as app_logic
from model import Exceptions


# ── Constantes ─────────────────────────────────────────
TARIFA_BOLSA = 75
TARIFA_LICORES = 342

PRODUCTOS = {
    "Shampoo": {"iva": 0.19},
    "Dolex": {"iva": 0.05},
    "Barra de Chocolate": {"iva": 0.05},
    "Canasta de Huevos": {"iva": 0.00},
    "Whisky": {"iva": 0.19, "licor": {"grado": 40, "volumen": 750}},
    "Cigarrillos": {"inc": 0.10},
    "Cerveza": {"iva": 0.19, "licor": {"grado": 10, "volumen": 650}},
}


# ── UI Components ──────────────────────────────────────
class Background(BoxLayout):
    """Fondo con color suave."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *_):
        self.rect.size = self.size
        self.rect.pos = self.pos


# ── App Principal ──────────────────────────────────────
class SalesTaxApp(App):

    def build(self):
        root = Background()

        container = AnchorLayout()

        # Tarjeta principal
        form = BoxLayout(
            orientation="vertical",
            size_hint=(0.85, 0.65),
            padding=20,
            spacing=15
        )

        with form.canvas.before:
            Color(1, 1, 1, 1)
            self.form_bg = RoundedRectangle(
                size=form.size,
                pos=form.pos,
                radius=[12]
            )

        form.bind(size=self._update_form_bg, pos=self._update_form_bg)

        # ── Título ─────────────────────────────
        form.add_widget(Label(
            text="Calculadora de Impuestos",
            font_size=22,
            bold=True,
            size_hint=(1, 0.15),
            color=(0.1, 0.1, 0.1, 1)
        ))

        # ── Grid ──────────────────────────────
        grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint=(1, None),
            height=150 
        )

        grid.add_widget(self._label("Producto"))
        self.spinner = Spinner(
            text="Seleccione",
            values=list(PRODUCTOS.keys()),
            font_size=16,
            background_normal="",
            background_color=(0.9, 0.92, 0.97, 1),
            color=(0, 0, 0, 1)
        )
        grid.add_widget(self.spinner)

        grid.add_widget(self._label("Precio"))
        self.precio_input = self._input()
        grid.add_widget(self.precio_input)

        grid.add_widget(self._label("Bolsas"))
        self.bolsas_input = self._input()
        grid.add_widget(self.bolsas_input)

        form.add_widget(grid)

        # ── Resultado ─────────────────────────
        self.result_label = Label(
            text="",
            font_size=20,
            bold=True,
            size_hint=(1, None),
            height=40,
            color=(0.1, 0.4, 0.1, 1)
        )
        form.add_widget(self.result_label)

        # ── Botón ────────────────────────────
        calculate_button = Button(
            text="Calcular",
            font_size=16,
            size_hint=(1, None),
            height=45,
            background_normal="",
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        calculate_button.bind(on_press=self.calculate_total)

        form.add_widget(calculate_button)

        container.add_widget(form)
        root.add_widget(container)

        return root

    # ── UI Helpers ───────────────────────────
    def _label(self, text):
        return Label(
            text=text,
            font_size=16,
            color=(0.2, 0.2, 0.2, 1)
        )

    def _input(self):
        return TextInput(
            multiline=False,
            font_size=16,
            padding=[10, 10],
            background_normal="",
            background_active="",
            background_color=(0.96, 0.96, 0.96, 1),
            foreground_color=(0, 0, 0, 1)
        )

    def _update_form_bg(self, instance, _):
        self.form_bg.size = instance.size
        self.form_bg.pos = instance.pos

    # ── Lógica UI ────────────────────────────
    def calculate_total(self, *_):
        try:
            self._validate_inputs()

            price = float(self.precio_input.text)
            bags = int(self.bolsas_input.text)
            product_name = self.spinner.text
            product = PRODUCTOS[product_name]

            product_price = self._apply_tax(price, product)
            bag_price = app_logic.Calculate_bolsa(TARIFA_BOLSA, bags)

            total = product_price + bag_price
            self.result_label.text = f"Total: ${total:,.2f}"

        except Exceptions.TaxCalculationError as error:
            self._show_error(str(error))
        except ValueError:
            self.result_label.text = "Ingrese valores numéricos válidos"
        except Exception as error:
            self._show_error(str(error))

    def _apply_tax(self, value, product):
        if "licor" in product:
            licor = product["licor"]
            value = app_logic.calculate_licores(
                value,
                licor["grado"],
                TARIFA_LICORES,
                licor["volumen"]
            )

        if "inc" in product:
            return app_logic.calculte_impuesto_nacional_consumo(
                value, product["inc"]
            )

        return app_logic.calculate_iva(value, product.get("iva", 0))

    def _validate_inputs(self):
        if self.spinner.text not in PRODUCTOS:
            raise Exception("Seleccione un producto")

        if not self.precio_input.text:
            raise Exception("Ingrese el precio")

        if not self.bolsas_input.text:
            raise Exception("Ingrese las bolsas")

    def _show_error(self, message):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message))

        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.4),
            background_normal="",
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )

        content.add_widget(close_button)

        popup = Popup(
            title="Error",
            content=content,
            size_hint=(0.7, 0.3)
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    SalesTaxApp().run()