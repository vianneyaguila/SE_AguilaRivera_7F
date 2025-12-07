# ==================================
# 3. main.py (Versión CustomTkinter Estilizada)
# ==================================
import sqlite3
import os
import customtkinter as ctk 
from motor_inferencia import MotorRecomendacion
from PIL import Image # Necesario para manejar imágenes (aunque solo mostramos texto)

# --- CONFIGURACIÓN GLOBAL DE COLORES Y FUENTE ---
COLOR_PRIMARIO = "#A59097" # Color morado/gris (Acento del botón, radio button activo)
COLOR_FONDO_TARJETA = "#ECE0E4" # Color gris/blanco (Fondo de las tarjetas de preguntas)
COLOR_TEXTO_OSCURO = "#333333" # Texto principal
FUENTE_PRINCIPAL = "tllt warp" # Nombre de la fuente de Figma

# Ruta para guardar la BD
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_FILENAME = 'sistema_experto_libros.db'
DB_FILE = os.path.join(BASE_DIR, DB_FILENAME) 

# --- DATOS DE EJEMPLO DE LIBROS (BASE DE HECHOS) ---
# Hechos: Titulo, Autor, Género, Ritmo, Complejidad, Rating, URL_Imagen
LIBROS_EJEMPLO = [
    # Romance
    ("Orgullo y Prejuicio", "Jane Austen", "Romance", "Lento", "Media", 4.5, 
     "https://m.media-amazon.com/images/I/71nI0kH-3mL._SL1500_.jpg"),
    ("Bajo la Misma Estrella", "John Green", "Romance", "Rápido", "Baja", 4.2, 
     "https://m.media-amazon.com/images/I/71mOq73n-1L._SL1500_.jpg"),
    
    # Comics
    ("Maus I", "Art Spiegelman", "Comic", "Lento", "Alta", 4.8, 
     "https://m.media-amazon.com/images/I/71Yy3rG8HdL._SL1500_.jpg"),
    ("Watchmen", "Alan Moore", "Comic", "Rápido", "Alta", 4.9, 
     "https://m.media-amazon.com/images/I/71GqC-M-SdL._SL1500_.jpg"),
     
    # Ciencia Ficción
    ("Dune", "Frank Herbert", "Ciencia Ficción", "Lento", "Alta", 4.7, 
     "https://m.media-amazon.com/images/I/71Z-P5nN8iL._SL1500_.jpg"),
    ("Neuromante", "William Gibson", "Ciencia Ficción", "Rápido", "Media", 4.6, 
     "https://m.media-amazon.com/images/I/61S-r57-qdL._SL1500_.jpg"),
    
    # Fantasía
    ("El Señor de los Anillos", "J.R.R. Tolkien", "Fantasia", "Lento", "Alta", 4.9,
     "https://m.media-amazon.com/images/I/71jN0D2lQ8L._SL1500_.jpg"),
    ("Harry Potter y la Piedra Filosofal", "J.K. Rowling", "Fantasia", "Rápido", "Baja", 4.7,
     "https://m.media-amazon.com/images/I/71gP-l5-i0L._SL1500_.jpg")
]

