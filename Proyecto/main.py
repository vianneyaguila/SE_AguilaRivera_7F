# ==================================
# 3. main.py (Punto de Entrada y Prototipado)
# ==================================
import pandas as pd
import sqlite3
import os
from motor_inferencia import MotorRecomendacion

# --- CONFIGURACIÓN DE RUTAS Y VARIABLES CLAVE ---

# Obtiene la ruta del directorio actual (asegura que la BD se guarde aquí)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# Nombres de archivos (¡USANDO EL NOMBRE CORTO Y LA EXTENSIÓN .xlsx!)
EXCEL_FILENAME = 'libros_datos.xlsx' 
DB_FILENAME = 'sistema_experto_libros.db'

# Rutas COMPLETAS y ABSOLUTAS
EXCEL_FILE = os.path.join(BASE_DIR, EXCEL_FILENAME)
DB_FILE = os.path.join(BASE_DIR, DB_FILENAME) 

# Nombres de las columnas de tu Excel para el mapeo (¡AJUSTAR ESTO A TU DATASET!)
# Sugerencia basada en datasets comunes:
COLS_MAPEO = {
    'book_id': 'ID_Libro', 
    'title': 'Titulo', 
    'authors': 'Autor',
    'average_rating': 'Rating_Base', # Usado como FC inicial y para Complejidad
    'Category': 'Atributo_1_Genero' # ASUME QUE TIENES UNA COLUMNA LLAMADA 'Category'
}


def cargar_datos_iniciales(excel_file, db_file):
    """Carga los datos del Excel (xlsx) a la tabla LIBROS en SQLite."""
    try:
        conn = sqlite3.connect(db_file)
        
        # 1. Leer el Excel (¡USANDO read_excel!)
        df_libros = pd.read_excel(excel_file, sheet_name=0, engine='openpyxl') 
        
        # 2. Preparación y Mapeo de Columnas
        df_libros = df_libros.rename(columns=COLS_MAPEO)
        
        # --- CREACIÓN DE ATRIBUTOS SINTÉTICOS (Ritmo y Complejidad) ---
        # Si el rating es alto, asumimos que es 'Rapido' y 'Baja' complejidad (popular)
        df_libros['Atributo_2_Ritmo'] = df_libros['Rating_Base'].apply(
            lambda x: 'Rapido' if x > 4.2 else 'Lento'
        )
        df_libros['Atributo_3_Complejidad'] = df_libros['Rating_Base'].apply(
            lambda x: 'Baja' if x > 4.2 else 'Alta'
        )
        
        # Rellenar valores nulos y asegurar que los atributos sean strings
        df_libros['Atributo_1_Genero'] = df_libros['Atributo_1_Genero'].fillna('Desconocido').astype(str)

        # Solo usar las columnas necesarias
        df_libros_final = df_libros[list(COLS_MAPEO.values()) + ['Atributo_2_Ritmo', 'Atributo_3_Complejidad']].copy()
        
        # 3. Crear y Llenar la tabla LIBROS (Requisito: Conexión a BD)
        df_libros_final.to_sql('LIBROS', conn, if_exists='replace', index=False)
        print(f"✅ Tabla 'LIBROS' creada y llenada con {len(df_libros_final)} registros.")

    except FileNotFoundError:
        print(f"❌ ERROR: Archivo '{excel_file}' no encontrado. ¡Asegúrate de renombrar tu Excel a {EXCEL_FILENAME}!")
    except Exception as e:
        print(f"❌ Error durante la carga de Excel o la BD: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


def simular_encuesta():
    """Simula la interfaz con preguntas cerradas."""
    print("\n--- INICIO DE LA ENCUESTA (Preguntas Cerradas) ---")
    
    # P1: Género
    resp_genero = input("1. ¿Qué ambientación prefiere? [1]Fantasía / [2]Contemporánea: ")
    respuesta1 = 'Mundos inventados (Fantasia)' if resp_genero == '1' else 'Realidad actual (Contemporanea)'
    
    # P2: Ritmo
    resp_ritmo = input("2. ¿Prefiere acción rápida o desarrollo lento? [1]Rápido / [2]Lento: ")
    respuesta2 = 'Ritmo Rápido' if resp_ritmo == '1' else 'Ritmo Lento'

    # P3: Complejidad
    resp_complejidad = input("3. ¿Busca un reto intelectual? [1]Sí (Alta) / [2]No (Baja): ")
    respuesta3 = 'Complejidad Alta' if resp_complejidad == '1' else 'Complejidad Baja'

    return [respuesta1, respuesta2, respuesta3]


if __name__ == "__main__":
    
    # 1. Carga inicial de Hechos
    cargar_datos_iniciales(EXCEL_FILE, DB_FILE)
    
    # 2. Inicialización del Motor
    motor = MotorRecomendacion(db_file=DB_FILE)
    if not motor.conectar_bd():
        exit()
        
    motor.cargar_reglas()
        
    # 3. Interacción y Respuestas
    respuestas_del_usuario = simular_encuesta()

    # 4. INICIO DE LA INFERENCIA 
    print("\n==============================================")
    print("          INICIO DEL MOTOR DE INFERENCIA      ")
    print("==============================================")
    
    recomendaciones, trazabilidad = motor.inferir_recomendaciones(respuestas_del_usuario)

    # 5. Demostración de Trazabilidad (Para el Video)
    print("\n--- DEMOSTRACIÓN DE INFERENCIA (TRAZABILIDAD) ---")
    for linea in trazabilidad:
        print(linea)
    print("-------------------------------------------------")
    
    # 6. Mostrar Resultados Finales
    print("\n✅ RECOMENDACIONES FINALES (TOP 3) ✅")
    if recomendaciones:
        for libro_id, puntaje in recomendaciones:
            cursor = motor.conn.cursor()
            cursor.execute(f"SELECT Titulo, Autor FROM LIBROS WHERE ID_Libro = {libro_id}")
            resultado = cursor.fetchone()
            
            if resultado:
                titulo, autor = resultado
                print(f"-> {titulo} ({autor}) | Puntaje de Afinidad Total: {puntaje:.2f}")
            else:
                print(f"Libro ID {libro_id} no encontrado.")
    else:
        print("No se encontraron coincidencias suficientes. Intente con otras respuestas.")
        
    motor.conn.close()