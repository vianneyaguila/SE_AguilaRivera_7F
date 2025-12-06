# ==================================
# 3. main.py (Punto de Entrada y Prototipado)
# ==================================
import pandas as pd
import sqlite3
import os
from motor_inferencia import MotorRecomendacion

# Variables de configuración (AJUSTA ESTO SEGÚN TU EXCEL)
EXCEL_FILE = 'mi_dataset_libros.xlsx' 
DB_FILE = 'sistema_experto_libros.db'
# Nombres de las columnas de tu Excel que mapean a los atributos
GENERO_COL = 'Genero' # Columna de Género de tu Excel
RITMO_COL = 'Ritmo'   # Columna de Ritmo de tu Excel

def cargar_datos_iniciales(excel_file, db_file):
    """Carga los datos del Excel a la tabla LIBROS en SQLite."""
    try:
        conn = sqlite3.connect(db_file)
        
        # 1. Leer el Excel (Asegúrate de tener instalado pandas y openpyxl)
        df_libros = pd.read_excel(excel_file, sheet_name=0) 
        
        # 2. Preparación y Mapeo de Columnas
        df_libros = df_libros.rename(columns={
            'book_id': 'ID_Libro', 
            'title': 'Titulo', 
            'authors': 'Autor',
            'average_rating': 'Rating_Base', # Usado como FC inicial
            GENERO_COL: 'Atributo_1_Genero', 
            RITMO_COL: 'Atributo_2_Ritmo' 
        })
        
        # Rellenar valores nulos y asegurar que los atributos sean strings
        df_libros['Atributo_1_Genero'] = df_libros['Atributo_1_Genero'].fillna('Desconocido').astype(str)
        df_libros['Atributo_2_Ritmo'] = df_libros['Atributo_2_Ritmo'].fillna('Desconocido').astype(str)
        
        # Solo usar las columnas necesarias
        df_libros_final = df_libros[['ID_Libro', 'Titulo', 'Autor', 'Rating_Base', 
                                     'Atributo_1_Genero', 'Atributo_2_Ritmo']].copy()
        
        # 3. Crear y Llenar la tabla LIBROS (Requisito: Conexión a BD)
        df_libros_final.to_sql('LIBROS', conn, if_exists='replace', index=False)
        print(f"✅ Tabla 'LIBROS' creada y llenada con {len(df_libros_final)} registros.")

    except FileNotFoundError:
        print(f"❌ ERROR: Archivo '{excel_file}' no encontrado. ¡Ajusta la variable EXCEL_FILE!")
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
        exit() # Termina si no hay conexión
        
    motor.cargar_reglas()
        
    # 3. Interacción y Respuestas
    respuestas_del_usuario = simular_encuesta()

    # 4. INICIO DE LA INFERENCIA (Punto central para el video)
    print("\n==============================================")
    print("          INICIO DEL MOTOR DE INFERENCIA      ")
    print("==============================================")
    
    # Ejecuta el motor y obtiene el top 3 y la traza
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
            # Consulta final para obtener el título completo
            cursor = motor.conn.cursor()
            cursor.execute(f"SELECT Titulo, Autor FROM LIBROS WHERE ID_Libro = {libro_id}")
            resultado = cursor.fetchone()
            
            if resultado:
                titulo, autor = resultado
                # Puntuación Total Máxima (ej: 0.95+0.85+0.90 + 5.0) para un cálculo simple de porcentaje.
                # Aquí el puntaje es la suma directa de las reglas activadas + el rating base.
                print(f"-> {titulo} ({autor}) | Puntaje de Afinidad Total: {puntaje:.2f}")
            else:
                print(f"Libro ID {libro_id} no encontrado.")
    else:
        print("No se encontraron coincidencias suficientes. Intente con otras respuestas.")
        
    motor.conn.close()