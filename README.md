# Calculadora de Impuestos de Venta

## Creadores originales
Luis Alejandro Correa  

Yojan Esteban Salazar  

## Fork realizado por
Jhairo Esteban Muñetón Cortés

Nelson David Jiménez Ruiz  

---

# Descripción
Este proyecto corresponde a una aplicación desarrollada para el curso **Código Limpio**.

La **Calculadora de Impuestos de Venta** permite calcular el precio final de un producto aplicando distintos tipos de impuestos presentes en el sistema tributario.

El sistema recibe información básica del producto, identifica el tipo de impuesto aplicable y calcula automáticamente el valor final del producto.

Inicialmente el modelo fue implementado en **Excel**, donde se verificó el flujo de procesamiento de los datos y se validaron los resultados mediante casos de prueba.

---

# Objetivo
Desarrollar una herramienta clara y estructurada que permita comprender el proceso de cálculo de impuestos de venta, aplicando los principios de **Código Limpio** y mostrando de forma clara el flujo de información dentro de un sistema.

---

# Funcionalidades principales

- Cálculo del precio final de productos aplicando distintos tipos de impuestos
- Simulación de diferentes escenarios de cálculo
- Comparación entre resultados esperados y resultados calculados
- Validación de datos de entrada
- Visualización clara del flujo **entrada → proceso → salida**
- Interfaz gráfica desarrollada con **Kivy**

---

# Ejecución

## Prerrequisitos
Antes de ejecutar y utilizar el proyecto se debe contar con:

- **Python 3.8 o superior**. Puede verificar su versión con:

```bash
python --version
```

- **Microsoft Excel** o cualquier software compatible con archivos `.xlsx`
- Descargar o clonar este repositorio en el computador
- Instalar las dependencias necesarias:

```bash
pip install kivy
```

---

## Ejecución del proyecto

### Opción 1 — Interfaz gráfica (GUI)

1. Ubicarse en la carpeta raíz del proyecto.
2. Ejecutar el siguiente comando:

```bash
python sales_tax.py
```

Esto abrirá la interfaz gráfica desarrollada con Kivy, donde podrá seleccionar el producto, ingresar el precio y el número de bolsas para calcular el total con impuestos.

### Opción 2 — Consola

1. Ubicarse en la carpeta raíz del proyecto.
2. Ejecutar el siguiente comando:

```bash
py src/view/logica_consola.py
```

### Opción 3 — Excel

1. Abrir el archivo de **Excel** incluido en el repositorio.
2. Ingresar los datos solicitados en las columnas correspondientes.
3. El sistema calculará automáticamente los impuestos y el precio final del producto.

---
## Ejecución de pruebas unitarias

Desde la carpeta raíz del proyecto, ejecutar:
```bash
python -m unittest discover -v -s Tests -p "*test*.py"
```

# Construcción

El proyecto se organiza en las siguientes carpetas:

**carpeta documentos**  
Contiene documentación adicional relacionada con el proyecto.

**carpeta src**  
Contiene el código fuente o archivos principales del sistema (model y view).

**carpeta Tests**  
Incluye los casos de prueba utilizados para validar los cálculos del sistema.

Cada carpeta puede incluir un archivo `__init__.py` para permitir que Python reconozca el directorio como módulo en caso de implementaciones futuras.

---

# Entradas y salidas

## Entradas

| Campo | Descripción |
|------|-------------|
| Valor del producto | Precio base del producto |
| Porcentaje de impuesto | Porcentaje correspondiente al impuesto |
| Número de bolsas | Cantidad de bolsas plásticas utilizadas |

Ejemplos de impuestos:

- IVA 19%
- IVA 5%
- INC 10%
- Impuesto a licores
- Impuesto a bolsas

---

## Proceso

El sistema calcula el valor del impuesto y el precio final del producto a partir del valor base.

### Pasos del cálculo

1. Se toma el valor base del producto.
2. Se identifica el porcentaje de impuesto aplicable.
3. Se calcula el valor del impuesto.
4. Se suma el impuesto al valor base para obtener el precio final.

### Fórmulas utilizadas

Impuesto = Valor × Porcentaje_de_Impuesto
Precio_Final = Valor + Impuesto

Este procedimiento se repite para cada producto registrado.

---

## Salidas

| Salida | Descripción |
|------|-------------|
| Precio Final | Valor total del producto después de aplicar el impuesto |
| Resultado Excel | Valor calculado automáticamente dentro del archivo |

En los casos analizados, los valores calculados coinciden con los valores esperados, lo que confirma la correcta ejecución del cálculo.

---

# Casos de prueba

El archivo de Excel incluye diferentes escenarios de prueba donde se comparan:

- Resultados esperados
- Resultados calculados automáticamente

Esto permite verificar que las fórmulas y el proceso de cálculo funcionan correctamente.

---

# Institución

**Universidad de Medellín**

Curso: **Código Limpio**
