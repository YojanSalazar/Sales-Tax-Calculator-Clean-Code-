"""
Capa de Acceso a Datos (Controller) — ORM manual con inyección de dependencias.

Gestiona las operaciones CRUD de la entidad Producto.
Usa PostgreSQL real mediante BaseDatosPostgreSQL.
"""

import sys
sys.path.append("src")

from controller.BaseDatos import BaseDatos, BaseDatosPostgreSQL
from model.Producto import Producto
from model.Exceptions_nuevo import ErrorProductoNoEncontrado, ErrorProductoYaExiste


# ── Variable global para la BD (inyectable) ──────────────────────────────────

_bd = None


def configurar_bd(base_datos: BaseDatos) -> None:
    """Inyecta la implementación de BD (real o mock)."""
    global _bd
    _bd = base_datos


def obtener_bd() -> BaseDatos:
    """Retorna la BD inyectada, o crea una con SecretConfig por defecto."""
    global _bd
    if _bd is None:
        import SecretConfig as config
        _bd = BaseDatosPostgreSQL({
            "database": config.PGDATABASE,
            "user":     config.PGUSER,
            "password": config.PGPASSWORD,
            "host":     config.PGHOST,
            "port":     config.PGPORT,
        })
    return _bd


def usar_bd_real(config_dict: dict) -> None:
    """Configura para usar PostgreSQL real."""
    configurar_bd(BaseDatosPostgreSQL(config_dict))


# ── DDL ─────────────────────────────────────────────────────────────────────

def crear_tabla():
    """
    Crea la tabla 'productos' si no existe.
    Lee el script DDL desde sql/crear-productos.sql.
    """
    try:
        with open("sql/crear-productos.sql", "r", encoding="utf-8") as archivo:
            sql = archivo.read()
        obtener_bd().ejecutar(sql)
    except FileNotFoundError:
        # Si no existe el archivo SQL, crear tabla manualmente
        sql = """
        CREATE TABLE IF NOT EXISTS productos (
            nombre              VARCHAR(100)   PRIMARY KEY,
            tipo_impuesto       VARCHAR(10)    NOT NULL,
            porcentaje_impuesto NUMERIC(5,4)   NOT NULL DEFAULT 0,
            grado_alcohol       NUMERIC(5,2)   NOT NULL DEFAULT 0,
            volumen_ml          INTEGER        NOT NULL DEFAULT 0
        );
        """
        obtener_bd().ejecutar(sql)


def eliminar_tabla():
    """Elimina (DROP) la tabla productos por completo."""
    obtener_bd().ejecutar("DROP TABLE IF EXISTS productos;")


def borrar_filas():
    """
    Borra todas las filas de la tabla (DELETE).

    ⚠ ATENCIÓN: No usar en producción.
    """
    obtener_bd().ejecutar("DELETE FROM productos;")


# ── CREATE ───────────────────────────────────────────────────────────────────

def insertar(producto: Producto):
    """
    Inserta un nuevo Producto en la base de datos.

    Lanza:
        ErrorProductoYaExiste si ya existe un producto con ese nombre.
    """
    try:
        obtener_bd().ejecutar(
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
    except Exception as e:
        if "ya existe" in str(e).lower() or "unique" in str(e).lower() or "duplicate" in str(e).lower():
            raise ErrorProductoYaExiste(producto.nombre)
        raise Exception(f"No fue posible insertar el producto '{producto.nombre}': {e}")


# ── READ ─────────────────────────────────────────────────────────────────────

def buscar_por_nombre(nombre: str) -> Producto:
    """
    Busca un producto por su nombre (clave primaria).

    Lanza:
        ErrorProductoNoEncontrado si no existe.
    """
    fila = obtener_bd().consultar_uno(
        """
        SELECT nombre, tipo_impuesto, porcentaje_impuesto, grado_alcohol, volumen_ml
        FROM productos
        WHERE nombre = %s;
        """,
        (nombre,),
    )

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
    filas = obtener_bd().consultar_todos(
        """
        SELECT nombre, tipo_impuesto, porcentaje_impuesto, grado_alcohol, volumen_ml
        FROM productos
        ORDER BY nombre;
        """
    )

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
    obtener_bd().ejecutar(
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
    if obtener_bd().obtener_filas_afectadas() == 0:
        raise ErrorProductoNoEncontrado(producto.nombre)


# ── DELETE ───────────────────────────────────────────────────────────────────

def borrar(nombre: str):
    """
    Elimina el producto con el nombre indicado.

    Lanza:
        ErrorProductoNoEncontrado si el nombre no existe.
    """
    obtener_bd().ejecutar(
        "DELETE FROM productos WHERE nombre = %s;",
        (nombre,),
    )
    if obtener_bd().obtener_filas_afectadas() == 0:
        raise ErrorProductoNoEncontrado(nombre)
