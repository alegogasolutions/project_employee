import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def cargar_json(ruta: Path):
    with ruta.open(encoding= "utf-8") as f:
        data = json.load(f)

    return data

def cargarDatos():
    return{
        "empresa": cargar_json(DATA_DIR / "empresa.json"),
        "documentos": cargar_json(DATA_DIR / "onboarding_docs.json"),
        "faq": cargar_json(DATA_DIR / "faq_onboarding.json"),
        "empleados": cargar_json(DATA_DIR / "empleados_demo.json")
    }

def tokenizar(texto):
    palabras = texto.lower().split()
    sinonimos = {
    "herramientas": "tools",
    "herramienta": "tools",
    "preparar": "setup",
    "preparo": "setup",
    "empezar": "inicio",
    "trabajar": "trabajo",
    "debo": "necesito",
    "necesito": "inicio"
}

    palabras_vacias = {
        "a", "al", "de", "del", "el", "en", "la", "las",
        "los", "un", "una", "y", "o", "que", "como",
        "para", "por", "con", "me", "mi", "tengo", "debo",
        "puedo", "hoy", "qué", "cómo"
    }

    resultado = set()

    for palabra in palabras:
        palabra = palabra.strip(".,;:¿?¡!()")
        palabra = sinonimos.get(palabra, palabra)

        if palabra not in palabras_vacias and len(palabra) > 1:
             resultado.add(palabra)

    return resultado

# 5. Contar las palabras que coinciden entre pregunta y documento
def puntuar(texto, palabras_pregunta):
    palabras_documento = tokenizar(texto)
    coincidencias = palabras_pregunta & palabras_documento

    return len(coincidencias)


# 6. Buscar los documentos y las FAQ más relevantes
def seleccionar_contexto(
    pregunta,
    datos,
    departamento=None,
    max_docs=3,
    max_faq=2
):
    palabras_pregunta = tokenizar(pregunta)

    pregunta_normalizada = pregunta.lower()

    
    
    herramientas_por_departamento = {
        "sales": {"hubspot"},
        "engineering": {"github", "jira", "notion"},
        "operations": set(),
        "people": set()
    }

    if "herramienta" in pregunta_normalizada:
        palabras_pregunta.update({
            "slack",
            "google",
            "workspace",
            "correo",
            "email"
        })

        palabras_pregunta.update(
            herramientas_por_departamento.get(departamento, set())
        )

    documentos_puntuados = []

    for doc in datos["documentos"]:
        texto = " ".join([
            doc.get("titulo", ""),
            doc.get("cuerpo", ""),
            " ".join(doc.get("tags", [])),
            doc.get("departamento", "")
        ])

        puntuacion = puntuar(texto, palabras_pregunta)

        
        if departamento and doc.get("departamento") == departamento:
            puntuacion += 3

        if (
            departamento
            and departamento in doc.get("tags", [])
        ):
            puntuacion += 2

        if puntuacion > 0:
            documentos_puntuados.append((puntuacion, doc))

    documentos_puntuados.sort(
        key=lambda elemento: elemento[0],
        reverse=True
    )

    documentos_seleccionados = [
        doc for _, doc in documentos_puntuados[:max_docs]
    ]

    faq_puntuadas = []

    for faq in datos["faq"]:
        texto = " ".join([
            faq.get("pregunta", ""),
            faq.get("respuesta_corta", ""),
            " ".join(faq.get("tags", []))
        ])

        puntuacion = puntuar(texto, palabras_pregunta)

        if puntuacion > 0:
            faq_puntuadas.append((puntuacion, faq))

    faq_puntuadas.sort(
        key=lambda elemento: elemento[0],
        reverse=True
    )

    faq_seleccionadas = [
        faq for _, faq in faq_puntuadas[:max_faq]
    ]

    return {
        "documentos": documentos_seleccionados,
        "faq": faq_seleccionadas
    }


          

#empresa = cargar_json(DATA_DIR / "plantilla_preguntas_benchmark.json")

#print(json.dumps(empresa, indent=2, ensure_ascii=False))