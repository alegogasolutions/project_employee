
from config import MAX_TURNOS


def agregar_mensaje(historial, pregunta, respuesta):
    historial.append({
        "pregunta": pregunta,
        "respuesta": respuesta
    })

    if len(historial) > MAX_TURNOS:
        historial.pop(0)

    return historial


def construir_historial(historial):
    if not historial:
        return "Todavía no hay conversaciones anteriores."

    lineas = []

    for turno in historial:
        lineas.append(f"Empleado: {turno['pregunta']}")
        lineas.append(f"Asistente: {turno['respuesta']}")

    return "\n".join(lineas)