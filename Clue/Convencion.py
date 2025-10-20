import random

# 1. Definir los 5 escenarios (historias)
escenario1 = {
    "culpable": "Dra. Evelyn Reed",
    "arma": "Café Envenenado",
    "locacion": "El Salón VIP",
    "historia": "¡Correcto! La Dra. Reed no podía permitir que Thorne triunfara..."
}
escenario2 = {
    "culpable": "Profesor Kenji Tanaka",
    "arma": "Premio a la Innovación",
    "locacion": "El Escenario Principal",
    "historia": "¡Has descubierto la verdad! El Profesor Tanaka confrontó a Thorne..."
}
escenario3 = {
    "culpable": "Glitch",
    "arma": "Unidad USB Corrupta",
    "locacion": "El Laboratorio de Pruebas",
    "historia": "¡Impresionante! 'Glitch' creía que la IA de Thorne..."
}
escenario4 = {
    "culpable": "Bryce Wagner",
    "arma": "Prototipo de Dron Pesado",
    "locacion": "El Muelle de Carga",
    "historia": "¡Exacto! Wagner estaba arruinado. Había invertido todo en Thorne..."
}
escenario5 = {
    "culpable": "Chloe Jenkins",
    "arma": "Cable de Red",
    "locacion": "La Sala de Servidores",
    "historia": "¡Increíble, era ella! Chloe descubrió que Thorne planeaba despedirla..."
}

# Lista de todos los posibles finales
lista_escenarios = [escenario1, escenario2, escenario3, escenario4, escenario5]

# Listas para que el usuario elija
personajes = ["Dra. Evelyn Reed", "Profesor Kenji Tanaka", "Glitch", "Bryce Wagner", "Chloe Jenkins"]
armas = ["Cable de Red", "Prototipo de Dron Pesado", "Café Envenenado", "Unidad USB Corrupta", "Premio a la Innovación"]
locaciones = ["El Escenario Principal", "El Laboratorio de Pruebas", "La Sala de Servidores", "El Salón VIP", "El Muelle de Carga"]

# --- INICIO DEL JUEGO ---
print("="*30)
print("MISTERIO EN INNOVATECH 2025")
print("="*30)
print(f"Ha ocurrido un asesinato. El cuerpo del Dr. Aris Thorne ha sido encontrado.")
print("Debes descubrir quién lo hizo, con qué arma y dónde.\n")

# El juego elige aleatoriamente la solución
solucion_secreta = random.choice(lista_escenarios)

# Bucle del juego
while True:
    print("\n--- HAZ TU ACUSACIÓN ---")

    # Función auxiliar para mostrar menú y obtener elección
    def hacer_eleccion(titulo, lista):
        print(f"\nElige {titulo}:")
        for i, item in enumerate(lista):
            print(f"  {i+1}. {item}")
        while True:
            try:
                eleccion = int(input(f"Tu elección (1-{len(lista)}): "))
                if 1 <= eleccion <= len(lista):
                    return lista[eleccion-1]
                else:
                    print("Por favor, introduce un número válido.")
            except ValueError:
                print("Por favor, introduce un número.")

    # Pedir las 3 partes de la acusación
    guess_culpable = hacer_eleccion("un CULPABLE", personajes)
    guess_arma = hacer_eleccion("un ARMA", armas)
    guess_locacion = hacer_eleccion("una LOCACIÓN", locaciones)

    print(f"\nTu acusación: Fue {guess_culpable} con {guess_arma} en {guess_locacion}.")

    # Comprobar si la acusación es correcta
    if (guess_culpable == solucion_secreta["culpable"] and
        guess_arma == solucion_secreta["arma"] and
        guess_locacion == solucion_secreta["locacion"]):

        print("\n¡FELICIDADES! ¡HAS RESUELTO EL CASO!")
        print("-" * 30)
        print(solucion_secreta["historia"])
        break # Termina el bucle
    else:
        print("\nINCORRECTO. Esa no es la solución. El verdadero culpable sigue libre.")
        print("Intenta de nuevo...")
        # El bucle vuelve a empezar

print("\n--- FIN DEL JUEGO ---")