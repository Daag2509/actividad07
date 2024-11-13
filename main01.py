import dearpygui.dearpygui as dpg
import pyttsx3
import os
import psycopg

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

# Conectar a la base de datos
def conectar_db():
    try:
        conexion = psycopg.connect(
            host="localhost",
            dbname="actividad07",
            user="postgres",
            password="30214055"
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Guardar texto y audio en la base de datos
def guardar_en_db(texto, audio_path):
    conexion = conectar_db()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO textos_audios (texto_original, audio_path) VALUES (%s, %s)",
                    (texto, audio_path)
                )
                conexion.commit()
                print("Datos guardados en la base de datos.")
        except Exception as e:
            print(f"Error al guardar en la base de datos: {e}")
        finally:
            conexion.close()

# Leer datos desde la base de datos
def leer_datos():
    conexion = conectar_db()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT texto_original, audio_path FROM textos_audios")
                registros = cursor.fetchall()

                # Mostrar los registros en una tabla simple
                for registro in registros:
                    print(f"Texto: {registro[0]}, Audio: {registro[1]}")
        except Exception as e:
            print(f"Error al leer registros: {e}")
        finally:
            conexion.close()

# Actualizar un registro existente
def actualizar_registro(id_registro, nuevo_texto):
    conexion = conectar_db()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "UPDATE textos_audios SET texto_original = %s WHERE id = %s",
                    (nuevo_texto, id_registro)
                )
                conexion.commit()
                print("Registro actualizado.")
        except Exception as e:
            print(f"Error al actualizar registro: {e}")
        finally:
            conexion.close()

# Borrar un registro específico
def borrar_registro(id_registro):
    conexion = conectar_db()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM textos_audios WHERE id = %s", (id_registro,))
                conexion.commit()
                print("Registro borrado.")
        except Exception as e:
            print(f"Error al borrar registro: {e}")
        finally:
            conexion.close()

# Reproducir audio almacenado
def reproducir_audio(audio_path):
    os.system(f'start {audio_path}') 
# Buscar texto específico en la base de datos
def buscar_texto(busqueda):
    conexion = conectar_db()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT texto_original FROM textos_audios WHERE texto_original ILIKE %s", (f'%{busqueda}%',))
                resultados = cursor.fetchall()

                for resultado in resultados:
                    print(f"Texto encontrado: {resultado[0]}")
        except Exception as e:
            print(f"Error al buscar texto: {e}")
        finally:
            conexion.close()

# Función para convertir texto a voz y guardar el archivo generado
def start_conversion(sender, app_data):
    # Obtener el texto a convertir
    texto = dpg.get_value("text_display")

    # Obtener configuración de velocidad y volumen
    rate = dpg.get_value("slider_rate")
    volume = dpg.get_value("slider_volume")

    # Configurar el motor de texto a voz
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Convertir el texto a voz y guardar como archivo mp3
    audio_file_path = "audio_nuevo.mp3"
    engine.save_to_file(texto, audio_file_path)
    engine.runAndWait()

    # Guardar en la base de datos
    guardar_en_db(texto, audio_file_path)

    # Mostrar popup de confirmación
    dpg.configure_item("popup_id", show=True)

# Callback para cargar archivo de texto
def file_callback(sender, app_data):
    if 'file_path_name' in app_data:
        file_path = app_data['file_path_name']
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                dpg.set_value("text_display", content)
                update_text_stats(content)  # Actualizar estadísticas de texto
        except FileNotFoundError:
            print(f"Error: El archivo no se encontró en la ruta: {file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")

# Actualizar estadísticas del texto cargado
def update_text_stats(text):
    word_count = len(text.split())
    letter_count = len(text)
    dpg.set_value("word_count_display", f"Palabras: {word_count}")
    dpg.set_value("letter_count_display", f"Letras: {letter_count}")

# Probar voz con el texto actual
def test_voice(sender, app_data):
    texto = dpg.get_value("text_display")

    rate = dpg.get_value("slider_rate")
    volume = dpg.get_value("slider_volume")

    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    engine.say(texto)
    engine.runAndWait()

# Obtener voces disponibles del motor TTS
def get_voices():
    voices = engine.getProperty('voices')
    return voices

# Crear contexto y ventana principal con DearPyGui
dpg.create_context()
with dpg.window(label="Conversor de Texto a Voz", width=600, height=600):

    # Botón para cargar el archivo de texto
    dpg.add_button(label="Cargar archivo de texto", callback=lambda: dpg.show_item("file_dialog_id"))

    # Mostrar contenido del archivo cargado
    dpg.add_text("Contenido del texto:")
    dpg.add_input_text(tag="text_display", multiline=True, readonly=True, width=500, height=200)

   # Contadores de palabras y letras 
    dpg.add_text(tag="word_count_display", default_value="Palabras: 0")
    dpg.add_text(tag="letter_count_display", default_value="Letras: 0")

   # Controles para ajustar velocidad y volumen 
    dpg.add_text("Configuraciones de voz")
    voices = get_voices()
    voice_names = [voice.name for voice in voices]
    dpg.add_combo(label="Voces", items=voice_names, tag="voice_selector")
    dpg.add_slider_int(tag="slider_rate", label="Velocidad", default_value=150, min_value=100, max_value=300)
    dpg.add_slider_float(tag="slider_volume", label="Volumen", default_value=0.8, min_value=0.0, max_value=1.0)

   # Botones para probar voz y convertir 
    dpg.add_button(label="Probar voz", callback=test_voice)
    dpg.add_button(label="Convertir texto a voz", callback=start_conversion)

   # Botón para leer datos desde la base de datos 
    dpg.add_button(label="Leer Datos", callback=lambda: leer_datos())

   # Entrada para buscar textos específicos 
    dpg.add_input_text(tag="search_input", label="Buscar Texto")
    dpg.add_button(label="Buscar", callback=lambda: buscar_texto(dpg.get_value("search_input")))

   # Entrada para eliminar un registro por ID 
    dpg.add_input_int(tag="delete_id", label="ID del Registro a Borrar")
    dpg.add_button(label="Eliminar Registro", callback=lambda: borrar_registro(dpg.get_value("delete_id")))

# Cuadro de diálogo para seleccionar el archivo 
with dpg.file_dialog(directory_selector=False, show=False, callback=file_callback, tag="file_dialog_id"):
     dpg.add_file_extension(".txt", color=(0, 255 , 0 , 255))  # Filtra solo archivos .txt

# Popup de confirmación 
with dpg.window(label="Confirmación", modal=True, show=False, tag="popup_id"):
     dpg.add_text("La conversión se ha completado con éxito.")
     dpg.add_button(label="Cerrar", callback=lambda: dpg.configure_item("popup_id", show=False))

# Configurar y mostrar la ventana principal 
dpg.create_viewport(title="Conversor de Texto a Voz", width=600 , height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()