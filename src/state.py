
from historial import agregar_mensaje, construir_historial


def crear_estado():
    """Crea el estado inicial de una conversación."""
    return {
        "historial": []
    }


def guardar_turno(estado, pregunta, respuesta):
    """Guarda una pregunta y su respuesta en el historial."""
    agregar_mensaje(
        estado["historial"],
        pregunta,
        respuesta
    )
    return estado


def obtener_historial(estado):
    """Devuelve el historial como texto para el prompt."""
    return construir_historial(estado["historial"])