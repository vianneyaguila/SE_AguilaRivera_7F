# ==================================
# 1. motor_inferencia.py (Motor de Inferencia y Base de Conocimiento JSON)
# ==================================
import json
import os
from modelo_conocimiento import ReglaInferencia 
import random 

# Definimos la ruta del archivo JSON de conocimiento (se busca en la carpeta principal)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
CONOCIMIENTO_FILE = os.path.join(BASE_DIR, 'base_conocimiento.json')

class MotorRecomendacion:
    """Clase principal que gestiona la base de conocimiento JSON y la lógica de inferencia."""
    def __init__(self):
        self.reglas = []
        self.libros = [] # Almacenará los datos del JSON

    def cargar_conocimiento_json(self):
        """Carga los datos de los libros desde el archivo JSON."""
        try:
            with open(CONOCIMIENTO_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.libros = data.get('libros', [])
            # print(f"✅ {len(self.libros)} libros cargados desde JSON.")
            return True
        except FileNotFoundError:
            print(f"❌ Error: El archivo {CONOCIMIENTO_FILE} no fue encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"❌ Error: El archivo JSON no es válido.")
            return False

    def cargar_reglas(self):
        """Carga las reglas de inferencia (el conocimiento experto)."""
        self.reglas.clear()

        # Reglas para GÉNERO
        self.reglas.append(ReglaInferencia('Romance', 'Romance', 0.95))
        self.reglas.append(ReglaInferencia('Comic', 'Comic', 0.95))
        self.reglas.append(ReglaInferencia('Ciencia Ficción', 'Ciencia Ficción', 0.95))
        self.reglas.append(ReglaInferencia('Fantasia', 'Fantasia', 0.95))

        # Reglas para RITMO
        self.reglas.append(ReglaInferencia('Ritmo Rápido', 'Rápido', 0.85)) 
        self.reglas.append(ReglaInferencia('Ritmo Lento', 'Lento', 0.80)) 

        # Reglas para COMPLEJIDAD
        self.reglas.append(ReglaInferencia('Complejidad Alta', 'Alta', 0.90)) 
        self.reglas.append(ReglaInferencia('Complejidad Media', 'Media', 0.85))
        self.reglas.append(ReglaInferencia('Complejidad Baja', 'Baja', 0.70)) 

        # Reglas para MOTIVACIÓN
        self.reglas.append(ReglaInferencia('Motivación_Evadir', 'Evadir', 0.70))
        self.reglas.append(ReglaInferencia('Motivación_Aprender', 'Aprender', 0.75))
        self.reglas.append(ReglaInferencia('Motivación_Emocional', 'Emocional', 0.80))
        
        # Reglas para COMPROMISO
        self.reglas.append(ReglaInferencia('Compromiso_Corto', 'Corto', 0.60))
        self.reglas.append(ReglaInferencia('Compromiso_Medio', 'Medio', 0.65))
        self.reglas.append(ReglaInferencia('Compromiso_Largo', 'Largo', 0.60))
        
    def inferir_recomendaciones(self, respuestas_usuario):
        """Implementa el Encadenamiento Hacia Adelante con Ponderación (FC)."""
        puntajes_libros = {}
        trazabilidad = []
        
        # 1. Proceso de Inferencia
        for respuesta in respuestas_usuario:
            for regla in self.reglas:
                if regla.respuesta_usuario == respuesta:
                    trazabilidad.append(f"Regla Activada: {regla.respuesta_usuario} -> {regla.atributo_esperado} (FC: {regla.fc})")

                    atributo_buscado = regla.atributo_esperado
                    fc = regla.fc
                    
                    # 2. Búsqueda y Ponderación en la Base de Hechos (Libros JSON)
                    for libro in self.libros:
                        # Mapeamos los atributos para facilitar la búsqueda
                        atributos_libro = [
                            libro['Atributo_1_Genero'],
                            libro['Atributo_2_Ritmo'],
                            libro['Atributo_3_Complejidad'],
                            libro['Atributo_4_Motivacion'],
                            libro['Atributo_5_Compromiso']
                        ]
                        
                        if atributo_buscado in atributos_libro:
                            libro_id = libro['ID_Libro']
                            titulo = libro['Titulo']
                            rating_base = libro['Rating_Base']
                            
                            puntuacion_regla = fc
                            # Sumamos el puntaje de la regla al rating base (inicial o acumulado)
                            # Usamos el rating_base como puntaje inicial solo si el libro no tiene puntaje previo.
                            if libro_id not in puntajes_libros:
                                puntajes_libros[libro_id] = rating_base
                                
                            puntajes_libros[libro_id] += puntuacion_regla

                            trazabilidad.append(f"  |-> Acumulando: Libro '{titulo}' recibió +{fc}. Total: {puntajes_libros[libro_id]:.2f}")

        # 3. Clasificación y Salida
        recomendaciones_ordenadas = sorted(
            puntajes_libros.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        
        # 4. Obtener la información completa de los libros recomendados
        recomendaciones_finales = []
        for libro_id, puntaje in recomendaciones_ordenadas[:2]:
            libro_info = next((l for l in self.libros if l['ID_Libro'] == libro_id), None)
            if libro_info:
                recomendaciones_finales.append({
                    "ID_Libro": libro_id,
                    "Titulo": libro_info['Titulo'],
                    "Autor": libro_info['Autor'],
                    "Ruta_Imagen": libro_info['Ruta_Imagen'],
                    "Puntaje_Total": puntaje
                })

        return recomendaciones_finales, trazabilidad