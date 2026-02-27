Calculadora de Impuestos de venta

## Creadores
- **Luis Alejandro Correa**
- **Yohan Salazar**

---

## Descripción del Proyecto

Este proyecto consiste en un archivo de **Excel** que simula el proceso de **cálculo del precio final de productos**, aplicando distintos tipos de impuestos (IVA) según corresponda.

El propósito principal es demostrar, de manera clara y estructurada, cómo a partir de unos **datos de entrada**, se ejecuta un **proceso de cálculo**, generando una **salida correcta y verificable**.  
El archivo incluye **casos normales de prueba**, donde se compara el resultado esperado con el resultado calculado en Excel.

---

## Entradas (Inputs)

Las entradas del sistema son los datos iniciales necesarios para realizar los cálculos:

- **Producto**  
  Nombre del producto a evaluar.  
  Ejemplos: `Shampoo`, `Dolex`, `Barra de Chocolate`.

- **Valor**  
  Precio base del producto sin impuestos aplicados.

- **Impuestos**  
  Porcentaje de IVA aplicado al producto.  
  Ejemplos:
  - IVA del **19%**
  - IVA del **5%**
  - INC del 10%
  - Impuesto a licores
  - Impuesto bolsa
Estas entradas representan la información proporcionada por el usuario para iniciar el proceso.

---

## Proceso

El proceso se basa en el cálculo del impuesto y el precio final del producto:

1. Se toma el **valor base** del producto.
2. Se identifica el **porcentaje de IVA** correspondiente.
3. Se calcula el impuesto usando la fórmula:


Este procedimiento se repite para cada producto registrado en el archivo de Excel.

---

## Salidas (Outputs)

Las salidas corresponden a los resultados obtenidos tras ejecutar el proceso:

- **Salida**  
Precio final del producto luego de aplicar el impuesto.

- **Excel**  
Valor calculado automáticamente dentro del archivo como verificación.

En los casos analizados, los valores de **Salida** y **Excel** coinciden, lo que confirma la correcta ejecución del proceso.


