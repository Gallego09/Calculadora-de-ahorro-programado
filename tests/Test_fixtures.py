import pytest
from src.controller.calculadora_controlador import ControladorCalculadora
from src.controller.usuario_controlador import ControladorUsuarios

@pytest.fixture(scope="module", autouse=True)
def setup_usuarios():
    ControladorUsuarios.EliminarTabla()
    ControladorUsuarios.CrearTabla()
    yield
    ControladorUsuarios.EliminarTabla()

@pytest.fixture(scope="module", autouse=True)
def setup_calculadora():
    ControladorCalculadora.EliminarTabla()
    ControladorCalculadora.CrearTabla()
    yield
    ControladorCalculadora.EliminarTabla()
