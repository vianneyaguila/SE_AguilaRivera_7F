# =================================================================================
# 1. motor_inferencia.py (Motor de Inferencia y Base de Conocimiento JSON)
# =================================================================================
import json           # Módulo para trabajar con archivos JSON (la Base de Hechos/Conocimiento).
import os             # Módulo para interactuar con el sistema operativo (manejo de rutas).
from modelo_conocimiento import ReglaInferencia # Importa la clase de regla que definimos antes.
import random         # Módulo importado (aunque no se usa en la lógica final de inferencia, puede ser para funciones futuras).

# --- CONFIGURACIÓN DE RUTA ---
# Obtiene el directorio base del script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# Define la ruta completa al archivo JSON de la base de conocimiento.
CONOCIMIENTO_FILE = os.path.join(BASE_DIR, 'base_conocimiento.json')

class MotorRecomendacion:
    """Clase principal que gestiona la base de conocimiento JSON y la lógica de inferencia."""
    def __init__(self):
        # Lista vacía que almacenará los objetos ReglaInferencia.
        self.reglas = []
        # Lista vacía que almacenará los diccionarios de libros cargados desde el JSON (Base de Hechos).
        self.libros = [] 

    def cargar_conocimiento_json(self):
        """Carga los datos de los libros (Base de Hechos) desde el archivo JSON."""
        try:
            # Abre y lee el archivo JSON.
            with open(CONOCIMIENTO_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Extrae la lista de libros del diccionario cargado. Si 'libros' no existe, usa una lista vacía.
            self.libros = data.get('libros', []) 
            # print(f"✅ {len(self.libros)} libros cargados desde JSON.") # Mensaje de depuración.
            return True
        except FileNotFoundError:
            print(f"❌ Error: El archivo {CONOCIMIENTO_FILE} no fue encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"❌ Error: El archivo JSON no es válido.")
            return False

    def cargar_reglas(self):
        """Carga las reglas de inferencia (el conocimiento experto)."""
        # Limpia cualquier regla precargada.
        self.reglas.clear()

        # --- DEFINICIÓN DE REGLAS DE ALTO NIVEL ---
        # Por cada respuesta posible en la GUI, se crea una ReglaInferencia que mapea 
        # esa respuesta a un atributo del libro con un Factor de Certeza (FC) específico.
        
        # Reglas para GÉNERO (FC alto, pues el género es crucial)
        self.reglas.append(ReglaInferencia('Romance', 'Romance', 0.95))
        self.reglas.append(ReglaInferencia('Comic', 'Comic', 0.95))
        self.reglas.append(ReglaInferencia('Ciencia Ficción', 'Ciencia Ficción', 0.95))
        self.reglas.append(ReglaInferencia('Fantasia', 'Fantasia', 0.95))

        # Reglas para RITMO (FC ligeramente menor)
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
        
        # Reglas para COMPROMISO (FC más bajo, ya que es menos determinante que el género/ritmo)
        self.reglas.append(ReglaInferencia('Compromiso_Corto', 'Corto', 0.60))
        self.reglas.append(ReglaInferencia('Compromiso_Medio', 'Medio', 0.65))
        self.reglas.append(ReglaInferencia('Compromiso_Largo', 'Largo', 0.60))
        
    def inferir_recomendaciones(self, respuestas_usuario):
        """
        Implementa el Encadenamiento Hacia Adelante con Ponderación (FC). 
        
        Evalúa las respuestas del usuario contra la base de reglas para puntuar los libros.
        :param respuestas_usuario: Lista de cadenas con las opciones elegidas por el usuario.
        :return: Lista de diccionarios con la información de los libros recomendados y una lista de trazabilidad.
        """
        # Diccionario para almacenar la puntuación acumulada de cada libro: {ID_Libro: Puntaje_Total}
        puntajes_libros = {}
        # Lista para registrar qué reglas se activaron y por qué (trazabilidad del razonamiento).
        trazabilidad = []
        
        # 1. Proceso de Inferencia (Iteración sobre las respuestas del usuario)
        for respuesta in respuestas_usuario:
            # Por cada respuesta del usuario, busca qué reglas de la Base de Reglas se activan.
            for regla in self.reglas:
                # Condición de activación de la regla (Encadenamiento Hacia Adelante)
                if regla.respuesta_usuario == respuesta:
                    # Registra la activación de la regla para la trazabilidad.
                    trazabilidad.append(f"Regla Activada: {regla.respuesta_usuario} -> {regla.atributo_esperado} (FC: {regla.fc})")

                    atributo_buscado = regla.atributo_esperado
                    fc = regla.fc
                    
                    # 2. Búsqueda y Ponderación en la Base de Hechos (Libros JSON)
                    # Una vez que una regla se activa, se aplica su conclusión a todos los libros.
                    for libro in self.libros:
                        # Extraemos los atributos relevantes del libro en una lista para facilitar la búsqueda.
                        atributos_libro = [
                            libro['Atributo_1_Genero'],
                            libro['Atributo_2_Ritmo'],
                            libro['Atributo_3_Complejidad'],
                            libro['Atributo_4_Motivacion'],
                            libro['Atributo_5_Compromiso']
                        ]
                        
                        # Si el atributo buscado por la regla está presente en el libro, se puntúa.
                        if atributo_buscado in atributos_libro:
                            libro_id = libro['ID_Libro']
                            titulo = libro['Titulo']
                            # El 'Rating_Base' actúa como un puntaje inicial o de popularidad.
                            rating_base = libro['Rating_Base'] 
                            
                            puntuacion_regla = fc
                            
                            # Inicialización del puntaje del libro: si el libro no tiene puntaje, 
                            # se inicializa con su Rating_Base.
                            if libro_id not in puntajes_libros:
                                puntajes_libros[libro_id] = rating_base
                                
                            # Acumulación: Sumamos el Factor de Certeza de la regla activada al puntaje total.
                            puntajes_libros[libro_id] += puntuacion_regla

                            trazabilidad.append(f"  |-> Acumulando: Libro '{titulo}' recibió +{fc}. Total: {puntajes_libros[libro_id]:.2f}")

        # 3. Clasificación y Salida
        # Ordenamos los libros en orden descendente por su puntaje acumulado.
        recomendaciones_ordenadas = sorted(
            puntajes_libros.items(), # puntajes_libros.items() devuelve [(id, puntaje), ...]
            key=lambda item: item[1], # La clave de ordenamiento es el puntaje (item[1]).
            reverse=True # Orden descendente (el más alto primero).
        )
        
        # 4. Obtener la información completa de los libros recomendados
        recomendaciones_finales = []
        # Tomamos solo las 2 mejores recomendaciones (los dos primeros elementos).
        for libro_id, puntaje in recomendaciones_ordenadas[:2]: 
            # Busca la información completa del libro en la lista original 'self.libros'.
            libro_info = next((l for l in self.libros if l['ID_Libro'] == libro_id), None)
            
            if libro_info:
                # Estructura el diccionario final con el puntaje total.
                recomendaciones_finales.append({
                    "ID_Libro": libro_id,
                    "Titulo": libro_info['Titulo'],
                    "Autor": libro_info['Autor'],
                    "Ruta_Imagen": libro_info['Ruta_Imagen'],
                    "Puntaje_Total": puntaje # Puntaje total (Rating_Base + suma de FC).
                })

        # Devuelve la lista de las 2 mejores recomendaciones y el registro de la inferencia.
        return recomendaciones_finales, trazabilidad