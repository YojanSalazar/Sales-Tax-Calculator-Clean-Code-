import unittest
import sys
from datetime import date
 
sys.path.append("src")
 
import controller.ControladorProductos as UsuarioDAO
from model.app_logic import Usuario
 
 
class TestUsuarioDAO(unittest.TestCase):
 
    @classmethod
    def setUpClass(cls):
        # Fixture: crea las tablas y limpia antes de todos los tests
        UsuarioDAO.CrearTabla()
        UsuarioDAO.BorrarFilas()
 
    def tearDown(self):
        # Limpia después de cada test para evitar conflictos de clave primaria
        UsuarioDAO.BorrarFilas()
 
 
    # ── INSERTAR ──────────────────────────────────────────────────────────────
 
    def test_insertar_normal1(self):
    # ENTRADAS
    # Verifica que un usuario básico se inserte correctamente
    # en la base de datos y pueda recuperarse por cédula.
 
        usuario = Usuario(
            cedula="1001",
            nombre="Carlos",
            apellido="López",
            correo="carlos@mail.com",
            direccion="Calle 1 # 2-3",
            telefono="3001234567",
            codigo_departamento="05",
            codigo_municipio="001",
        )
 
        UsuarioDAO.Insertar(usuario)
 
        recuperado = UsuarioDAO.BuscarPorCedula("1001")
 
        self.assertEqual(recuperado.cedula, "1001")
        self.assertEqual(recuperado.nombre, "Carlos")
        self.assertEqual(recuperado.apellido, "López")
 
    def test_insertar_normal2(self):
    # ENTRADAS
    # Verifica que un usuario con familiares se inserte
    # correctamente y los familiares se recuperen completos.
 
        usuario = Usuario(
            cedula="1002",
            nombre="María",
            apellido="Pérez",
            correo="maria@mail.com",
            direccion="Carrera 5 # 10-20",
            telefono="3109876543",
            codigo_departamento="05",
            codigo_municipio="002",
        )
        usuario.agregarFamiliar("Hijo", "Lucho", "Pérez", date(2010, 5, 15))
        usuario.agregarFamiliar("Esposo", "Jorge", "Ruiz", date(1980, 3, 22))
 
        UsuarioDAO.Insertar(usuario)
 
        recuperado = UsuarioDAO.BuscarPorCedula("1002")
 
        self.assertEqual(recuperado.nombre, "María")
        self.assertEqual(len(recuperado.familiares), 2)
 
    def test_insertar_normal3(self):
    # ENTRADAS
    # Verifica que los datos opcionales (correo, teléfono,
    # dirección) se guarden y recuperen correctamente.
 
        usuario = Usuario(
            cedula="1003",
            nombre="Pedro",
            apellido="Martínez",
            correo="pedro@correo.com",
            direccion="Avenida 80 # 45-10",
            telefono="3207654321",
            codigo_departamento="11",
            codigo_municipio="001",
        )
 
        UsuarioDAO.Insertar(usuario)
 
        recuperado = UsuarioDAO.BuscarPorCedula("1003")
 
        self.assertEqual(recuperado.correo, "pedro@correo.com")
        self.assertEqual(recuperado.telefono, "3207654321")
        self.assertEqual(recuperado.direccion, "Avenida 80 # 45-10")
 
    def test_insertar_error_cedula_duplicada(self):
    # ENTRADAS
    # Verifica que el sistema lance una excepción cuando
    # se intenta insertar dos usuarios con la misma cédula.
 
        usuario = Usuario(
            cedula="1004",
            nombre="Ana",
            apellido="García",
            correo="ana@mail.com",
            direccion="Calle 10 # 1-1",
            telefono="3001111111",
            codigo_departamento="05",
            codigo_municipio="001",
        )
 
        UsuarioDAO.Insertar(usuario)
 
        with self.assertRaises(Exception):
            UsuarioDAO.Insertar(usuario)
 
 
    # ── BUSCAR ────────────────────────────────────────────────────────────────
 
    def test_buscar_normal1(self):
    # ENTRADAS
    # Verifica que BuscarPorCedula retorne el usuario correcto
    # con todos sus datos cuando la cédula existe en la BD.
 
        usuario = Usuario(
            cedula="2001",
            nombre="Laura",
            apellido="Gómez",
            correo="laura@mail.com",
            direccion="Calle 50 # 3-3",
            telefono="3112223344",
            codigo_departamento="05",
            codigo_municipio="001",
        )
        UsuarioDAO.Insertar(usuario)
 
        recuperado = UsuarioDAO.BuscarPorCedula("2001")
 
        self.assertEqual(recuperado.nombre, "Laura")
        self.assertEqual(recuperado.apellido, "Gómez")
        self.assertEqual(recuperado.correo, "laura@mail.com")
 
    def test_buscar_normal2(self):
    # ENTRADAS
    # Verifica que BuscarTodos retorne al menos los usuarios
    # previamente insertados en la base de datos.
 
        u1 = Usuario("2002", "Felipe", "Torres", "f@mail.com", "Dir 1", "311", "05", "001")
        u2 = Usuario("2003", "Sandra", "Vargas", "s@mail.com", "Dir 2", "312", "05", "002")
        UsuarioDAO.Insertar(u1)
        UsuarioDAO.Insertar(u2)
 
        lista = UsuarioDAO.BuscarTodos()
        cedulas = [u.cedula for u in lista]
 
        self.assertIn("2002", cedulas)
        self.assertIn("2003", cedulas)
 
    def test_buscar_normal3(self):
    # ENTRADAS
    # Verifica que los familiares de un usuario se recuperen
    # correctamente al buscarlo por cédula.
 
        usuario = Usuario("2004", "Rosa", "Díaz", "rosa@mail.com", "Dir 3", "313", "05", "003")
        usuario.agregarFamiliar("Madre", "Elena", "Díaz", date(1955, 7, 20))
        UsuarioDAO.Insertar(usuario)
 
        recuperado = UsuarioDAO.BuscarPorCedula("2004")
 
        self.assertEqual(len(recuperado.familiares), 1)
        self.assertEqual(recuperado.familiares[0].nombre, "Elena")
        self.assertEqual(recuperado.familiares[0].parentezco, "Madre")
 
    def test_buscar_error_cedula_inexistente(self):
    # ENTRADAS
    # Verifica que el sistema lance ErrorNoEncontrado cuando
    # se busca una cédula que no existe en la base de datos.
 
        with self.assertRaises(UsuarioDAO.ErrorNoEncontrado):
            UsuarioDAO.BuscarPorCedula("9999999")
 
 
    # ── MODIFICAR ─────────────────────────────────────────────────────────────
 
    def test_modificar_normal1(self):
    # ENTRADAS
    # Verifica que el nombre y apellido de un usuario
    # se actualicen correctamente en la base de datos.
 
        usuario = Usuario("3001", "Original", "Apellido", "o@mail.com", "Dir", "300", "05", "001")
        UsuarioDAO.Insertar(usuario)
 
        usuario.nombre = "Modificado"
        usuario.apellido = "NuevoApellido"
        UsuarioDAO.Actualizar(usuario)
 
        actualizado = UsuarioDAO.BuscarPorCedula("3001")
 
        self.assertEqual(actualizado.nombre, "Modificado")
        self.assertEqual(actualizado.apellido, "NuevoApellido")
 
    def test_modificar_normal2(self):
    # ENTRADAS
    # Verifica que el correo y teléfono de un usuario
    # se actualicen correctamente en la base de datos.
 
        usuario = Usuario("3002", "Juan", "Ríos", "viejo@mail.com", "Dir", "300", "05", "001")
        UsuarioDAO.Insertar(usuario)
 
        usuario.correo = "nuevo@correo.com"
        usuario.telefono = "3119998877"
        UsuarioDAO.Actualizar(usuario)
 
        actualizado = UsuarioDAO.BuscarPorCedula("3002")
 
        self.assertEqual(actualizado.correo, "nuevo@correo.com")
        self.assertEqual(actualizado.telefono, "3119998877")
 
    def test_modificar_normal3(self):
    # ENTRADAS
    # Verifica que la dirección y los códigos de departamento
    # y municipio se actualicen correctamente en la base de datos.
 
        usuario = Usuario("3003", "Sofía", "Luna", "sofia@mail.com", "Dir Vieja", "300", "05", "001")
        UsuarioDAO.Insertar(usuario)
 
        usuario.direccion = "Carrera 45 # 80-10"
        usuario.codigo_departamento = "76"
        usuario.codigo_municipio = "520"
        UsuarioDAO.Actualizar(usuario)
 
        actualizado = UsuarioDAO.BuscarPorCedula("3003")
 
        self.assertEqual(actualizado.direccion, "Carrera 45 # 80-10")
        self.assertEqual(actualizado.codigo_departamento, "76")
        self.assertEqual(actualizado.codigo_municipio, "520")
 
 
if __name__ == "__main__":
    unittest.main()