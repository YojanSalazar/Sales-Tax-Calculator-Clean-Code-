"""
Capa de abstracción para la base de datos.

Permite inyectar diferentes implementaciones:
- BaseDatosPostgreSQL: conexión real a PostgreSQL
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Any


class BaseDatos(ABC):
    """Interfaz abstracta para operaciones de BD."""

    @abstractmethod
    def ejecutar(self, sql: str, parametros: tuple = ()) -> None:
        """Ejecuta un comando SQL (CREATE, INSERT, UPDATE, DELETE)."""

    @abstractmethod
    def consultar_uno(self, sql: str, parametros: tuple = ()) -> Tuple:
        """Ejecuta SELECT y retorna una fila (o None)."""

    @abstractmethod
    def consultar_todos(self, sql: str, parametros: tuple = ()) -> List[Tuple]:
        """Ejecuta SELECT y retorna todas las filas."""

    @abstractmethod
    def obtener_filas_afectadas(self) -> int:
        """Retorna cuántas filas fueron afectadas por último comando."""

    @abstractmethod
    def cerrar(self) -> None:
        """Cierra la conexión."""


class BaseDatosPostgreSQL(BaseDatos):
    """Implementación real con PostgreSQL."""

    def __init__(self, config_dict: dict):
        """
        config_dict contiene:
            - database, user, password, host, port
        """
        import psycopg2
        self.config = config_dict
        self.conexion = psycopg2.connect(**config_dict)
        self.cursor = self.conexion.cursor()

    def ejecutar(self, sql: str, parametros: tuple = ()) -> None:
        try:
            self.cursor.execute(sql, parametros)
            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise e

    def consultar_uno(self, sql: str, parametros: tuple = ()) -> Tuple:
        self.cursor.execute(sql, parametros)
        return self.cursor.fetchone()

    def consultar_todos(self, sql: str, parametros: tuple = ()) -> List[Tuple]:
        self.cursor.execute(sql, parametros)
        return self.cursor.fetchall()

    def obtener_filas_afectadas(self) -> int:
        return self.cursor.rowcount

    def cerrar(self) -> None:
        self.cursor.close()
        self.conexion.close()

class BaseDatosSQLite(BaseDatos):
    """Implementación local con SQLite para que funcione out-of-the-box."""

    def __init__(self, ruta_bd: str = "productos.db"):
        import sqlite3
        self.conexion = sqlite3.connect(ruta_bd)
        self.cursor = self.conexion.cursor()

    def ejecutar(self, sql: str, parametros: tuple = ()) -> None:
        # SQLite uses ? instead of %s for placeholders
        sql = sql.replace("%s", "?")
        try:
            self.cursor.execute(sql, parametros)
            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise e

    def consultar_uno(self, sql: str, parametros: tuple = ()) -> Tuple:
        sql = sql.replace("%s", "?")
        self.cursor.execute(sql, parametros)
        return self.cursor.fetchone()

    def consultar_todos(self, sql: str, parametros: tuple = ()) -> List[Tuple]:
        sql = sql.replace("%s", "?")
        self.cursor.execute(sql, parametros)
        return self.cursor.fetchall()

    def obtener_filas_afectadas(self) -> int:
        return self.cursor.rowcount

    def cerrar(self) -> None:
        self.cursor.close()
        self.conexion.close()
