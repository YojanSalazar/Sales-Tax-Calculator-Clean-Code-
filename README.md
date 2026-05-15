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

La **Calculadora de Impuestos de Venta** permite calcular el precio final de un producto aplicando distintos tipos de impuestos presentes en el sistema tributario colombiano. Adicionalmente, gestiona un catálogo de productos en **PostgreSQL** usando el patrón **ORM manual** con operaciones CRUD completas (Crear, Leer, Actualizar, Eliminar).

---

# Objetivo
Desarrollar una herramienta clara y estructurada que permita comprender el proceso de cálculo de impuestos de venta, aplicando los principios de **Código Limpio** y mostrando de forma clara el flujo de información dentro de un sistema.

---

# Funcionalidades principales

- **CRUD completo** de productos en PostgreSQL (INSERT, SELECT, UPDATE, DELETE)
- Cálculo del precio final de productos aplicando distintos tipos de impuestos
- Validación de datos de entrada
- Interfaz de consola para gestionar productos
- Interfaz gráfica desarrollada con **Kivy**
- 12 casos de prueba de integración con BD real

---

# Configuración de la Base de Datos

## 1. Instalar PostgreSQL

Descargue e instale PostgreSQL desde [postgresql.org](https://www.postgresql.org/download/) o use Docker:

```bash
# Opción con Docker
docker run --name postgres-impuestos -e POSTGRES_PASSWORD=mi_clave -p 5432:5432 -d postgres
```

## 2. Crear la base de datos

Conéctese a PostgreSQL y cree la base de datos:

```bash
psql -U postgres
```

```sql
CREATE DATABASE calculadora_impuestos;
```

## 3. Crear la tabla productos

Desde la carpeta raíz del proyecto, ejecute el script DDL:

```bash
psql -U postgres -d calculadora_impuestos -f sql/crear-productos.sql
```

O ejecute manualmente en `psql`:

```sql
\c calculadora_impuestos

CREATE TABLE IF NOT EXISTS productos (
    nombre              VARCHAR(100)   PRIMARY KEY,
    tipo_impuesto       VARCHAR(10)    NOT NULL CHECK (tipo_impuesto IN ('IVA','INC','LICOR','EXENTO')),
    porcentaje_impuesto NUMERIC(5,4)   NOT NULL DEFAULT 0,
    grado_alcohol       NUMERIC(5,2)   NOT NULL DEFAULT 0,
    volumen_ml          INTEGER        NOT NULL DEFAULT 0
);
```

## 4. Configurar la conexión (`SecretConfig.py`)

El archivo `src/SecretConfig.py` contiene los datos de conexión. **Nunca suba este archivo al repositorio** (ya está en `.gitignore`).

Edite `src/SecretConfig.py` con sus datos reales:

```python
PGDATABASE = "calculadora_impuestos"   # nombre de su base de datos
PGUSER     = "postgres"                # su usuario de PostgreSQL
PGPASSWORD = "mi_clave"               # su contraseña
PGHOST     = "localhost"                # servidor (localhost para local)
PGPORT     = 5432                       # puerto (5432 por defecto)
```

## 5. Instalar dependencias de Python

```bash
pip install psycopg2-binary kivy
```

---

# Ejecución

## Prerrequisitos
- **Python 3.8 o superior**
- **PostgreSQL** instalado y ejecutándose
- Base de datos y tabla creadas (ver sección anterior)
- `SecretConfig.py` configurado con datos reales
- Dependencias instaladas (`psycopg2-binary`, `kivy`)

## Ejecución del proyecto

### Opción 1 — Consola CRUD (Gestión de productos en BD)

1. Ubicarse en la carpeta raíz del proyecto.
2. Ejecutar:

```bash
python src/view/consola.py
```

Esto abrirá un menú interactivo con opciones para:
- **Insertar** un nuevo producto
- **Buscar** un producto por nombre
- **Listar** todos los productos
- **Actualizar** los datos de un producto
- **Eliminar** un producto
- **Calcular** el precio final con impuestos

### Opción 2 — Interfaz gráfica (GUI)

```bash
python sales_tax.py
```

### Opción 3 — Excel

Abrir el archivo de Excel incluido en el repositorio e ingresar los datos en las columnas correspondientes.

---

## Ejecución de pruebas

Los tests de integración se conectan a PostgreSQL real. Asegúrese de que la BD esté activa y `SecretConfig.py` esté configurado.

Desde la carpeta raíz del proyecto:

```bash
python -m unittest src.Tests.test_controlador_productos -v
```

Los 12 tests cubren:
- **INSERT**: 3 casos normales + 1 caso de error (duplicado)
- **SELECT**: 3 casos normales + 1 caso de error (no encontrado)
- **UPDATE**: 3 casos normales + 1 caso de error (no encontrado)
- **DELETE**: 1 caso normal + 1 caso de error (no encontrado)

---

# Arquitectura del proyecto

```
├── sql/
│   └── crear-productos.sql        # Script DDL para crear la tabla
├── src/
│   ├── SecretConfig.py            # Configuración de conexión (NO subir al repo)
│   ├── model/
│   │   ├── Producto.py            # Clase Model del producto
│   │   ├── Exceptions_nuevo.py    # Excepciones personalizadas
│   │   └── app_logic_nuevo.py     # Lógica de cálculo de impuestos
│   ├── controller/
│   │   ├── BaseDatos.py           # Capa de abstracción de BD (ORM)
│   │   └── ControladorProductos.py # Controlador CRUD
│   ├── view/
│   │   ├── consola.py             # Interfaz de consola (CRUD)
│   │   ├── gui_sales_tax.py       # Interfaz gráfica (Kivy)
│   │   └── logica_consola.py      # Consola legacy (solo cálculos)
│   └── Tests/
│       └── test_controlador_productos.py  # Tests de integración
├── README.md
└── main.py
```

---

# Modelo ORM

El proyecto implementa un ORM manual con las siguientes capas:

| Capa | Clase | Responsabilidad |
|------|-------|----------------|
| **Model** | `Producto` | Representa un producto con sus atributos |
| **Controller** | `ControladorProductos` | Operaciones CRUD (INSERT, SELECT, UPDATE, DELETE) |
| **Acceso a datos** | `BaseDatos` / `BaseDatosPostgreSQL` | Abstracción de la BD con inyección de dependencias |
| **View** | `consola.py` | Interfaz de usuario en consola |

---

# Institución

**Universidad de Medellín**

Curso: **Código Limpio**
