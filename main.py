import sys
import os

# Agregamos la ruta "src" de manera absoluta para que funcione desde cualquier lado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

from view.gui_sales_tax import SalesTaxApp

SalesTaxApp().run()