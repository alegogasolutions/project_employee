from context import cargarDatos
from logic import responder_pregunta
from state import crear_estado
from checklist import (
    crear_checklist,
    obtener_tareas_iniciales,
    guardar_checklist,
    marcar_tarea_completada
)
from pathlib import Path



datos = cargarDatos()
estado = crear_estado()

print("Empleados disponibles:")
for empleado in datos["empleados"]:
    print(f'{empleado["id"]} - {empleado["nombre"]}')

id_empleado = input("Introduce tu ID de empleado: ").strip()

empleado_actual = next(
    (
        empleado
        for empleado in datos["empleados"]
        if empleado["id"] == id_empleado
    ),
    None
)

if empleado_actual is None:
    print("ID de empleado no encontrado.")
    exit()


print("\n¿Qué quieres hacer?")
print("1. Hacer una pregunta sobre onboarding")
print("2. Generar mi checklist de los cinco días")
print("3. Marcar una tarea como completada")

opcion = input("Elige una opción (1, 2 o 3): ").strip()

if opcion == "2":
    tareas_por_dia = obtener_tareas_iniciales(empleado_actual)
    checklist = crear_checklist(empleado_actual, tareas_por_dia)

    ruta_salida = (
        Path(__file__).parent.parent
        / "output"
        / f"checklist_{empleado_actual['id']}.json"
    )
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    guardar_checklist(checklist, ruta_salida)
    print(f"\nChecklist guardada en: {ruta_salida}")



elif opcion == "1":
    print("\nEscribe 'salir' cuando quieras terminar el chat.")

    while True:
        pregunta = input("\nTú: ").strip()

        if pregunta.lower() == "salir":
            print("Chat terminado.")
            break

        if not pregunta:
            print("Escribe una pregunta para continuar.")
            continue

        respuesta = responder_pregunta(
            pregunta,
            empleado_actual,
            datos,
            estado
        )

        print(f"\nAsistente: {respuesta}")
elif opcion == "3":
    ruta_salida = (
        Path(__file__).parent.parent
        / "output"
        / f"checklist_{empleado_actual['id']}.json"
    )

    if not ruta_salida.exists():
        print("Todavía no existe tu checklist. Genera una primero con la opción 2.")

    else:
        import json

        with open(ruta_salida, "r", encoding="utf-8") as archivo:
            checklist = json.load(archivo)

        for dia in checklist["dias"]:
            print(f"\nDía {dia['dia']}:")

            for numero, tarea in enumerate(dia["tareas"], start=1):
                estado = "Completada" if tarea["completada"] else "Pendiente"
                print(f"{numero}. [{estado}] {tarea['titulo']}")

        try:
            dia_numero = int(input("\n¿Qué día quieres actualizar (1-5)? "))
            tarea_numero = int(input("¿Qué número de tarea quieres completar? "))

            actualizada = marcar_tarea_completada(
                checklist,
                dia_numero,
                tarea_numero
            )

            if actualizada:
                guardar_checklist(checklist, ruta_salida)
                print("¡Tarea marcada como completada y guardada!")
            else:
                print("Ese día o número de tarea no es válido.")

        except ValueError:
            print("Debes introducir números válidos.")

else:
    print("Opción no válida. Elige 1, 2 o 3.")

