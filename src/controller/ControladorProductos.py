"""
Capa de Acceso a Datos (Controller) — ORM manual con psycopg2.

Gestiona las operaciones CRUD de la entidad Producto
contra una base de datos PostgreSQL.
"""

import sys
sys.path.append("src")
import SecretConfig as SecretConfig # Archivo con credenciales de DB (no subir a GitHub)
import psycopg2
from model.Producto import Producto
from model.Exceptions_nuevo import ErrorProductoNoEncontrado, ErrorProductoYaExiste


# ── Conexión ────────────────────────────────────────────────────────────────

def obtener_cursor():
    """
    Abre una conexión a PostgreSQL y retorna el cursor asociado.
    Las credenciales se leen desde SecretConfig.py.
    """
    conexion = psycopg2.connect(
        database=SecretConfig.PGDATABASE,
        user=SecretConfig.PGUSER,
        password=SecretConfig.PGPASSWORD,
        host=SecretConfig.PGHOST,
        port=SecretConfig.PGPORT,
    )
    return conexion.cursor()


# ── DDL ─────────────────────────────────────────────────────────────────────

def crear_tabla():
    """
    Crea la tabla 'productos' si no existe.
    Lee el script DDL desde sql/crear-productos.sql.
    """
    with open("sql/crear-productos.sql", "r", encoding="utf-8") as archivo:
        sql = archivo.read()

    cursor = obtener_cursor()
    try:
        cursor.execute(sql)
        cursor.connection.commit()
    except Exception:
        cursor.connection.rollback()


def eliminar_tabla():
    """Elimina (DROP) la tabla productos por completo."""
    cursor = obtener_cursor()
    cursor.execute("DROP TABLE IF EXISTS productos;")
    cursor.connection.commit()


def borrar_filas():
    """
    Borra todas las filas de la tabla (DELETE).

    ⚠ ATENCIÓN: No usar en producción.
    """
    cursor = obtener_cursor()
    cursor.execute("DELETE FROM productos;")
    cursor.connection.commit()


# ── CREATE ───────────────────────────────────────────────────────────────────

def insertar(producto: Producto):
    """
    Inserta un nuevo Producto en la base de datos.

    Lanza:
        ErrorProductoYaExiste si ya existe un producto con ese nombre.
    """
    cursor = obtener_cursor()
    try:
        cursor.execute(
            """
            INSERT INTO productos
                (nombre, tipo_impuesto, porcentaje_impuesto, grado_alcohol, volumen_ml)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                producto.nombre,
                producto.tipo_impuesto,
                producto.porcentaje_impuesto,
                producto.grado_alcohol,
                producto.volumen_ml,
            ),
        )
        cursor.connection.commit()
    except psycopg2.errors.UniqueViolation:
        cursor.connection.rollback()
        raise ErrorProductoYaExiste(producto.nombre)
    except Exception as e:
        cursor.connection.rollback()
        raise Exception(f"No fue posible insertar el producto '{producto.nombre}': {e}")


# ── READ ─────────────────────────────────────────────────────────────────────

def buscar_por_nombre(nombre: str) -> Producto:
    """
    Busca un producto por su nombre (clave primaria).

    Lanza:
        ErrorProductoNoEncontrado si no existe.
    """
    cursor = obtener_cursor()
    cursor.execute(
        """
        SELECT nombre, tipo_impuesto, porcentaje_impuesto, grado_alcohol, volumen_ml
        FROM productos
        WHERE nombre = %s;
        """,
        (nombre,),
    )
    fila = cursor.fetchone()

    if fila is None:
        raise ErrorProductoNoEncontrado(nombre)

    return Producto(
        nombre=fila[0],
        tipo_impuesto=fila[1],
        porcentaje_impuesto=float(fila[2]),
        grado_alcohol=float(fila[3]),
        volumen_ml=int(fila[4]),
    )


def buscar_todos() -> list:
    """Retorna una lista con todos los Producto registrados."""
    cursor = obtener_cursor()
    cursor.execute(
        """
        SELECT nombre, tipo_impuesto, porcentaje_impuesto, grado_alcohol, volumen_ml
        FROM productos
        ORDER BY nombre;
        """
    )
    filas = cursor.fetchall()

    return [
        Producto(
            nombre=f[0],
            tipo_impuesto=f[1],
            porcentaje_impuesto=float(f[2]),
            grado_alcohol=float(f[3]),
            volumen_ml=int(f[4]),
        )
        for f in filas
    ]


# ── UPDATE ───────────────────────────────────────────────────────────────────

def actualizar(producto: Producto):
    """
    Actualiza los datos de un Producto existente.
    El nombre es la clave primaria y no se modifica.

    Lanza:
        ErrorProductoNoEncontrado si el nombre no existe.
    """
    cursor = obtener_cursor()
    cursor.execute(
        """
        UPDATE productos
        SET
            tipo_impuesto       = %s,
            porcentaje_impuesto = %s,
            grado_alcohol       = %s,
            volumen_ml          = %s
        WHERE nombre = %s;
        """,
        (
            producto.tipo_impuesto,
            producto.porcentaje_impuesto,
            producto.grado_alcohol,
            producto.volumen_ml,
            producto.nombre,
        ),
    )
    if cursor.rowcount == 0:
        cursor.connection.rollback()
        raise ErrorProductoNoEncontrado(producto.nombre)

    cursor.connection.commit()


# ── DELETE ───────────────────────────────────────────────────────────────────

def borrar(nombre: str):
    """
    Elimina el producto con el nombre indicado.

    Lanza:
        ErrorProductoNoEncontrado si el nombre no existe.
    """
    cursor = obtener_cursor()
    cursor.execute(
        "DELETE FROM productos WHERE nombre = %s;",
        (nombre,),
    )
    if cursor.rowcount == 0:
        cursor.connection.rollback()
        raise ErrorProductoNoEncontrado(nombre)

    cursor.connection.commit()
