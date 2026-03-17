# Calculadora de Impuestos de Venta

## Creadores
- Luis Alejandro Correa  
- Yohan Salazar  

---

## ¿Qué es y para qué es?

Este proyecto consiste en una **calculadora de impuestos de venta**, implementada inicialmente en un archivo de **Excel**, que simula el proceso de cálculo del precio final de productos aplicando distintos tipos de impuestos.

El objetivo principal del proyecto es **demostrar de forma clara el flujo de procesamiento de datos en un sistema**, partiendo de **entradas (inputs)**, pasando por un **proceso de cálculo**, y generando **salidas (outputs)** verificables.

El archivo incluye **casos de prueba**, donde se comparan los resultados esperados con los resultados calculados automáticamente en Excel.

---

## ¿Cómo lo hago funcionar?

### Prerrequisitos

Antes de ejecutar el proyecto se debe contar con:

- Microsoft Excel o cualquier software compatible con archivos `.xlsx`
- Descargar o clonar este repositorio en su computador

### Ejecución

1. Ubicarse en la carpeta raíz del proyecto.
2. Abrir el archivo de Excel incluido en el proyecto.
3. Ingresar los datos solicitados en las columnas correspondientes.
4. El sistema calculará automáticamente los impuestos y el precio final del producto.

---

## ¿Cómo está hecho?

El proyecto está diseñado siguiendo un **modelo básico de procesamiento de información**, donde se identifican tres componentes principales: **entradas, proceso y salidas**.

### Entradas (Inputs)

Las entradas del sistema corresponden a los datos iniciales necesarios para realizar los cálculos:

- **Producto**  
  Nombre del producto a evaluar.  
  Ejemplos: Shampoo, Dolex, Barra de Chocolate.

- **Valor**  
  Precio base del producto sin impuestos aplicados.

- **Impuestos**  
  Porcentaje de impuesto aplicado al producto. Algunos ejemplos incluyen:

  - IVA del 19%
  - IVA del 5%
  - INC del 10%
  - Impuesto a licores
  - Impuesto a bolsas

Estas entradas representan la información proporcionada por el usuario para iniciar el proceso.

---

### Proceso

El proceso consiste en calcular el valor del impuesto y el precio final del producto.

Pasos del cálculo:

1. Se toma el **valor base del producto**.
2. Se identifica el **porcentaje de impuesto aplicable**.
3. Se calcula el **valor del impuesto**.
4. Se suma el impuesto al valor base para obtener el **precio final**.

**Fórmulas utilizadas:**



Impuesto = Valor × Porcentaje_de_Impuesto
Precio_Final = Valor + Impuesto


Este procedimiento se repite para cada producto registrado en el archivo.

---

### Salidas (Outputs)

Las salidas corresponden a los resultados generados después de ejecutar el proceso.

- **Salida**  
  Precio final del producto luego de aplicar el impuesto.

- **Excel**  
  Valor calculado automáticamente dentro del archivo como verificación.

En los casos analizados, los valores de **Salida** y **Excel** coinciden, lo que confirma la correcta ejecución del cálculo.

---

## Uso

El archivo permite simular distintos escenarios de cálculo de impuestos cambiando los valores de entrada.

Esto facilita:

- Verificar cálculos de impuestos
- Comparar resultados esperados
- Analizar cómo cambia el precio final según el tipo de impuesto aplicad
