# ==================================
# 2. motor_inferencia.py (Motor de Inferencia y Conexión a BD)
# ==================================
import sqlite3
from modelo_conocimiento import ReglaInferencia 

class MotorRecomendacion:
    """Clase principal que gestiona la conexión a BD y la lógica de inferencia."""
    def __init__(self, db_file):
        self.db_file = db_file
        self.reglas = []
        self.conn = None

    def conectar_bd(self):
        """Establece la conexión a la base de datos SQLite."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            # print(f"✅ Conectado a la BD: {self.db_file}")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error de conexión a BD: {e}")
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

        # print(f"✅ {len(self.reglas)} reglas de inferencia cargadas en el motor.")
        
    def inferir_recomendaciones(self, respuestas_usuario):
        """Implementa el Encadenamiento Hacia Adelante con Ponderación (FC)."""
        puntajes_libros = {}
        trazabilidad = []
        cursor = self.conn.cursor()

        for respuesta in respuestas_usuario:
            for regla in self.reglas:
                # 1. Disparo de Reglas
                if regla.respuesta_usuario == respuesta:
                    trazabilidad.append(f"Regla Activada: {regla.respuesta_usuario} -> {regla.atributo_esperado} (FC: {regla.fc})")

                    atributo_buscado = regla.atributo_esperado
                    fc = regla.fc
                    
                    # 2. Búsqueda en la Base de Hechos (Busca en los 3 atributos de la tabla LIBROS)
                    query = f"""
                    SELECT ID_Libro, Titulo, Rating_Base 
                    FROM LIBROS 
                    WHERE Atributo_1_Genero = '{atributo_buscado}' 
                       OR Atributo_2_Ritmo = '{atributo_buscado}' 
                       OR Atributo_3_Complejidad = '{atributo_buscado}'
                    """
                    
                    cursor.execute(query)
                    libros_coincidentes = cursor.fetchall()
                    
                    # 3. Ponderación y Acumulación
                    for libro_id, titulo, rating_base in libros_coincidentes:
                        puntuacion_regla = fc
                        puntajes_libros[libro_id] = puntajes_libros.get(libro_id, rating_base) + puntuacion_regla
                        trazabilidad.append(f"  |-> Acumulando: Libro '{titulo}' recibió +{fc}. Total: {puntajes_libros[libro_id]:.2f}")

        # 4. Clasificación y Salida
        recomendaciones_ordenadas = sorted(
            puntajes_libros.items(), 
            key=lambda item: item[1], 
            reverse=True
        )

        return recomendaciones_ordenadas[:3], trazabilidad