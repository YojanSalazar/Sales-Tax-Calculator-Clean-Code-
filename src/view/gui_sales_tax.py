"""Interfaz gráfica con Kivy para la calculadora de impuestos."""

import sys
import os

# Agregamos la ruta "src" que está dos niveles arriba de este archivo
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_DIR)

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

import model.app_logic_nuevo as app_logic
from model.Producto import Producto
from model import Exceptions_nuevo as Exceptions
from controller.BaseDatos import BaseDatosSQLite
import controller.ControladorProductos as ControladorProductos


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
        # Initialize DB
        self.db = BaseDatosSQLite("productos.db")
        ControladorProductos.configurar_bd(self.db)
        # Create table if not exists (SQLite schema)
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS productos (
                nombre              VARCHAR(100)   PRIMARY KEY,
                tipo_impuesto       VARCHAR(10)    NOT NULL,
                porcentaje_impuesto NUMERIC(5,4)   NOT NULL DEFAULT 0,
                grado_alcohol       NUMERIC(5,2)   NOT NULL DEFAULT 0,
                volumen_ml          INTEGER        NOT NULL DEFAULT 0
            );
        ''')
        
        # Insert initial data if empty
        productos = ControladorProductos.buscar_todos()
        if not productos:
            try:
                ControladorProductos.insertar(Producto("Shampoo", "IVA", 0.19))
                ControladorProductos.insertar(Producto("Dolex", "IVA", 0.05))
                ControladorProductos.insertar(Producto("Cigarrillos", "INC", 0.10))
                ControladorProductos.insertar(Producto("Whisky", "LICOR", 0.19, 40, 750))
                ControladorProductos.insertar(Producto("Canasta de Huevos", "EXENTO", 0.00))
            except Exception:
                pass

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
            height=dp(500),
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
            values=self._obtener_nombres_productos(),
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
        self.bolsas_input.text = "0"
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

        # ── Botones ──────────────────────────
        buttons_layout = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None), height=dp(110))
        
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
        buttons_layout.add_widget(calculate_button)

        manage_button = Button(
            text="Gestión de Productos",
            font_size="18sp",
            size_hint=(1, None),
            height=dp(50),
            background_normal="",
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        manage_button.bind(on_press=self.open_manage_popup)
        buttons_layout.add_widget(manage_button)

        form.add_widget(buttons_layout)

        wrapper.add_widget(form)
        scroll.add_widget(wrapper)
        root.add_widget(scroll)

        return root

    def _obtener_nombres_productos(self):
        try:
            productos = ControladorProductos.buscar_todos()
            return [p.nombre for p in productos]
        except Exception:
            return []

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
            
            p = ControladorProductos.buscar_por_nombre(product_name)
            p_dict = {
                "tipo_impuesto": p.tipo_impuesto,
                "porcentaje_impuesto": p.porcentaje_impuesto,
                "grado_alcohol": p.grado_alcohol,
                "volumen_ml": p.volumen_ml,
            }

            total = app_logic.calcular_precio_final(price, p_dict, bags)
            self.result_label.text = f"Total: ${total:,.2f}"

        except Exceptions.ErrorProductoNoEncontrado:
            self._show_error("Producto no encontrado en la Base de Datos")
        except Exception as error:
            self._show_error(str(error))

    def _validate_inputs(self):
        if self.spinner.text == "Seleccione":
            raise Exception("Seleccione un producto")

        if not self.precio_input.text:
            raise Exception("Ingrese el precio")

        if not self.bolsas_input.text:
            raise Exception("Ingrese las bolsas")

    def _show_error(self, message):
        content = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(15))
        error_label = Label(
            text=message, font_size="16sp", halign="center", valign="middle",
            size_hint=(1, None), height=dp(100), color=(1, 1, 1, 1)
        )
        error_label.bind(size=lambda *x: setattr(error_label, 'text_size', (error_label.width - dp(10), None)))
        close_button = Button(
            text="Cerrar", size_hint=(1, None), height=dp(50),
            background_normal="", background_color=(0.8, 0.2, 0.2, 1), color=(1, 1, 1, 1)
        )
        content.add_widget(error_label)
        content.add_widget(close_button)

        popup = Popup(title="Mensaje", content=content, size_hint=(0.85, 0.4), auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def _show_success(self, message):
        self._show_error(message)

    # ── Gestión de Productos CRUD ─────────────────
    def open_manage_popup(self, *_):
        content = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        grid = GridLayout(cols=2, spacing=dp(5), size_hint_y=None, height=dp(250))
        
        grid.add_widget(self._label("Nombre:"))
        self.crud_nombre = self._input()
        grid.add_widget(self.crud_nombre)

        grid.add_widget(self._label("Tipo:"))
        self.crud_tipo = Spinner(
            text="IVA", values=["IVA", "INC", "LICOR", "EXENTO"],
            size_hint_y=None, height=dp(45)
        )
        grid.add_widget(self.crud_tipo)

        grid.add_widget(self._label("Porcentaje (ej 0.19):"))
        self.crud_porcentaje = self._input()
        self.crud_porcentaje.text = "0.0"
        grid.add_widget(self.crud_porcentaje)

        grid.add_widget(self._label("Grado Alc:"))
        self.crud_grado = self._input()
        self.crud_grado.text = "0.0"
        grid.add_widget(self.crud_grado)

        grid.add_widget(self._label("Volumen ml:"))
        self.crud_volumen = self._input()
        self.crud_volumen.text = "0"
        grid.add_widget(self.crud_volumen)

        content.add_widget(grid)

        # Botones CRUD
        buttons = GridLayout(cols=2, spacing=dp(5), size_hint_y=None, height=dp(100))
        
        btn_buscar = Button(text="Buscar", background_color=(0.2, 0.5, 0.9, 1))
        btn_buscar.bind(on_press=self.crud_action_buscar)
        buttons.add_widget(btn_buscar)

        btn_insert = Button(text="Insertar", background_color=(0.2, 0.8, 0.2, 1))
        btn_insert.bind(on_press=self.crud_action_insertar)
        buttons.add_widget(btn_insert)

        btn_update = Button(text="Modificar", background_color=(0.8, 0.8, 0.2, 1))
        btn_update.bind(on_press=self.crud_action_modificar)
        buttons.add_widget(btn_update)

        btn_delete = Button(text="Eliminar", background_color=(0.8, 0.2, 0.2, 1))
        btn_delete.bind(on_press=self.crud_action_eliminar)
        buttons.add_widget(btn_delete)

        content.add_widget(buttons)

        close_btn = Button(text="Cerrar", size_hint_y=None, height=dp(40))
        content.add_widget(close_btn)

        self.crud_popup = Popup(title="Gestión de Productos", content=content, size_hint=(0.95, 0.8), auto_dismiss=False)
        close_btn.bind(on_press=self.close_manage_popup)
        self.crud_popup.open()

    def close_manage_popup(self, *_):
        self.spinner.values = self._obtener_nombres_productos()
        if self.spinner.text not in self.spinner.values:
            self.spinner.text = "Seleccione"
        self.crud_popup.dismiss()

    def crud_action_buscar(self, *_):
        nombre = self.crud_nombre.text.strip()
        if not nombre:
            self._show_error("Ingrese un nombre para buscar")
            return
        try:
            p = ControladorProductos.buscar_por_nombre(nombre)
            self.crud_tipo.text = p.tipo_impuesto
            self.crud_porcentaje.text = str(p.porcentaje_impuesto)
            self.crud_grado.text = str(p.grado_alcohol)
            self.crud_volumen.text = str(p.volumen_ml)
            self._show_success(f"Producto '{nombre}' cargado.")
        except Exceptions.ErrorProductoNoEncontrado:
            self._show_error("Producto no encontrado.")

    def crud_action_insertar(self, *_):
        try:
            p = self._get_crud_producto()
            ControladorProductos.insertar(p)
            self._show_success(f"Producto '{p.nombre}' insertado.")
        except Exception as e:
            self._show_error(str(e))

    def crud_action_modificar(self, *_):
        try:
            p = self._get_crud_producto()
            ControladorProductos.actualizar(p)
            self._show_success(f"Producto '{p.nombre}' modificado.")
        except Exception as e:
            self._show_error(str(e))

    def crud_action_eliminar(self, *_):
        nombre = self.crud_nombre.text.strip()
        if not nombre:
            self._show_error("Ingrese un nombre para eliminar")
            return
        try:
            ControladorProductos.borrar(nombre)
            self._show_success(f"Producto '{nombre}' eliminado.")
            self.crud_nombre.text = ""
        except Exception as e:
            self._show_error(str(e))

    def _get_crud_producto(self):
        nombre = self.crud_nombre.text.strip()
        if not nombre:
            raise Exception("El nombre no puede estar vacío")
        try:
            porc = float(self.crud_porcentaje.text)
            grado = float(self.crud_grado.text)
            vol = int(self.crud_volumen.text)
        except ValueError:
            raise Exception("Porcentaje y grado deben ser decimales. Volumen debe ser entero.")
        
        return Producto(nombre, self.crud_tipo.text, porc, grado, vol)


if __name__ == "__main__":
    SalesTaxApp().run()
