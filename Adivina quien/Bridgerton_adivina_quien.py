# --- Sección 1: Importaciones y Configuración Inicial ---

# Importamos la librería 'random'. La usaremos para poder elegir una pregunta al azar
# de la lista de preguntas disponibles. Esto hace que cada partida sea un poco diferente.
import random

# --- Sección 2: Base de Conocimientos ---

# Esta es nuestra "Base de Conocimientos". Es una lista de diccionarios.
# Cada diccionario representa a un personaje y contiene sus atributos (hechos).
# Por ejemplo, para 'Daphne', el hecho 'es_bridgerton' es 'si'.
# El sistema usará estos datos para comparar con las respuestas del usuario.
personajes = [
    {'nombre': 'Daphne Bridgerton', 'es_bridgerton': 'si', 'es_hombre': 'no', 'titulo_noble': 'si', 'es_protagonista': 'si', 'oculta_secreto': 'no'},
    {'nombre': 'Anthony Bridgerton', 'es_bridgerton': 'si', 'es_hombre': 'si', 'titulo_noble': 'si', 'es_protagonista': 'si', 'oculta_secreto': 'no'},
    {'nombre': 'Simon Basset', 'es_bridgerton': 'no', 'es_hombre': 'si', 'titulo_noble': 'si', 'es_protagonista': 'si', 'oculta_secreto': 'no'},
    {'nombre': 'Penelope Featherington', 'es_bridgerton': 'no', 'es_hombre': 'no', 'titulo_noble': 'no', 'es_protagonista': 'si', 'oculta_secreto': 'si'},
    {'nombre': 'Eloise Bridgerton', 'es_bridgerton': 'si', 'es_hombre': 'no', 'titulo_noble': 'no', 'es_protagonista': 'no', 'oculta_secreto': 'no'},
    {'nombre': 'Colin Bridgerton', 'es_bridgerton': 'si', 'es_hombre': 'si', 'titulo_noble': 'no', 'es_protagonista': 'si', 'oculta_secreto': 'no'},
    {'nombre': 'Kate Sharma', 'es_bridgerton': 'no', 'es_hombre': 'no', 'titulo_noble': 'no', 'es_protagonista': 'si', 'oculta_secreto': 'no'},
]

# --- Sección 3: Variables del Juego ---

# Creamos una copia de la base de conocimientos. Esta lista 'posibles' se irá
# reduciendo a medida que hacemos preguntas. Empezamos asumiendo que cualquier
# personaje es una posibilidad. No modificamos la lista original 'personajes'.
posibles = personajes.copy()

# Este diccionario asocia las claves de atributos (ej. 'es_bridgerton') con
# las preguntas que el usuario verá en pantalla. Facilita mostrar la pregunta correcta.
preguntas = {
    'es_bridgerton': '¿Tu personaje es un Bridgerton?',
    'es_hombre': '¿Tu personaje es hombre?',
    'titulo_noble': '¿Tu personaje tiene un título de nobleza importante (Duque/Vizconde)?',
    'es_protagonista': '¿Tu personaje ha protagonizado una temporada?',
    'oculta_secreto': '¿Tu personaje oculta un gran secreto?'
}

# Creamos una lista vacía para llevar un registro de los atributos sobre los que
# ya hemos preguntado. Esto evita que el sistema haga la misma pregunta dos veces.
preguntas_hechas = []

# --- Sección 4: Inicio del Juego ---

# Imprimimos los mensajes de bienvenida para el usuario, dándole las instrucciones
# básicas para poder jugar.
print("¡Bienvenido a Adivina Quién: Edición Bridgerton!")
print("Piensa en un personaje y responde mis preguntas con 'si' o 'no'.\n")

# --- Sección 5: Ciclo Principal del Juego (Motor de Inferencia) ---

