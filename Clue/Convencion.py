import random
import json
from pathlib import Path # Para encontrar el archivo .json

# --- Carga de Datos ---
RUTA_BASE = Path(__file__).parent
RUTA_JSON = RUTA_BASE / "misterios.json"

def cargar_escenarios(archivo_json):
    """Carga la lista de 5 escenarios desde un archivo JSON."""
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error fatal al cargar '{archivo_json}': {e}")
        return None

# Listas para que el usuario elija (deben coincidir con el JSON)
personajes = ["Dra. Evelyn Reed", "Profesor Kenji Tanaka", "Glitch", "Bryce Wagner", "Chloe Jenkins"]
armas = ["Cable de Red", "Prototipo de Dron Pesado", "Café Envenenado", "Unidad USB Corrupta", "Premio a la Innovación"]
locaciones = ["El Escenario Principal", "El Laboratorio de Pruebas", "La Sala de Servidores", "El Salón VIP", "El Muelle de Carga"]

# --- INICIO DEL JUEGO ---

# Cargamos los 5 escenarios desde el archivo
lista_escenarios = cargar_escenarios(RUTA_JSON)

if not lista_escenarios:
    print("Saliendo del programa. No se pudieron cargar los 5 escenarios.")
else:
    print("="*30)
    print("MISTERIO EN INNOVATECH 2025")
    print("="*30)
    print("Ha ocurrido un asesinato. El Dr. Aris Thorne ha sido encontrado.")
    print("Debes adivinar la combinación correcta de culpable, arma y locación.\n")

    # El juego elige aleatoriamente 1 de las 5 historias
    solucion_secreta = random.choice(lista_escenarios)

    # --- Bucle del Juego ---
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
            print(solucion_secreta["historia"]) # Muestra la historia ganadora
            break # Termina el bucle
        else:
            print("\nINCORRECTO. Esa no es la solución. El verdadero culpable sigue libre.")
            print("Intenta de nuevo...")
            # El bucle vuelve a empezar

    print("\n--- FIN DEL JUEGO ---")