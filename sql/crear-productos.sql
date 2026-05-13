-- ============================================================
-- Script DDL: crea la tabla productos
-- Ejecutar una vez antes de iniciar la aplicación.
--
-- Uso desde terminal:
--   psql -U <usuario> -d <base_de_datos> -f sql/crear-productos.sql
-- ============================================================

CREATE TABLE IF NOT EXISTS productos (
    nombre              VARCHAR(100)   PRIMARY KEY,
    tipo_impuesto       VARCHAR(10)    NOT NULL CHECK (tipo_impuesto IN ('IVA','INC','LICOR','EXENTO')),
    porcentaje_impuesto NUMERIC(5,4)   NOT NULL DEFAULT 0,
    grado_alcohol       NUMERIC(5,2)   NOT NULL DEFAULT 0,
    volumen_ml          INTEGER        NOT NULL DEFAULT 0
);
