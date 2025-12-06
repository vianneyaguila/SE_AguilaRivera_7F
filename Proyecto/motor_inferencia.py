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
        """Carga las reglas de inferencia (el conocimiento experto)."""
        
        # REGLAS DE CONOCIMIENTO
        self.reglas.append(ReglaInferencia('Mundos inventados (Fantasia)', 'Fantasia', 0.95))
        self.reglas.append(ReglaInferencia('Realidad actual (Contemporanea)', 'Contemporaneo', 0.95))

        self.reglas.append(ReglaInferencia('Ritmo Rápido', 'Rapido', 0.85)) 
        self.reglas.append(ReglaInferencia('Ritmo Lento', 'Lento', 0.80)) 

        self.reglas.append(ReglaInferencia('Complejidad Alta', 'Alta', 0.90)) 
        self.reglas.append(ReglaInferencia('Complejidad Baja', 'Baja', 0.70)) 

        print(f"✅ {len(self.reglas)} reglas de inferencia cargadas en el motor.")
        
    def inferir_recomendaciones(self, respuestas_usuario):
        """
        Implementa el Encadenamiento Hacia Adelante con Ponderación (FC).
        """
        puntajes_libros = {}
        trazabilidad = []
        cursor = self.conn.cursor()

        for respuesta in respuestas_usuario:
            for regla in self.reglas:
                # 1. Disparo de Reglas (Inferencia Sencilla)
                if regla.respuesta_usuario == respuesta:
                    trazabilidad.append(f"Regla Activada: {regla.respuesta_usuario} -> {regla.atributo_esperado} (FC: {regla.fc})")

                    atributo = regla.atributo_esperado
                    fc = regla.fc
                    
                    # 2. Búsqueda en la Base de Hechos (Tabla LIBROS)
                    # Busca libros cuyo Género o Ritmo/Complejidad coincidan con el atributo esperado.
                    query = f"""
                    SELECT ID_Libro, Titulo, Rating_Base 
                    FROM LIBROS 
                    WHERE Atributo_1_Genero = '{atributo}' OR Atributo_2_Ritmo = '{atributo}' OR Atributo_3_Complejidad = '{atributo}'
                    """
                    
                    cursor.execute(query)
                    libros_coincidentes = cursor.fetchall()
                    
                    # 3. Ponderación y Acumulación (Inferencia Compleja)
                    for libro_id, titulo, rating_base in libros_coincidentes:
                        # Puntuación Acumulada = Suma de FCs + Rating Base del libro
                        # El rating_base se agrega aquí como factor inicial de calidad
                        puntuacion_regla = fc
                        puntajes_libros[libro_id] = puntajes_libros.get(libro_id, rating_base) + puntuacion_regla
                        
                        trazabilidad.append(f"  |-> Acumulando: Libro '{titulo}' recibió +{fc} por esta regla. Puntuación Acumulada: {puntajes_libros[libro_id]:.2f}")

        # 4. Clasificación y Salida
        recomendaciones_ordenadas = sorted(
            puntajes_libros.items(), 
            key=lambda item: item[1], 
            reverse=True
        )

        return recomendaciones_ordenadas[:3], trazabilidad