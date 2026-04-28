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
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp

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


# ── Fondo ──────────────────────────────────────────────
class Background(BoxLayout):
    """Fondo adaptable."""

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
        root = Background(orientation="vertical")

        scroll = ScrollView(size_hint=(1, 1))

        # Contenedor principal
        wrapper = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(15)
        )
        wrapper.bind(minimum_height=wrapper.setter("height"))

        # Tarjeta principal
        form = BoxLayout(
            orientation="vertical",
            size_hint=(0.95, None),
            height=dp(450),
            padding=dp(20),
            spacing=dp(15),
            pos_hint={"center_x": 0.5}
        )

        with form.canvas.before:
            Color(1, 1, 1, 1)
            self.form_bg = RoundedRectangle(
                size=form.size,
                pos=form.pos,
                radius=[20]
            )

        form.bind(size=self._update_form_bg, pos=self._update_form_bg)

        # ── Título ─────────────────────────
        form.add_widget(Label(
            text="Calculadora de Impuestos",
            font_size="24sp",
            bold=True,
            size_hint=(1, None),
            height=dp(60),
            color=(0.1, 0.1, 0.1, 1)
        ))

        # ── Formulario ─────────────────────
        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(180)
        )

        grid.add_widget(self._label("Producto"))
        self.spinner = Spinner(
            text="Seleccione",
            values=list(PRODUCTOS.keys()),
            font_size="16sp",
            size_hint_y=None,
            height=dp(45),
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

        # ── Resultado ──────────────────────
        self.result_label = Label(
            text="",
            font_size="20sp",
            bold=True,
            size_hint=(1, None),
            height=dp(50),
            color=(0.1, 0.4, 0.1, 1)
        )
        form.add_widget(self.result_label)

        # ── Botón ──────────────────────────
        calculate_button = Button(
            text="Calcular",
            font_size="18sp",
            size_hint=(1, None),
            height=dp(50),
            background_normal="",
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        calculate_button.bind(on_press=self.calculate_total)

        form.add_widget(calculate_button)

        wrapper.add_widget(form)
        scroll.add_widget(wrapper)
        root.add_widget(scroll)

        return root

    # ── Helpers UI ─────────────────────────
    def _label(self, text):
        return Label(
            text=text,
            font_size="16sp",
            size_hint_y=None,
            height=dp(45),
            color=(0.2, 0.2, 0.2, 1)
        )

    def _input(self):
        return TextInput(
            multiline=False,
            font_size="16sp",
            size_hint_y=None,
            height=dp(45),
            padding=[dp(10), dp(10)],
            background_normal="",
            background_active="",
            background_color=(0.96, 0.96, 0.96, 1),
            foreground_color=(0, 0, 0, 1)
        )

    def _update_form_bg(self, instance, _):
        self.form_bg.size = instance.size
        self.form_bg.pos = instance.pos

    # ── Lógica UI ──────────────────────────
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
            self._show_error("Ingrese valores numéricos válidos")
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
        content = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(15)
        )

        error_label = Label(
            text=message,
            font_size="16sp",
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(100),
            color=(1, 1, 1, 1)
        )

        def update_text(*args):
            error_label.text_size = (error_label.width - dp(10), None)

        error_label.bind(size=update_text)

        close_button = Button(
            text="Cerrar",
            size_hint=(1, None),
            height=dp(50),
            background_normal="",
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )

        content.add_widget(error_label)
        content.add_widget(close_button)

        popup = Popup(
            title="Error",
            content=content,
            size_hint=(0.85, 0.35),
            auto_dismiss=False
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    SalesTaxApp().run()
