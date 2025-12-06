# ==================================
# 2. motor_inferencia.py (Motor de Inferencia y Conexión a BD)
# ==================================
import sqlite3
from modelo_conocimiento import ReglaInferencia 

class MotorRecomendacion:
    """Clase principal que gestiona la conexión a BD y la lógica de inferencia."""
    def __init__(self, db_file='sistema_experto_libros.db'):
        self.db_file = db_file
        self.reglas = []
        self.conn = None

    def conectar_bd(self):
        """Establece la conexión a la base de datos SQLite."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"✅ Conectado a la BD: {self.db_file}")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error de conexión a BD: {e}")
            return False

    def cargar_reglas(self):
        """
        Carga las reglas de inferencia. 
        Para simplificar la demostración, se cargan manualmente aquí en lugar de una tabla extra.
        """
        # REGLAS DE CONOCIMIENTO (Ejemplo SÓLIDO para Recomendación)
        self.reglas.append(ReglaInferencia('Mundos inventados (Fantasia)', 'Fantasia', 0.95)) # R1
        self.reglas.append(ReglaInferencia('Realidad actual (Contemporanea)', 'Contemporaneo', 0.95)) # R2

        self.reglas.append(ReglaInferencia('Ritmo Rápido', 'Rapido', 0.85)) # R3
        self.reglas.append(ReglaInferencia('Ritmo Lento', 'Lento', 0.80)) # R4

        self.reglas.append(ReglaInferencia('Complejidad Alta', 'Alta', 0.90)) # R5
        self.reglas.append(ReglaInferencia('Complejidad Baja', 'Baja', 0.70)) # R6

        print(f"✅ {len(self.reglas)} reglas de inferencia cargadas en el motor.")
        
    def inferir_recomendaciones(self, respuestas_usuario):
        """
        Implementa el Encadenamiento Hacia Adelante con Ponderación (FC).
        Muestra la trazabilidad para la demostración del video.
        """
        puntajes_libros = {}
        trazabilidad = []

        for respuesta in respuestas_usuario:
            for regla in self.reglas:
                # 1. Disparo de Reglas (IF la respuesta del usuario coincide con la condición de la regla)
                if regla.respuesta_usuario == respuesta:
                    trazabilidad.append(f"Regla Activada: {regla.respuesta_usuario} -> {regla.atributo_esperado} (FC: {regla.fc})")

                    # 2. Búsqueda en la Base de Hechos (Tabla LIBROS)
                    atributo = regla.atributo_esperado
                    fc = regla.fc
                    
                    # Consulta SQL: Busca libros cuyo Género o Ritmo coincidan con el atributo esperado.
                    query = f"""
                    SELECT ID_Libro, Titulo, Rating_Base 
                    FROM LIBROS 
                    WHERE Atributo_1_Genero = '{atributo}' OR Atributo_2_Ritmo = '{atributo}'
                    """
                    
                    cursor = self.conn.cursor()
                    cursor.execute(query)
                    libros_coincidentes = cursor.fetchall()
                    
                    # 3. Ponderación y Acumulación (Inferencia Compleja)
                    for libro_id, titulo, rating_base in libros_coincidentes:
                        # Puntuación Acumulada = Suma de FCs + Rating Base del libro
                        # El rating base actúa como un FC inicial para ese libro.
                        puntuacion_regla = fc
                        puntajes_libros[libro_id] = puntajes_libros.get(libro_id, rating_base) + puntuacion_regla
                        
                        trazabilidad.append(f"  |-> Acumulando: Libro '{titulo}' recibió +{fc} por esta regla. Puntuación Acumulada: {puntajes_libros[libro_id]:.2f}")

        # 4. Clasificación y Salida
        recomendaciones_ordenadas = sorted(
            puntajes_libros.items(), 
            key=lambda item: item[1], 
            reverse=True
        )

        # Retorna el TOP 3 y la traza para el video
        return recomendaciones_ordenadas[:3], trazabilidad