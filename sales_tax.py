import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

# pyrefly: ignore [missing-import]
from view.gui_sales_tax import SalesTaxApp

SalesTaxApp().run()