# Este es el corazón del sistema. El bucle 'while' se ejecutará repetidamente
# MIENTRAS la longitud de la lista 'posibles' sea mayor que 1.
# Es decir, mientras haya más de un sospechoso, seguiremos haciendo preguntas.
while len(posibles) > 1:
    
    # 1. Selección de la pregunta:
    # Creamos una lista temporal con los atributos que aún NO hemos preguntado.
    # Usamos 'random.choice' para elegir uno de ellos al azar.
    atributo_actual = random.choice([attr for attr in preguntas.keys() if attr not in preguntas_hechas])
    
    # Añadimos el atributo elegido a la lista de 'preguntas_hechas' para no repetirlo.
    preguntas_hechas.append(atributo_actual)
    
    # 2. Interacción con el usuario:
    # Obtenemos la pregunta del diccionario 'preguntas' usando el atributo elegido como clave.
    # 'input()' muestra la pregunta y espera a que el usuario escriba su respuesta.
    # '.lower()' convierte la respuesta a minúsculas ('SI' -> 'si') para evitar errores.
    respuesta = input(f"{preguntas[atributo_actual]} (si/no): ").lower()
    
    # 3. Filtrado (Encadenamiento hacia adelante):
    # Aquí es donde se aplica la "regla". Partimos de un hecho (la respuesta del usuario)
    # y lo usamos para modificar nuestro estado (la lista de 'posibles').
    
    # Creamos una lista temporal vacía para guardar los personajes que SÍ coinciden.
    posibles_actualizados = []
    
    # Recorremos cada 'personaje' que todavía está en nuestra lista de 'posibles'.
    for personaje in posibles:
        # Verificamos si el valor del atributo del personaje (ej. personaje['es_hombre'])
        # es igual a la respuesta que dio el usuario.
        # '.get(atributo_actual)' es una forma segura de acceder al valor.
        if personaje.get(atributo_actual) == respuesta:
            # Si coinciden, añadimos ese personaje a nuestra lista de actualizados.
            posibles_actualizados.append(personaje)
    
    # Reemplazamos nuestra antigua lista de 'posibles' por la nueva lista ya filtrada.
    posibles = posibles_actualizados
    
    # Comprobación de seguridad: Si la lista de posibles se queda vacía, significa
    # que ninguna de nuestras opciones coincide con las respuestas. Rompemos el bucle.
    if not posibles:
        break

# --- Sección 6: Fase Final - Adivinanza y Aprendizaje ---

# Cuando el bucle 'while' termina, pueden pasar tres cosas:

# CASO 1: Hemos encontrado un único sospechoso.
if len(posibles) == 1:
    # Sacamos el único diccionario de personaje que queda en la lista.
    personaje_adivinado = posibles[0]
    
    # Hacemos la pregunta final para confirmar si hemos acertado.
    respuesta_final = input(f"\n¿Tu personaje es {personaje_adivinado['nombre']}? (si/no): ").lower()
    
    # Si el usuario dice que 'si', hemos ganado.
    if respuesta_final == 'si':
        print("\n¡Excelente! ¡He adivinado una vez más!")
    # Si el usuario dice que 'no', hemos perdido y entramos en el modo aprendizaje.
    else:
        # --- MODO APRENDIZAJE ---
        print("\n¡Oh no! Me has vencido. Ayúdame a aprender.")
        # Pedimos el nombre del personaje correcto.
        nombre_correcto = input("¿Cuál era el nombre de tu personaje?: ")
        # Pedimos una pregunta que nos ayude a diferenciar nuestra suposición fallida del personaje correcto.
        nueva_pregunta = input(f"Escribe una pregunta que diferencie a {personaje_adivinado['nombre']} de {nombre_correcto}: ")
        # Preguntamos cuál sería la respuesta a esa nueva pregunta para el personaje correcto.
        respuesta_para_nuevo = input(f"Y para {nombre_correcto}, ¿la respuesta a esa pregunta sería 'si' o 'no'?: ").lower()
        
        # Convertimos la pregunta en una clave de atributo válida (ej. "¿Es reina?" -> "es_reina").
        nuevo_atributo = nueva_pregunta.lower().replace(" ", "_").replace("¿", "").replace("?","")
        
        # Informamos al usuario de lo que hemos aprendido. En un programa real,
        # aquí escribiríamos este nuevo personaje y atributo en un archivo para
        # que la base de conocimientos crezca permanentemente.
        print("\n¡Gracias! He actualizado mi conocimiento.")
        print(f"Nuevo personaje añadido: {nombre_correcto}")
        print(f"Nueva pregunta: '{nueva_pregunta}' (atributo: {nuevo_atributo})")
        print(f"   - Para {nombre_correcto}, la respuesta es '{respuesta_para_nuevo}'")
        # Deducimos la respuesta para el personaje con el que nos confundimos (debe ser la contraria).
        print(f"   - Para {personaje_adivinado['nombre']}, la respuesta es '{'no' if respuesta_para_nuevo == 'si' else 'si'}'")

# CASO 2: La lista 'posibles' se quedó vacía durante el juego.
elif not posibles:
    print("\nMe he quedado sin opciones. No conozco a un personaje con esas características.")
    # Aquí también se podría añadir una opción para que el usuario enseñe al sistema
    # este nuevo personaje desde cero.

# CASO 3: El bucle terminó, pero todavía hay más de un personaje en la lista.
# Esto puede pasar si nos quedamos sin preguntas para diferenciar a los finalistas.
else:
    print("\nMmm... no estoy seguro. Hay varios personajes que coinciden. ¡Me has ganado!")