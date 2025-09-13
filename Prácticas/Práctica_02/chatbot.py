import json
import os

# Archivo donde se guarda el "conocimiento" del bot
BASE_DATOS = "conocimiento.json"

# Si no existe la base de datos, se crea con respuestas iniciales
if not os.path.exists(BASE_DATOS):
    conocimiento_inicial = {
        "hola": "¡Hola! ¿Cómo estás?",
        "como estas": "Estoy bien, ¿y tú?",
        "de que te gustaria hablar": "Podemos hablar de lo que quieras :)"
    }
    with open(BASE_DATOS, "w") as f:
        json.dump(conocimiento_inicial, f, indent=4)

# Cargar la base de datos
with open(BASE_DATOS, "r") as f:
    conocimiento = json.load(f)

print(" Chatbot iniciado. Escribe 'salir' para terminar.\n")

while True:
    pregunta = input("Tú: ").lower().strip()

    if pregunta == "salir":
        print("CB Adiós! Hasta la próxima.")
        break

    # Buscar si el chatbot ya conoce la respuesta
    if pregunta in conocimiento:
        print("CB:", conocimiento[pregunta])
    else:
        print("CB: No sé cómo responder eso...")
        nueva_respuesta = input("Por favor, enséñame la respuesta: ")
        conocimiento[pregunta] = nueva_respuesta

        # Guardar el nuevo conocimiento
        with open(BASE_DATOS, "w") as f:
            json.dump(conocimiento, f, indent=4)

        print("CB: ¡Gracias! Ahora ya sé cómo responder eso.")
