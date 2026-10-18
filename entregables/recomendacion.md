# Recomendación — Employee Onboarding Assistant

## Caso de uso

El asistente acompaña a los nuevos empleados de Bridge SA durante sus primeros cinco días. Responde preguntas utilizando la documentación interna, adapta las respuestas al perfil del empleado y genera checklists de onboarding. No debe inventar políticas, revelar datos confidenciales de otros empleados ni atender consultas externas al onboarding.

## Modelo recomendado para el prototipo

Se recomienda provisionalmente `gemini-3.5-flash-lite` para el chat en tiempo real.

En el benchmark se registraron 10 casos por modelo, sin errores de API. Una de las consultas fue bloqueada localmente antes de llamar al modelo, por lo que se midieron nueve llamadas por modelo.

En esta ejecución, `gemini-3.5-flash-lite` obtuvo una latencia media de **1,13 segundos** y consumió **8.091 tokens** en total. `gemini-3.1-flash-lite` obtuvo una latencia media de **5,76 segundos** y consumió **8.200 tokens**.

Por tanto, en esta muestra, Gemini 3.5 Flash Lite fue más rápido y utilizó 109 tokens menos. Estos resultados describen únicamente la ejecución realizada y no garantizan el mismo rendimiento en otras condiciones.

## Modelo alternativo

`gemini-3.1-flash-lite` se mantiene como alternativa para futuras comparaciones. En el caso de inyección incluido en el benchmark, respondió rechazando explícitamente la petición maliciosa, mientras que Gemini 3.5 Flash Lite indicó que no encontraba información suficiente.

Esta diferencia debe evaluarse con más casos antes de concluir que un modelo es más seguro. La protección del asistente depende también de la validación de entradas, la selección de contexto y las instrucciones de seguridad.

## Trade-off principal

En esta ejecución, `gemini-3.5-flash-lite` combinó menor latencia media con un consumo total de tokens ligeramente inferior.

La diferencia fue de 109 tokens en los 10 casos registrados por modelo. La muestra es pequeña y no basta para garantizar que el modelo sea siempre más rápido o económico. Los resultados pueden variar según las preguntas, la longitud del contexto, la carga del servicio y las condiciones de uso.

## ¿Qué pasaría si duplicáramos el tráfico?

Si se duplicara el volumen de consultas y se mantuviera el mismo consumo medio por consulta, el consumo estimado pasaría de 8.091 a **16.182 tokens** para `gemini-3.5-flash-lite`, y de 8.200 a **16.400 tokens** para `gemini-3.1-flash-lite`.

Esta estimación supone que se repite una carga equivalente a la del benchmark. No predice por sí sola el coste económico ni la latencia con tráfico duplicado. También habría que considerar las tarifas vigentes, los límites de cuota, la concurrencia y posibles errores o reintentos.

Antes de escalar, convendría medir tokens por consulta, latencia, errores y capacidad disponible.

## Riesgos y condiciones antes del despliegue

* Repetir el benchmark con más casos y en diferentes momentos.
* Evaluar manualmente las respuestas con una rúbrica común para ambos modelos.
* Mantener las validaciones que bloquean solicitudes no permitidas antes de llamar al modelo.
* Ampliar las pruebas de inyección con diferentes formulaciones.
* Verificar que las preguntas ambiguas generan aclaraciones cuando sea necesario.
* Comprobar que el asistente no inventa políticas ni revela información confidencial.
* Automatizar las pruebas de robustez que actualmente requieren comprobación manual.

## Conclusión

Para el prototipo se recomienda `gemini-3.5-flash-lite` por su menor latencia media y su consumo total de tokens ligeramente inferior en esta ejecución. La elección es provisional y debe revisarse con más pruebas de calidad, seguridad y rendimiento antes de un despliegue real.
