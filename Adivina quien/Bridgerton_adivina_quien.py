import random
import json
import sys
import os  ### NUEVO ### Importamos la librería 'os' para manejar rutas de archivos

# --- Sección 1: Manejo de la Base de Conocimientos (JSON) ---

### NUEVO ### Esta línea obtiene la ruta absoluta de la CARPETA donde está este script
script_dir = os.path.dirname(os.path.abspath(__file__))

### NUEVO ### Unimos la ruta de la carpeta con el nombre del archivo JSON
DB_FILE = os.path.join(script_dir, 'basedatos_bridgerton.json')

def cargar_datos():
    """
    Esta función intenta abrir y leer el archivo JSON.
    Devuelve los datos de personajes y preguntas.
    """
    try:
        # Ahora usa la ruta completa y segura
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos['personajes'], datos['preguntas']
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{DB_FILE}'.")
        print("Asegúrate de que 'basedatos_bridgerton.json' está en la misma carpeta que el script.")
        sys.exit()
    except json.JSONDecodeError:
        print(f"Error: El archivo '{DB_FILE}' tiene un formato JSON inválido.")
        sys.exit()

def guardar_datos(personajes, preguntas):
    """
    Esta función guarda los datos actualizados de vuelta en el archivo JSON.
    Se usa cuando el sistema aprende algo nuevo.
    """
    try:
        # También usa la ruta completa para guardar
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            datos_completos = {
                'preguntas': preguntas,
                'personajes': personajes
            }
            json.dump(datos_completos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error al guardar los datos: {e}")

# --- Sección 2: Inicialización del Juego ---

personajes, preguntas = cargar_datos()
posibles = personajes.copy()
preguntas_hechas = []
respuestas_dadas = {}

# --- Sección 3: Presentación (Se ejecuta solo una vez) ---

print("¡Bienvenido a Adivina Quién: Edición Bridgerton!")
print("Piensa en un personaje y responde mis preguntas con 'si' o 'no'.\n")

# --- Sección 4: Ciclo Principal del Juego (Motor de Inferencia) ---

while len(posibles) > 1:
    atributos_disponibles = [attr for attr in preguntas.keys() if attr not in preguntas_hechas]
    
    if not atributos_disponibles:
        break
        
    atributo_actual = random.choice(atributos_disponibles)
    preguntas_hechas.append(atributo_actual)
    
    respuesta = "" # Inicializamos la variable
    while respuesta not in ['si', 'no']:
        respuesta = input(f"{preguntas[atributo_actual]} (si/no): ").lower()
        if respuesta not in ['si', 'no']:
            print("Respuesta inválida. Por favor, responde solo 'si' o 'no'.")

    respuestas_dadas[atributo_actual] = respuesta

    posibles_actualizados = []
    for personaje in posibles:
        if personaje.get(atributo_actual) == respuesta:
            posibles_actualizados.append(personaje)
    
    posibles = posibles_actualizados
    
    if not posibles:
        break

# --- Sección 5: Fase Final - Adivinanza y Aprendizaje ---

if len(posibles) == 1:
    personaje_adivinado = posibles[0]
    respuesta_final = input(f"\n¿Tu personaje es {personaje_adivinado['nombre']}? (si/no): ").lower()
    
    if respuesta_final == 'si':
        print("\n¡Excelente! ¡He adivinado una vez más!")
    else:
        # --- MODO APRENDIZAJE (AHORA GUARDA EN JSON) ---
        print("\n¡Oh no! Me has vencido. Ayúdame a aprender.")
        nombre_correcto = input("¿Cuál era el nombre de tu personaje?: ")
        nueva_pregunta = input(f"Escribe una pregunta que diferencie a {personaje_adivinado['nombre']} de {nombre_correcto}: ")
        respuesta_para_nuevo = input(f"Y para {nombre_correcto}, ¿la respuesta a esa pregunta sería 'si' o 'no'?: ").lower()
        
        nuevo_atributo = nueva_pregunta.lower().replace(" ", "_").replace("¿", "").replace("?","")
        
        preguntas[nuevo_atributo] = nueva_pregunta
        
        nuevo_personaje = respuestas_dadas.copy()
        nuevo_personaje['nombre'] = nombre_correcto
        nuevo_personaje[nuevo_atributo] = respuesta_para_nuevo
        
        # Actualizar todos los personajes existentes con un valor por defecto para la nueva pregunta
        for p in personajes:
            if p['nombre'] == personaje_adivinado['nombre']:
                p[nuevo_atributo] = 'no' if respuesta_para_nuevo == 'si' else 'si'
            elif nuevo_atributo not in p:
                # Damos un valor 'desconocido' o 'no' a los demás
                p[nuevo_atributo] = 'no' 
        
        personajes.append(nuevo_personaje)
        
        guardar_datos(personajes, preguntas)
        
        print("\n¡Gracias! He actualizado mi base de conocimientos para la próxima vez.")

elif not posibles:
    print("\nMe he quedado sin opciones. No conozco a un personaje con esas características.")
else:
    print(f"\nMmm... no estoy seguro. Quedan {len(posibles)} personajes:")
    for p in posibles:
        print(f"- {p['nombre']}")
    print("¡Me has ganado!")