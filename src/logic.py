
from context import seleccionar_contexto
from prompts import build_context_block, build_chat_prompt
from gemini_client import llamar_gemini_texto
from validators import validar_pregunta
from state import guardar_turno, obtener_historial


def responder_pregunta(pregunta, empleado, datos, estado):
    # 1. Comprobar si la pregunta es segura.
    es_valida, mensaje = validar_pregunta(pregunta)

    if not es_valida:
        return mensaje

    # 2. Normalizar la pregunta.
    pregunta_normalizada = pregunta.lower()

    
    # 2.1. Aclarar las preguntas ambiguas sobre una baja.
    preguntas_sobre_baja = [
        "pedir la baja",
        "tramitar una baja",
        "solicitar la baja",
        "necesito la baja",
        "darme de baja",
        "gestionar una baja"
    ]

    if any(
        frase in pregunta_normalizada
        for frase in preguntas_sobre_baja
    ):
        return (
            "¿Te refieres a una baja médica por motivos de salud "
            "o a una baja laboral o excedencia? El procedimiento "
            "es diferente según el caso."
        )

    # 3. Comprobar preguntas sobre días extra de vacaciones.
    preguntas_sobre_dias_extra = [
        "días extra de vacaciones",
        "dias extra de vacaciones",
        "vacaciones adicionales",
        "días adicionales de vacaciones",
        "dias adicionales de vacaciones"
    ]

    if any(
        frase in pregunta_normalizada
        for frase in preguntas_sobre_dias_extra
    ):
        return (
            "No encuentro información suficiente en la documentación "
            "de Bridge SA para confirmar días extra de vacaciones."
        )

    # 4. Buscar documentos y preguntas frecuentes.
    resultado = seleccionar_contexto(
        pregunta,
        datos,
        departamento=empleado.get("departamento")
    )

    if not resultado["documentos"] and not resultado["faq"]:
        return (
            "No encuentro información suficiente en la documentación "
            "de Bridge SA para responder con seguridad."
        )

    # 5. Preparar el contexto.
    contexto = build_context_block(
        perfil=empleado,
        faq_entries=resultado["faq"],
        documentos=resultado["documentos"]
    )

    # 6. Recuperar el historial.
    historial_texto = obtener_historial(estado)

    # 7. Construir el prompt.
    prompt = build_chat_prompt(
        contexto,
        pregunta,
        historial_texto
    )

    # 8. Consultar a Gemini.
    respuesta = llamar_gemini_texto(prompt)

    # 9. Guardar la conversación.
    guardar_turno(estado, pregunta, respuesta)

    return respuesta
