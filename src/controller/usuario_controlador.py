import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import psycopg2
import SecretConfig
from src.model.usuar import *

class ControladorUsuarios:
    """
    Controlador encargado de gestionar los usuarios
    """

    def ObtenerCursor():
        """
        Crea la conexión y retorna un cursor
        """
        conexion = psycopg2.connect(
            host=SecretConfig.PGHOST,
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD
        )
        return conexion.cursor()

    @staticmethod
    def CrearTabla():
        """
        Crea la tabla de usuarios desde archivo SQL
        """
        cursor = ControladorUsuarios.ObtenerCursor()
        with open("sql/crear_usuarios.sql", "r") as file:
            cursor.execute(file.read())
        cursor.connection.commit()

    @staticmethod
    def EliminarTabla():
        """
        Elimina la tabla de usuarios desde archivo SQL
        """
        cursor = ControladorUsuarios.ObtenerCursor()
        with open("sql/eliminar_usuarios.sql", "r") as file:
            cursor.execute(file.read())
        cursor.connection.commit()

    @staticmethod
    def InsertarUsuario(usuario: Usuario):
        """
        Inserta o actualiza un objeto Usuario en la base de datos
        """
        cursor = ControladorUsuarios.ObtenerCursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (
                    nombre, apellido, documento_identidad, correo, telefono
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (documento_identidad) DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    apellido = EXCLUDED.apellido,
                    correo = EXCLUDED.correo,
                    telefono = EXCLUDED.telefono
            """, (
                usuario.nombre,
                usuario.apellido,
                usuario.documento_identidad,
                usuario.correo,
                usuario.telefono
            ))
            cursor.connection.commit()
            print(f"Inserted/Updated user with documento_identidad: {usuario.documento_identidad}")
        except Exception as e:
            print(f"Error inserting/updating user: {e}")
            cursor.connection.rollback()
            raise
        finally:
            cursor.close()

    @staticmethod
    def EliminarUsuarioPorDocumento(documento_identidad: int):
        """
        Elimina un usuario de la base de datos según su documento de identidad.
        """
        cursor = ControladorUsuarios.ObtenerCursor()
        cursor.execute("""
            DELETE FROM usuarios WHERE documento_identidad = %s
        """, (documento_identidad,))
        cursor.connection.commit()

    @staticmethod
    def BuscarUsuarioPorDocumento(documento_identidad: int):
        """
        Busca un usuario por su documento de identidad
        """
        cursor = ControladorUsuarios.ObtenerCursor()
        cursor.execute("""
            SELECT nombre, apellido, documento_identidad, correo, telefono
            FROM usuarios
            WHERE documento_identidad = %s
        """, (documento_identidad,))
        fila = cursor.fetchone()
        cursor.close()
        if fila:
            return Usuario(*fila)
        return None

# PRUEBAS PARA USUARIOS

# Limpiar y crear tabla
ControladorUsuarios.EliminarTabla()
ControladorUsuarios.CrearTabla()

# 1. Insertar usuario 1
usuario1 = Usuario("Juan", "Pérez", 12345678, "juan@example.com", "123456789")
ControladorUsuarios.InsertarUsuario(usuario1)
resultado = ControladorUsuarios.BuscarUsuarioPorDocumento(12345678)
assert resultado is not None and resultado.nombre == "Juan"
print("✔ Inserción 1 correcta")

# 2. Insertar usuario 2
usuario2 = Usuario("Ana", "Gómez", 87654321, "ana@example.com", "321321321")
ControladorUsuarios.InsertarUsuario(usuario2)
resultado = ControladorUsuarios.BuscarUsuarioPorDocumento(87654321)
assert resultado is not None and resultado.apellido == "Gómez"
print("✔ Inserción 2 correcta")

# 3. Insertar usuario 3
usuario3 = Usuario("Luis", "Martínez", 11223344, "luis@example.com", "555555555")
ControladorUsuarios.InsertarUsuario(usuario3)
resultado = ControladorUsuarios.BuscarUsuarioPorDocumento(11223344)
assert resultado is not None and resultado.correo == "luis@example.com"
print("✔ Inserción 3 correcta")

# 4. Modificar usuario 1
usuario_mod1 = Usuario("Juan", "Pérez", 12345678, "juan.nuevo@example.com", "999999999")
ControladorUsuarios.InsertarUsuario(usuario_mod1)
resultado = ControladorUsuarios.BuscarUsuarioPorDocumento(12345678)
assert resultado is not None and resultado.correo == "juan.nuevo@example.com"
print("✔ Modificación 1 correcta")

# 5. Modificar usuario 2
usuario_mod2 = Usuario("Ana", "Gómez", 87654321, "ana.nueva@example.com", "888888888")
ControladorUsuarios.InsertarUsuario(usuario_mod2)
resultado = ControladorUsuarios.BuscarUsuarioPorDocumento(87654321)
assert resultado is not None and resultado.telefono == "888888888"
print("✔ Modificación 2 correcta")

# 6. Modificar usuario 3
usuario_mod3 = Usuario("Luis", "Martínez", 11223344, "luis.nuevo@example.com", "666666666")
ControladorUsuarios.InsertarUsuario(usuario_mod3)
resultado = ControladorUsuarios.BuscarUsuarioPorDocumento(11223344)
assert resultado is not None and resultado.correo == "luis.nuevo@example.com"
print("✔ Modificación 3 correcta")

# 7. Búsqueda de usuario 1
usuario_b1 = Usuario("Laura", "Martínez", 11111111, "laura@example.com", "300100200")
ControladorUsuarios.InsertarUsuario(usuario_b1)
resultado1 = ControladorUsuarios.BuscarUsuarioPorDocumento(11111111)
assert resultado1 is not None and resultado1.nombre == "Laura"
print("✔ Búsqueda 1 correcta - Laura")

# 8. Búsqueda de usuario 2
usuario_b2 = Usuario("Pedro", "López", 22222222, "pedro@example.com", "300200300")
ControladorUsuarios.InsertarUsuario(usuario_b2)
resultado2 = ControladorUsuarios.BuscarUsuarioPorDocumento(22222222)
assert resultado2 is not None and resultado2.apellido == "López"
print("✔ Búsqueda 2 correcta - Pedro")

# 9. Búsqueda de usuario 3
usuario_b3 = Usuario("Sofía", "Castro", 33333333, "sofia@example.com", "300300400")
ControladorUsuarios.InsertarUsuario(usuario_b3)
resultado3 = ControladorUsuarios.BuscarUsuarioPorDocumento(33333333)
assert resultado3 is not None and resultado3.correo == "sofia@example.com"
print("✔ Búsqueda 3 correcta - Sofía")