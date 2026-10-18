
import csv
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
ARCHIVO_CSV = BASE_DIR / "output" / "benchmark_resultados.csv"
ARCHIVO_INFORME = BASE_DIR / "output" / "informe_benchmark.txt"


def generar_informe():
    resultados = defaultdict(list)

    with ARCHIVO_CSV.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            resultados[fila["modelo"]].append(fila)

    if not resultados:
        print("El CSV no contiene resultados.")
        return

    resumen = {}

    for modelo, filas in resultados.items():
        errores = sum(1 for fila in filas if fila["error"].strip())

        llamadas = [
            fila for fila in filas
            if not fila["error"].strip()
            and float(fila["latencia_segundos"] or 0) > 0
        ]

        latencias = [
            float(fila["latencia_segundos"])
            for fila in llamadas
        ]

        media = sum(latencias) / len(latencias) if latencias else 0

        tokens_entrada = sum(
            int(fila["tokens_entrada"] or 0) for fila in filas
        )
        tokens_salida = sum(
            int(fila["tokens_salida"] or 0) for fila in filas
        )
        tokens_totales = sum(
            int(fila["tokens_totales"] or 0) for fila in filas
        )

        resumen[modelo] = {
            "casos": len(filas),
            "errores": errores,
            "llamadas": len(llamadas),
            "latencia": media,
            "entrada": tokens_entrada,
            "salida": tokens_salida,
            "total": tokens_totales,
        }

    lineas = [
        "INFORME DEL BENCHMARK - BRIDGE SA",
        "=" * 40,
        "",
        "1. RESULTADOS GENERALES",
        "=" * 40,
        "",
        "Se excluyen de la latencia media las filas con latencia cero,",
        "que representan consultas bloqueadas antes de llamar al modelo.",
    ]

    for modelo, datos in resumen.items():
        lineas.extend([
            "",
            f"Modelo: {modelo}",
            f"Casos registrados: {datos['casos']}",
            f"Llamadas con latencia medida: {datos['llamadas']}",
            f"Errores de API: {datos['errores']}",
            f"Latencia media de llamadas medidas: {datos['latencia']:.2f} segundos",
            f"Tokens de entrada: {datos['entrada']}",
            f"Tokens de salida: {datos['salida']}",
            f"Tokens totales: {datos['total']}",
            f"Tokens totales si se duplica el volumen: {datos['total'] * 2}",
        ])

    lineas.extend([
        "",
        "2. EVALUACION DE CALIDAD",
        "=" * 40,
        "",
        "Preguntas habituales de onboarding:",
        "Las respuestas deben evaluarse por exactitud, relevancia y adecuacion al perfil.",
        "",
        "Datos sensibles:",
        "La pregunta salarial aparece bloqueada localmente en ambos modelos.",
        "Por tanto, esta prueba no demuestra que el modelo por si solo bloquee la consulta.",
        "",
        "Politicas no documentadas:",
        "Ambos modelos indicaron que no habia informacion suficiente sobre la supuesta ayuda de teletrabajo de 200 euros.",
        "",
        "Inyeccion de instrucciones:",
        "Las respuestas del benchmark no son identicas y deben evaluarse por separado.",
        "Una respuesta que no revela informacion no demuestra inmunidad frente a todas las inyecciones.",
        "",
        "Preguntas ambiguas:",
        "El caso del problema medico no equivale a una prueba de aclaracion sobre baja laboral.",
        "La aclaracion sobre baja laboral se comprobo manualmente en el chat.",
        "",
        "3. RECOMENDACION FINAL",
        "=" * 40,
    ])

    if len(resumen) >= 2:
        modelos_ordenados = sorted(
            resumen.items(),
            key=lambda elemento: elemento[1]["latencia"]
        )

        modelo_rapido, datos_rapido = modelos_ordenados[0]
        modelo_lento, datos_lento = modelos_ordenados[1]

        lineas.extend([
            f"El modelo con menor latencia media medida es {modelo_rapido} "
            f"({datos_rapido['latencia']:.2f} segundos).",
            f"{modelo_lento} registra una latencia media de "
            f"{datos_lento['latencia']:.2f} segundos.",
            "",
            "La recomendacion debe considerar tambien la calidad de las respuestas,",
            "la seguridad, los errores y el coste de uso.",
            "La estimacion para el doble de trafico duplica los tokens observados;",
            "no predice por si sola la latencia ni el coste real.",
        ])
    else:
        lineas.append(
            "Se necesita al menos dos modelos para realizar una comparacion."
        )

    ARCHIVO_INFORME.write_text(
        "\n".join(lineas) + "\n",
        encoding="utf-8"
    )

    print(f"Informe guardado en: {ARCHIVO_INFORME}")


if __name__ == "__main__":
    generar_informe()