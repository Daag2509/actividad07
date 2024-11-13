
## Conversor de Texto a Voz

Este programa permite convertir texto a voz utilizando la biblioteca pyttsx3 y almacenar tanto el texto original como la ruta del archivo de audio generado en una base de datos PostgreSQL. También incluye funcionalidades para leer, buscar, actualizar y eliminar registros en la base de datos.

## Requisitos

* Python 3.x
* 0Bibliotecas:
* dearpygui
* pyttsx3
* psycopg


## Estructura de datos

* Base de Datos: actividad07
* Tabla: textos_audios

1. id	SERIAL	Identificador único para cada registro (clave primaria)
2. texto_original	TEXT	El texto que se va a convertir en audio
3. audio_path	TEXT	La ruta al archivo de audio generado
## Funciones

1. conectar_db()
Conecta a la base de datos PostgreSQL y devuelve la conexión.

Uso:
conexion = conectar_db()

2. guardar_en_db(texto, audio_path)

Guarda el texto original y la ruta del archivo de audio en la tabla textos_audios.

Parámetros:
texto: El texto que se va a guardar.
audio_path: La ruta del archivo de audio generado.

Uso:
guardar_en_db("Texto ejemplo", "ruta/al/audio.mp3")

3. leer_datos()

Lee todos los registros de la tabla textos_audios y los imprime en la consola.

Uso:
leer_datos()

4. actualizar_registro(id_registro, nuevo_texto)

Actualiza el texto original de un registro existente en la tabla.

Parámetros:
id_registro: El ID del registro que se desea actualizar.
nuevo_texto: El nuevo texto que reemplazará al antiguo.

Uso:
actualizar_registro(1, "Nuevo texto")

5. borrar_registro(id_registro)

Borra un registro específico de la tabla según su ID.

Parámetros:
id_registro: El ID del registro que se desea borrar.

Uso:
borrar_registro(1)

6. reproducir_audio(audio_path)

Reproduce el archivo de audio almacenado en la ruta especificada.

Parámetros:
audio_path: La ruta del archivo de audio a reproducir.

Uso:
reproducir_audio("ruta/al/audio.mp3")

7. buscar_texto(busqueda)

Busca textos específicos en la tabla según una cadena proporcionada y muestra los resultados en la consola.

Parámetros:
busqueda: La cadena que se desea buscar dentro del texto original.

Uso:
buscar_texto("ejemplo")

8. start_conversion(sender, app_data)

Convierte el texto ingresado por el usuario a voz y guarda el resultado como un archivo MP3. También guarda el texto y la ruta del archivo en la base de datos.

9. file_callback(sender, app_data)

Carga un archivo de texto seleccionado por el usuario y muestra su contenido en el campo correspondiente.

10. update_text_stats(text)

Actualiza las estadísticas (número de palabras y letras) del texto cargado y las muestra en la interfaz gráfica.

11. test_voice(sender, app_data)

Prueba la conversión a voz con el texto actual sin guardar el archivo.

12. get_voices()

Obtiene una lista de voces disponibles del motor TTS (pyttsx3).

## Interfaz grafica

* La interfaz gráfica está construida utilizando DearPyGui e incluye:

1. Un botón para cargar archivos de texto.

2. Un área para mostrar el contenido del texto cargado.

3. Contadores para mostrar cuántas palabras y letras hay en el texto.

4. Controles deslizantes para ajustar velocidad y volumen.

5. Botones para probar voz, convertir texto a voz, leer datos desde la base de datos, buscar textos específicos y eliminar registros por ID.
