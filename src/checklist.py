
import json



def crear_checklist(empleado, tareas_por_dia):
    checklist = {
        "empleado_id": empleado["id"],
        "dias": []
    }

    for dia in range(1, 6):
        tareas = tareas_por_dia.get(dia, [])

        dia_checklist = {
            "dia": dia,
            "mensaje_resumen": f"Objetivos de onboarding del día {dia}.",
            "tareas": []
        }

        for numero, tarea in enumerate(tareas, start=1):
            dia_checklist["tareas"].append({
                "id": f"dia{dia}_tarea{numero}",
                "titulo": tarea["tarea"],
                "fuente_doc": tarea["documento_origen"],
                "completada": False
            })

        checklist["dias"].append(dia_checklist)

    return checklist


def guardar_checklist(checklist, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(checklist, archivo, ensure_ascii=False, indent=2)



def obtener_tareas_iniciales(empleado):
    tareas_por_dia = {}

    departamento = empleado["departamento"].lower()

    
    tareas_comunes = [
        {
            "tarea": "Activar Slack antes de las 9:00",
            "documento_origen": "doc_bienvenida_01"
        },
        {
            "tarea": "Activar el correo corporativo antes de las 9:00",
            "documento_origen": "doc_bienvenida_01"
        },
        {
            "tarea": "Comprobar el acceso de lectura a Notion antes de las 9:00",
            "documento_origen": "doc_bienvenida_01"
        }
    ]

    if departamento == "engineering":
        documento_id = "doc_eng_01"

        tareas_por_dia = {
            1: [
                {
                    "tarea": "Asistir a la sesión de bienvenida",
                    "documento_origen": "doc_bienvenida_01"
                },
                {
                    "tarea": "Activar la verificación en dos pasos (2FA) de GitHub",
                    "documento_origen": "doc_it_03"
                },
                {
                    "tarea": "Leer la arquitectura en Notion",
                    "documento_origen": documento_id
                }
            ],
            2: [
                {
                    "tarea": "Configurar el entorno local con Python 3.10 o superior",
                    "documento_origen": documento_id
                },
                {
                    "tarea": "Solicitar acceso a staging",
                    "documento_origen": documento_id
                }
            ],
            3: [
                {
                    "tarea": "Realizar una sesión de pair programming con el buddy",
                    "documento_origen": documento_id
                }
            ],
            4: [
                {
                    "tarea": "Trabajar en la primera issue asignada en Jira",
                    "documento_origen": documento_id
                }
            ],
            5: [
                {
                    "tarea": "Realizar la retrospectiva de onboarding con el manager",
                    "documento_origen": documento_id
                }
            ]
        }

    elif departamento == "sales":
        documento_id = "doc_sales_01"

        tareas_por_dia = {
            1: [
                {
                    "tarea": "Asistir a la bienvenida y obtener acceso a HubSpot",
                    "documento_origen": documento_id
                }
            ],
            2: [
                {
                    "tarea": "Realizar la formación sobre el catálogo de programas",
                    "documento_origen": documento_id
                }
            ],
            3: [
                {
                    "tarea": "Observar una llamada comercial",
                    "documento_origen": documento_id
                }
            ],
            4: [
                {
                    "tarea": "Practicar el pitch comercial interno",
                    "documento_origen": documento_id
                }
            ],
            5: [
                {
                    "tarea": "Revisar el pipeline con el manager",
                    "documento_origen": documento_id
                }
            ]
        }

    if 1 in tareas_por_dia:
        tareas_por_dia[1] = tareas_comunes + tareas_por_dia[1]

    return tareas_por_dia


def marcar_tarea_completada(checklist, dia_numero, tarea_numero):
    for dia in checklist["dias"]:
        if dia["dia"] == dia_numero:
            tareas = dia["tareas"]

            if 1 <= tarea_numero <= len(tareas):
                tareas[tarea_numero - 1]["completada"] = True
                return True

            return False

    return False