# --- FUNCIÓN DE CREACIÓN DE BD (SIN CAMBIOS) ---
def crear_y_cargar_bd_libros(db_file, libros_data):
    """Crea la tabla LIBROS en SQLite y la llena con datos."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LIBROS (
                ID_Libro INTEGER PRIMARY KEY AUTOINCREMENT,
                Titulo TEXT NOT NULL,
                Autor TEXT NOT NULL,
                Atributo_1_Genero TEXT NOT NULL,
                Atributo_2_Ritmo TEXT NOT NULL,
                Atributo_3_Complejidad TEXT NOT NULL,
                Rating_Base REAL NOT NULL,
                URL_Imagen TEXT
            );
        """)
        cursor.execute("DELETE FROM LIBROS;")
        for libro in libros_data:
            cursor.execute("""
                INSERT INTO LIBROS (Titulo, Autor, Atributo_1_Genero, Atributo_2_Ritmo, Atributo_3_Complejidad, Rating_Base, URL_Imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, libro)
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error al crear/cargar la BD: {e}")
    finally:
        if conn:
            conn.close()

# --- CLASE PRINCIPAL DE LA APLICACIÓN CustomTkinter ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DE LA VENTANA Y ESTILOS ---
        self.title("SERL - Sistema Experto de Recomendación")
        self.geometry("800x950")
        self.grid_columnconfigure(0, weight=1) 
        
        # Usamos el modo claro, ya que los colores de Figma son claros
        ctk.set_appearance_mode("Light") 
        # Configurar el tema con el color primario para botones/acento
        ctk.set_default_color_theme("blue") # Esto es solo para la estructura interna, pero usamos fg_color para sobrescribir
        
        # Fuentes personalizadas
        self.font_titulo = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=24, weight="bold")
        self.font_pregunta = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        self.font_opcion = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=14)
        
        # --- CONFIGURACIÓN DEL MOTOR ---
        self.motor = MotorRecomendacion(db_file=DB_FILE)
        self.motor.conectar_bd()
        self.motor.cargar_reglas()

        # --- INTERFAZ (Layout y Widgets Estilizados) ---
        
        # 1. Título Principal
        self.label_titulo = ctk.CTkLabel(self, text="Sistema Experto de Recomendación de Libros", 
                                         font=self.font_titulo, text_color=COLOR_TEXTO_OSCURO)
        self.label_titulo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # 2. Contenedor principal de las Preguntas (simula la estructura de tu Figma)
        self.frame_preguntas = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
        self.frame_preguntas.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.frame_preguntas.grid_columnconfigure(0, weight=1)

        # Variables para Radio Buttons
        self.var_ritmo = ctk.StringVar(value="")
        self.var_complejidad = ctk.StringVar(value="")
        
        # 2.1 Género (CTkComboBox)
        self.label_genero = ctk.CTkLabel(self.frame_preguntas, text="1. ¿Qué género o ambientación prefiere?", font=self.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label_genero.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        self.opciones_genero = ["Romance", "Comic", "Ciencia Ficción", "Fantasia"]
        self.dd_genero = ctk.CTkComboBox(self.frame_preguntas, values=self.opciones_genero, width=350, 
                                         fg_color=COLOR_FONDO_TARJETA, button_color=COLOR_PRIMARIO, 
                                         border_color=COLOR_PRIMARIO, text_color=COLOR_TEXTO_OSCURO, font=self.font_opcion)
        self.dd_genero.set("Seleccionar")
        self.dd_genero.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # 2.2 Ritmo (CTkRadioButton)
        self.label_ritmo = ctk.CTkLabel(self.frame_preguntas, text="2. ¿Prefiere un ritmo de lectura?", font=self.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label_ritmo.grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")
        self.rb_ritmo_rapido = ctk.CTkRadioButton(self.frame_preguntas, text="Acción y giros rápidos", variable=self.var_ritmo, value="Ritmo Rápido", 
                                                 fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO, text_color=COLOR_TEXTO_OSCURO, font=self.font_opcion)
        self.rb_ritmo_rapido.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.rb_ritmo_lento = ctk.CTkRadioButton(self.frame_preguntas, text="Desarrollo profundo y pausado", variable=self.var_ritmo, value="Ritmo Lento", 
                                                fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO, text_color=COLOR_TEXTO_OSCURO, font=self.font_opcion)
        self.rb_ritmo_lento.grid(row=4, column=0, padx=20, pady=(5, 15), sticky="w")

        # 2.3 Complejidad (CTkRadioButton)
        self.label_complejidad = ctk.CTkLabel(self.frame_preguntas, text="3. ¿Busca un reto intelectual en la lectura?", font=self.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label_complejidad.grid(row=5, column=0, padx=20, pady=(15, 5), sticky="w")
        self.rb_comp_alta = ctk.CTkRadioButton(self.frame_preguntas, text="Sí (trama compleja)", variable=self.var_complejidad, value="Complejidad Alta", 
                                               fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO, text_color=COLOR_TEXTO_OSCURO, font=self.font_opcion)
        self.rb_comp_alta.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        self.rb_comp_media = ctk.CTkRadioButton(self.frame_preguntas, text="Intermedia", variable=self.var_complejidad, value="Complejidad Media", 
                                                fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO, text_color=COLOR_TEXTO_OSCURO, font=self.font_opcion)
        self.rb_comp_media.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.rb_comp_baja = ctk.CTkRadioButton(self.frame_preguntas, text="No (lectura ligera)", variable=self.var_complejidad, value="Complejidad Baja", 
                                               fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO, text_color=COLOR_TEXTO_OSCURO, font=self.font_opcion)
        self.rb_comp_baja.grid(row=8, column=0, padx=20, pady=(5, 15), sticky="w")

        # 3. Botón de Ejecución (Usando el COLOR_PRIMARIO)
        self.btn_recomendar = ctk.CTkButton(self, text="Recomendar Libro (Ejecutar Sistema Experto)", 
                                            command=self.ejecutar_inferencia,
                                            fg_color=COLOR_PRIMARIO, 
                                            hover_color="#89777E", # Un tono más oscuro para el hover
                                            font=self.font_pregunta)
        self.btn_recomendar.grid(row=2, column=0, padx=20, pady=20)
        
        # 4. Frame de Resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.resultado_frame.grid_columnconfigure(0, weight=1)

        # 4.1 Frame para mostrar las recomendaciones (Libros)
        self.recomendaciones_scroll_frame = ctk.CTkScrollableFrame(self.resultado_frame, label_text="✅ RECOMENDACIONES FINALES (TOP 3)", 
                                                                   label_font=self.font_pregunta)
        self.recomendaciones_scroll_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.recomendaciones_scroll_frame.grid_columnconfigure(0, weight=1)
        
        # 4.2 Textbox para Trazabilidad
        self.label_trazabilidad = ctk.CTkLabel(self.resultado_frame, text="TRAZABILIDAD DE INFERENCIA:", 
                                               font=ctk.CTkFont(family=FUENTE_PRINCIPAL, size=12, weight="bold"))
        self.label_trazabilidad.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.textbox_trazabilidad = ctk.CTkTextbox(self.resultado_frame, height=180, width=700, font=ctk.CTkFont(family="Consolas", size=10))
        self.textbox_trazabilidad.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.textbox_trazabilidad.insert("end", "Presiona el botón para iniciar la recomendación...")


    def ejecutar_inferencia(self):
        """Función que recolecta datos y llama al motor."""
        
        # 1. Recolección de Respuestas
        respuestas_usuario = [
            self.dd_genero.get(),
            self.var_ritmo.get(),
            self.var_complejidad.get()
        ]
        
        # 2. Validación
        if "Seleccionar" in respuestas_usuario or "" in respuestas_usuario:
            self.textbox_trazabilidad.delete("1.0", "end")
            self.textbox_trazabilidad.insert("end", "❌ ERROR: Por favor, seleccione una opción en cada pregunta.")
            return

        # 3. Ejecutar la Inferencia
        recomendaciones, trazabilidad = self.motor.inferir_recomendaciones(respuestas_usuario)
        
        # 4. Mostrar Resultados (Limpiar y actualizar)
        
        # Limpiar el frame de recomendaciones
        for widget in self.recomendaciones_scroll_frame.winfo_children():
            widget.destroy()

        self.textbox_trazabilidad.delete("1.0", "end")
        
        if recomendaciones:
            self.textbox_trazabilidad.insert("end", "Resultados generados exitosamente.\n\n")
            
            row_index = 0
            for libro_id, puntaje in recomendaciones:
                cursor = self.motor.conn.cursor()
                cursor.execute(f"SELECT Titulo, Autor, URL_Imagen FROM LIBROS WHERE ID_Libro = {libro_id}")
                resultado = cursor.fetchone()
                
                if resultado:
                    titulo, autor, url_imagen = resultado
                    
                    # Mostrar resultados en una tarjeta estilizada
                    card = ctk.CTkFrame(self.recomendaciones_scroll_frame, corner_radius=10, fg_color=COLOR_FONDO_TARJETA)
                    card.grid(row=row_index, column=0, padx=10, pady=10, sticky="ew")
                    card.grid_columnconfigure(1, weight=1)

                    # Título y Autor
                    info_text = f"Título: {titulo}\nAutor: {autor}\nAfinidad: {puntaje:.2f}"
                    
                    label_info = ctk.CTkLabel(card, text=info_text, justify="left", font=self.font_opcion, text_color=COLOR_TEXTO_OSCURO)
                    label_info.grid(row=0, column=1, padx=15, pady=10, sticky="w")
                    
                    row_index += 1
                
        else:
            self.textbox_trazabilidad.insert("end", "No se encontraron coincidencias suficientes. Intente con otras respuestas.\n")
            
        # 4.2 Mostrar Trazabilidad
        self.textbox_trazabilidad.insert("end", "\n--- TRAZABILIDAD DETALLADA ---\n")
        for line in trazabilidad:
            self.textbox_trazabilidad.insert("end", line + "\n")


# --- EJECUCIÓN DEL SISTEMA ---
if __name__ == "__main__":
    # 1. Crear y cargar la base de datos
    crear_y_cargar_bd_libros(DB_FILE, LIBROS_EJEMPLO)
    
    # 2. Ejecución de la Interfaz CustomTkinter
    app = App()
    app.mainloop()