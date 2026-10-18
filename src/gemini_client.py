
from google import genai

from config import MODEL, TEMPERATURE_TEXTO
from gemini_auth import configurar_gemini_api_key

_cliente_gemini = None


def crear_cliente():
    global _cliente_gemini

    if _cliente_gemini is None:
        configurar_gemini_api_key()
        _cliente_gemini = genai.Client()

    return _cliente_gemini



def llamar_gemini_texto(prompt: str) -> str:
    try:
        cliente = crear_cliente()

        respuesta = cliente.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=TEMPERATURE_TEXTO
            )
        )

        return (respuesta.text or "").strip()

    except Exception as error:
        print(f"Error al conectar con Gemini: {error}")
        return "Lo siento, el asistente no está disponible en este momento. Inténtalo de nuevo más tarde."