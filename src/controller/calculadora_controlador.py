import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import psycopg2
import SecretConfig
from src.model.calculadora import CalculadoraAhorro

class ControladorCalculadora:

    @staticmethod
    def ObtenerCursor():
        conexion = psycopg2.connect(
            host=SecretConfig.PGHOST,
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD
        )
        return conexion.cursor()

    @staticmethod
    def CrearTabla():
        cursor = ControladorCalculadora.ObtenerCursor()
        with open("sql/crear_calculadora.sql", "r") as file:
            cursor.execute(file.read())
        cursor.connection.commit()

    @staticmethod
    def EliminarTabla():
        cursor = ControladorCalculadora.ObtenerCursor()
        with open("sql/eliminar_calculadora.sql", "r") as file:
            cursor.execute(file.read())
        cursor.connection.commit()

    @staticmethod
    def InsertarCalculadora(calc: CalculadoraAhorro):
        cursor = ControladorCalculadora.ObtenerCursor()
        cursor.execute("""
            INSERT INTO calculadora_ahorro (
                id_usuario, monto_mensual, meses, tasa_interes, total_ahorrado
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            calc.id_usuario,
            calc.monto_mensual,
            calc.meses,
            calc.tasa_interes,
            calc.total_ahorrado
        ))
        cursor.connection.commit()

    @staticmethod
    def BuscarCalculadoraPorUsuario(id_usuario: int):
        cursor = ControladorCalculadora.ObtenerCursor()
        cursor.execute("""
            SELECT id_usuario, monto_mensual, meses, tasa_interes, total_ahorrado, fecha_creacion
            FROM calculadora_ahorro
            WHERE id_usuario = %s
        """, (id_usuario,))
        fila = cursor.fetchone()
        if fila:
            return CalculadoraAhorro(*fila)
        return None

# PRUEBAS PARA CALCULADORA

# Limpiar y crear tabla
ControladorCalculadora.EliminarTabla()
ControladorCalculadora.CrearTabla()

# 1. Insertar calculadora 1
calc1 = CalculadoraAhorro(11111111, 1000.0, 12, 0.05, 12682.0)
ControladorCalculadora.InsertarCalculadora(calc1)
resultado = ControladorCalculadora.BuscarCalculadoraPorUsuario(11111111)
assert resultado is not None and resultado.monto_mensual == 1000.0
print("✔ Inserción 1 correcta - Calculadora Laura")

# 2. Insertar calculadora 2
calc2 = CalculadoraAhorro(22222222, 2000.0, 24, 0.06, 52898.0)
ControladorCalculadora.InsertarCalculadora(calc2)
resultado = ControladorCalculadora.BuscarCalculadoraPorUsuario(22222222)
assert resultado is not None and resultado.meses == 24
print("✔ Inserción 2 correcta - Calculadora Pedro")

# 3. Insertar calculadora 3
calc3 = CalculadoraAhorro(33333333, 1500.0, 18, 0.04, 28650.0)
ControladorCalculadora.InsertarCalculadora(calc3)
resultado = ControladorCalculadora.BuscarCalculadoraPorUsuario(33333333)
assert resultado is not None and resultado.tasa_interes == 0.04
print("✔ Inserción 3 correcta - Calculadora Sofía")

# 4. Modificar calculadora 1
ControladorCalculadora.EliminarTabla()
ControladorCalculadora.CrearTabla()
calc_mod1 = CalculadoraAhorro(11111111, 1200.0, 12, 0.05, 15218.4)
ControladorCalculadora.InsertarCalculadora(calc_mod1)
resultado = ControladorCalculadora.BuscarCalculadoraPorUsuario(11111111)
assert resultado is not None and resultado.monto_mensual == 1200.0
print("✔ Modificación 1 correcta - Calculadora Laura")

# 5. Modificar calculadora 2
ControladorCalculadora.EliminarTabla()
ControladorCalculadora.CrearTabla()
calc_mod2 = CalculadoraAhorro(22222222, 2500.0, 24, 0.06, 66122.5)
ControladorCalculadora.InsertarCalculadora(calc_mod2)
resultado = ControladorCalculadora.BuscarCalculadoraPorUsuario(22222222)
assert resultado is not None and resultado.total_ahorrado == 66122.5
print("✔ Modificación 2 correcta - Calculadora Pedro")

# 6. Modificar calculadora 3
ControladorCalculadora.EliminarTabla()
ControladorCalculadora.CrearTabla()
calc_mod3 = CalculadoraAhorro(33333333, 1500.0, 18, 0.045, 28867.5)
ControladorCalculadora.InsertarCalculadora(calc_mod3)
resultado = ControladorCalculadora.BuscarCalculadoraPorUsuario(33333333)
assert resultado is not None and resultado.tasa_interes == 0.045
print("✔ Modificación 3 correcta - Calculadora Sofía")

# 7. Búsqueda de calculadora 1
ControladorCalculadora.EliminarTabla()
ControladorCalculadora.CrearTabla()
calc_b1 = CalculadoraAhorro(11111111, 1000.0, 12, 0.05, 12682.0)
ControladorCalculadora.InsertarCalculadora(calc_b1)
resultado1 = ControladorCalculadora.BuscarCalculadoraPorUsuario(11111111)
assert resultado1 is not None and resultado1.monto_mensual == 1000.0
print("✔ Búsqueda 1 correcta - Calculadora Laura")

# 8. Búsqueda de calculadora 2
calc_b2 = CalculadoraAhorro(22222222, 2000.0, 24, 0.06, 52898.0)
ControladorCalculadora.InsertarCalculadora(calc_b2)
resultado2 = ControladorCalculadora.BuscarCalculadoraPorUsuario(22222222)
assert resultado2 is not None and resultado2.meses == 24
print("✔ Búsqueda 2 correcta - Calculadora Pedro")

# 9. Búsqueda de calculadora 3
calc_b3 = CalculadoraAhorro(33333333, 1500.0, 18, 0.04, 28650.0)
ControladorCalculadora.InsertarCalculadora(calc_b3)
resultado3 = ControladorCalculadora.BuscarCalculadoraPorUsuario(33333333)
assert resultado3 is not None and resultado3.total_ahorrado == 28650.0
print("✔ Búsqueda 3 correcta - Calculadora Sofía")