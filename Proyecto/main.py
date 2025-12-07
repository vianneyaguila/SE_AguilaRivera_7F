# =========================================================
# SISTEMA EXPERTO DE RECOMENDACIÓN DE LIBROS (REPARADO Y FUNCIONAL)
# Replicando diseño final con fondo de imagen, texto negro y navegación corregida.
# =========================================================
import sqlite3
import os
import customtkinter as ctk 
from PIL import Image, ImageTk 
import random 

# --- DEPENDENCIAS SIMULADAS ---
class MotorRecomendacion:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        
    def conectar_bd(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(f"Error al conectar a la BD: {e}")
            
    def cargar_reglas(self):
        pass

    def inferir_recomendaciones(self, respuestas, num_recomendaciones=2):
        # ... (Lógica de inferencia simulada sin cambios) ...
        if not self.conn:
             return []
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT ID_Libro, Titulo, Autor, Atributo_1_Genero, Atributo_2_Ritmo, Atributo_3_Complejidad, Rating_Base FROM LIBROS")
        libros = cursor.fetchall()
        
        recomendaciones_simuladas = []
        for libro in libros:
            libro_id, titulo, autor, genero, ritmo, complejidad, rating_base = libro
            puntaje = rating_base + random.uniform(0.1, 1.5)
            
            if genero == respuestas[0]: puntaje += 1.0
            if ritmo == respuestas[1]: puntaje += 0.5
            if complejidad == respuestas[2]: puntaje += 0.5
            
            recomendaciones_simuladas.append((libro_id, puntaje))

        recomendaciones_simuladas.sort(key=lambda x: x[1], reverse=True)
        return recomendaciones_simuladas[:num_recomendaciones]

# --- CONFIGURACIÓN GLOBAL DE COLORES Y FUENTE ---
COLOR_PRIMARIO = "#D48B9A"       # Rosa Suave (Botón Volver a Empezar)
COLOR_SECUNDARIO = "#A59097"     # Morado/Gris (Radio Buttons - color interno)
COLOR_FONDO_TARJETA = "white"    # Fondo de las tarjetas de resultado
COLOR_TEXTO_OSCURO = "#000000"   # TODO TEXTO NEGRO
COLOR_HIGHLIGHT = "#FFFFFF"      # Fondo de texto de preguntas (Blanco)
COLOR_FONDO_APLICACION = "#E0E0E0" # Fondo base de la ventana (gris claro)

FUENTE_PRINCIPAL = "Arial"   
IMAGEN_FONDO = "tarjeta_fondo.png.png" 
IMAGEN_PORTADA_PRUEBA = "placeholder_book.jpg" 

# Rutas y Datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_FILENAME = 'sistema_experto_libros_2.db'
DB_FILE = os.path.join(BASE_DIR, DB_FILENAME) 

LIBROS_EJEMPLO = [
    (1, "Orgullo y Prejuicio", "Jane Austen", "Romance", "Ritmo Lento", "Complejidad Media", 4.5),
    (2, "Maus I", "Art Spiegelman", "Comic", "Ritmo Lento", "Complejidad Alta", 4.8),
    (3, "Dune", "Frank Herbert", "Ciencia Ficción", "Ritmo Rápido", "Complejidad Alta", 4.7),
    (6, "Crónicas Marcianas", "Ray Bradbury", "Ciencia Ficción", "Ritmo Rápido", "Complejidad Media", 4.4),
]

def crear_y_cargar_bd_libros(db_file, libros_data):
    # (Función para crear la base de datos, sin cambios)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LIBROS (
                ID_Libro INTEGER PRIMARY KEY,
                Titulo TEXT NOT NULL,
                Autor TEXT NOT NULL,
                Atributo_1_Genero TEXT NOT NULL,
                Atributo_2_Ritmo TEXT NOT NULL,
                Atributo_3_Complejidad TEXT NOT NULL,
                Rating_Base REAL NOT NULL
            );
        """)
        cursor.execute("DELETE FROM LIBROS;")
        for libro in libros_data:
            cursor.execute("""
                INSERT INTO LIBROS (ID_Libro, Titulo, Autor, Atributo_1_Genero, Atributo_2_Ritmo, Atributo_3_Complejidad, Rating_Base)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, libro)
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error al crear/cargar la BD: {e}")
    finally:
        if conn:
            conn.close()

# ----------------------------------------------------------------------
## CLASE PRINCIPAL DE LA APLICACIÓN CustomTkinter
# ----------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURACIÓN DE LA VENTANA ---
        self.title("SERL - Sistema Experto de Recomendación")
        self.geometry("450x750")  
        self.resizable(False, False) 
        self.configure(fg_color=COLOR_FONDO_APLICACION) 
        ctk.set_appearance_mode("Light") 
        
        # --- CONFIGURACIÓN DEL MOTOR ---
        self.motor = MotorRecomendacion(db_file=DB_FILE)
        self.motor.conectar_bd()
        self.motor.cargar_reglas()

        # --- FUENTES ---
        self.font_pregunta = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=22, weight="bold")
        self.font_opcion = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="normal")
        self.font_button = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        self.font_card_title = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        self.font_card_info = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=14, weight="normal")
        self.font_intro = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=30, weight="bold")
        
        # --- VARIABLES DE CONTROL DE PASOS ---
        self.current_step = 0 
        self.max_steps = 3 # 1 (Género), 2 (Ritmo), 3 (Complejidad). Después sigue el resultado.
        
        # --- VARIABLES PARA ALMACENAR RESPUESTAS ---
        # Se inicializan en None para forzar la selección.
        self.var_genero = ctk.StringVar(value=None) 
        self.var_ritmo = ctk.StringVar(value=None)
        self.var_complejidad = ctk.StringVar(value=None)

        # --- CONTENEDOR PRINCIPAL: Tarjeta con IMAGEN DE FONDO ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=30)
        self.main_container.grid(row=0, column=0, padx=40, pady=40, sticky="nsew") 
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Cargar y configurar la imagen de fondo (tarjeta_fondo.png.png)
        self.bg_image = None
        self.bg_label = None
        try:
            image_path = os.path.join(BASE_DIR, IMAGEN_FONDO)
            img = Image.open(image_path).resize((370, 670)) 
            self.bg_image = ctk.CTkImage(light_image=img, size=(370, 670))
            
            self.bg_label = ctk.CTkLabel(self.main_container, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            # Fallback a color sólido si no encuentra la imagen
            print(f"❌ Error al cargar la imagen de fondo: {e}. Usando color sólido.")
            self.main_container.configure(fg_color="#ECE0E4") 
        
        # --- SISTEMA DE GESTIÓN DE PÁGINAS ---
        self.frames = {}
        
        # Solo Intro, 3 Preguntas y Resultado
        for F in (IntroFrame, GenreFrame, RhythmFrame, ComplexityFrame, ResultFrame):
            frame = F(self.main_container, self) 
            self.frames[F.__name__] = frame 
            frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.show_frame("IntroFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        # Asegurar que la imagen de fondo esté detrás del frame actual
        if self.bg_label:
             self.bg_label.tkraise()
        frame.tkraise()
        if hasattr(frame, 'update_buttons'):
            frame.update_buttons()

    def go_next(self):
        # 1. Transición de Intro
        if self.current_step == 0:
            self.current_step = 1
            self.show_frame("GenreFrame")
            return
            
        # 2. Validación y avance de Preguntas
        if self.current_step == 1:
            if self.var_genero.get() in [None, ""]: return # Validación de selección
            self.current_step = 2
            self.show_frame("RhythmFrame")
        
        elif self.current_step == 2:
            if self.var_ritmo.get() in [None, ""]: return
            self.current_step = 3
            self.show_frame("ComplexityFrame")
        
        elif self.current_step == 3: 
            if self.var_complejidad.get() in [None, ""]: return
            # Si estamos en la última pregunta, ejecutamos la inferencia
            self.ejecutar_inferencia()
            return
        
    def go_back(self):
        # Retroceso: solo si estamos en pasos 2 o 3.
        if self.current_step == 2:
            self.current_step = 1
            self.show_frame("GenreFrame")
        elif self.current_step == 3:
            self.current_step = 2
            self.show_frame("RhythmFrame")
        
    def ejecutar_inferencia(self):
        respuestas_usuario = [
            self.var_genero.get(),
            self.var_ritmo.get(),
            self.var_complejidad.get()
        ]
        
        recomendaciones = self.motor.inferir_recomendaciones(respuestas_usuario, num_recomendaciones=2) 
        
        result_frame = self.frames["ResultFrame"]
        result_frame.update_results(recomendaciones)
        
        self.current_step = 4 # Paso de resultado
        self.show_frame("ResultFrame")
        
# ----------------------------------------------------------------------
## PANTALLAS DE LA INTERFAZ
# ----------------------------------------------------------------------

class IntroFrame(ctk.CTkFrame):
    """Pantalla de bienvenida."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor para el texto que simula la forma curva de la portada
        self.label_container = ctk.CTkFrame(self, fg_color=COLOR_HIGHLIGHT, corner_radius=20)
        self.label_container.grid(row=0, column=0, pady=(150, 50), sticky="n")
        
        self.label = ctk.CTkLabel(self.label_container, 
                                 text="Encuentra tu próxima\ngran lectura", 
                                 font=controller.font_intro, 
                                 text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, padx=20, pady=10)
        
        # Botón de inicio
        self.start_button = ctk.CTkButton(self, 
                                          text="Comenzar", 
                                          command=controller.go_next,
                                          fg_color=COLOR_PRIMARIO, 
                                          hover_color="#B57A86", 
                                          text_color="white", 
                                          font=controller.font_button,
                                          width=200, height=50, corner_radius=25) 
        self.start_button.grid(row=1, column=0, pady=(50, 50), sticky="s")

    def update_buttons(self):
        pass

class BaseQuestionFrame(ctk.CTkFrame):
    """Clase base para las preguntas, gestionando navegación y diseño."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure((0, 2), weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        
        # Contenedor principal de la pregunta (tarjeta blanca)
        self.content_card = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20)
        self.content_card.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=(50, 0))
        self.content_card.grid_columnconfigure(0, weight=1)
        
        # Contenedor de la pregunta con efecto "subrayador" (Blanco)
        self.question_container = ctk.CTkFrame(self.content_card, fg_color=COLOR_HIGHLIGHT, corner_radius=10)
        self.question_container.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.question_container.grid_columnconfigure(0, weight=1)
        
        # Contenedor para las opciones
        self.options_container = ctk.CTkFrame(self.content_card, fg_color="transparent")
        self.options_container.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.options_container.grid_columnconfigure(0, weight=1)

        # --- BOTÓN ATRÁS (←) ---
        self.back_button = ctk.CTkButton(self, text="←", 
                                         width=50, height=50, corner_radius=25, 
                                         fg_color="transparent", 
                                         hover_color="#CCCCCC",
                                         text_color=COLOR_TEXTO_OSCURO,
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         command=controller.go_back)

        self.back_button.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="w")
        
        # --- BOTÓN SIGUIENTE (→) ---
        self.next_button = ctk.CTkButton(self, text="→", 
                                         width=50, height=50, corner_radius=25, 
                                         fg_color="transparent", 
                                         hover_color="#CCCCCC",
                                         text_color=COLOR_TEXTO_OSCURO,
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         command=controller.go_next)

        self.next_button.grid(row=1, column=2, padx=10, pady=(20, 0), sticky="e")
    
    def update_buttons(self):
        # Ocultar el botón de regreso en el paso 1
        if self.controller.current_step == 1:
            self.back_button.grid_remove() 
        else:
            self.back_button.grid()
        
        # El botón de siguiente siempre está visible en las preguntas
        self.next_button.grid()

class GenreFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, 
                                 text="¿Qué género o ambientación\nprefieres?", 
                                 font=controller.font_pregunta, 
                                 text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, padx=10, pady=5)
        
        opciones = ["Romance", "Comic", "Ciencia Ficción", "Fantasia"]
        for i, opcion in enumerate(opciones):
            btn = ctk.CTkRadioButton(self.options_container, 
                                     text=opcion,
                                     variable=controller.var_genero,
                                     value=opcion,
                                     width=300, height=50, corner_radius=15, 
                                     fg_color=COLOR_SECUNDARIO, 
                                     hover_color=COLOR_PRIMARIO,
                                     border_color=COLOR_SECUNDARIO, # Borde del círculo
                                     text_color=COLOR_TEXTO_OSCURO,
                                     font=controller.font_opcion)
            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")

class RhythmFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, 
                                 text="¿Prefieres un ritmo de lectura?", 
                                 font=controller.font_pregunta, 
                                 text_color=COLOR_TEXTO_OSCURO)
        self.label.grid(row=0, column=0, padx=10, pady=5)
        
        opciones = [("Acción y giros rápidos", "Ritmo Rápido"), 
                    ("Desarrollo profundo y pausado", "Ritmo Lento")]
        
        for i, (text, value) in enumerate(opciones):
            btn = ctk.CTkRadioButton(self.options_container, 
                                     text=text,
                                     variable=controller.var_ritmo,
                                     value=value,
                                     width=300, height=50, corner_radius=15, 
                                     fg_color=COLOR_SECUNDARIO, 
                                     hover_color=COLOR_PRIMARIO,
                                     border_color=COLOR_SECUNDARIO,
                                     text_color=COLOR_TEXTO_OSCURO,
                                     font=controller.font_opcion)
            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")

class ComplexityFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, 
                                 text="¿Buscas un reto intelectual\nen la lectura?", 
                                 font=controller.font_pregunta, 
                                 text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, padx=10, pady=5)
        
        opciones = [("Sí (vocabulario y trama compleja)", "Complejidad Alta"), 
                    ("Intermedia", "Complejidad Media"), 
                    ("No (lectura ligera)", "Complejidad Baja")]
        
        for i, (text, value) in enumerate(opciones):
            btn = ctk.CTkRadioButton(self.options_container, 
                                     text=text,
                                     variable=controller.var_complejidad,
                                     value=value,
                                     width=300, height=50, corner_radius=15, 
                                     fg_color=COLOR_SECUNDARIO, 
                                     hover_color=COLOR_PRIMARIO,
                                     border_color=COLOR_SECUNDARIO,
                                     text_color=COLOR_TEXTO_OSCURO,
                                     font=controller.font_opcion)
            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")

class BookCard(ctk.CTkFrame):
    """Widget reutilizable para mostrar un libro con portada simulada."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Cargar la imagen de portada simulada
        self.ctk_img = None
        try:
            image_path = os.path.join(BASE_DIR, IMAGEN_PORTADA_PRUEBA)
            img = Image.open(image_path).resize((80, 110))
            self.ctk_img = ctk.CTkImage(light_image=img, size=(80, 110))
            self.image_label = ctk.CTkLabel(self, text="", image=self.ctk_img)
            self.image_label.grid(row=0, column=0, padx=15, pady=15, sticky="nsw")
        except Exception:
            # Fallback: Frame de color (simulando la portada de la captura)
            img_frame = ctk.CTkFrame(self, fg_color=COLOR_SECUNDARIO, width=80, height=110, corner_radius=10)
            img_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsw")
        
        self.text_container = ctk.CTkFrame(self, fg_color="transparent")
        self.text_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.text_container.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.text_container, text="", justify="left", 
                                        font=controller.font_card_title, text_color=COLOR_TEXTO_OSCURO)
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 2))
        
        self.info_label = ctk.CTkLabel(self.text_container, text="", justify="left", 
                                       font=controller.font_card_info, text_color=COLOR_TEXTO_OSCURO)
        self.info_label.grid(row=1, column=0, sticky="w")
        
    def update_info(self, titulo, autor, puntaje):
        """Actualiza la información mostrada en la tarjeta."""
        self.title_label.configure(text=f"Título: {titulo}")
        info_text = (f"Autor: {autor}\n"
                      f"Afinidad Total: {puntaje:.2f}")
        self.info_label.configure(text=info_text)
        
class ResultFrame(ctk.CTkFrame):
    """Muestra las recomendaciones y el botón Volver a Empezar."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent") 
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        
        # Contenedor para el resultado, imitando la tarjeta blanca
        self.result_card = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20)
        self.result_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.result_card.grid_columnconfigure(0, weight=1)
        
        self.label_titulo = ctk.CTkLabel(self.result_card, text="Recomendación Personalizada", 
                                         font=controller.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label_titulo.grid(row=0, column=0, pady=(20, 10))
        
        # Contenedor para las dos tarjetas de libros
        self.cards_container = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.cards_container.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.cards_container.grid_columnconfigure(0, weight=1)
        
        self.book_card_1 = BookCard(self.cards_container, controller)
        self.book_card_2 = BookCard(self.cards_container, controller)
        
        self.book_card_1.grid(row=0, column=0, padx=0, pady=10, sticky="ew")
        self.book_card_2.grid(row=1, column=0, padx=0, pady=10, sticky="ew")
        
        # --- BOTÓN VOLVER A EMPEZAR (Dentro del recuadro principal) ---
        self.start_over_button = ctk.CTkButton(self.result_card, text="Volver a Empezar", 
                                                command=self.reset_app,
                                                fg_color=COLOR_PRIMARIO, 
                                                hover_color="#B57A86", 
                                                text_color="white", 
                                                font=controller.font_button,
                                                width=250, height=50, corner_radius=25) 
                                                    
        self.start_over_button.grid(row=2, column=0, padx=10, pady=(30, 20))


    def update_results(self, recomendaciones):
        """Muestra hasta dos recomendaciones."""
        
        card_widgets = [self.book_card_1, self.book_card_2]
        
        if not recomendaciones:
            self.book_card_1.update_info("No se encontró una recomendación adecuada.", "Motor inactivo", 0.0)
            self.book_card_2.grid_remove()
            return

        for i, (libro_id, puntaje) in enumerate(recomendaciones[:2]):
            if i < len(card_widgets):
                card = card_widgets[i]
                
                cursor = self.controller.motor.conn.cursor()
                cursor.execute("SELECT Titulo, Autor FROM LIBROS WHERE ID_Libro = ?", (libro_id,))
                resultado = cursor.fetchone()
                
                if resultado:
                    titulo, autor = resultado
                    card.update_info(titulo, autor, puntaje)
                    card.grid()
                else:
                    card.update_info(f"Error: Libro ID {libro_id} no encontrado.", "", 0.0)
                    card.grid_remove()
            
        if len(recomendaciones) < 2:
            self.book_card_2.grid_remove()
        elif len(recomendaciones) >= 2:
            self.book_card_2.grid(row=1, column=0, padx=0, pady=10, sticky="ew")

    def reset_app(self):
        self.controller.current_step = 0
        # Resetear las variables de respuesta a None
        self.controller.var_genero.set(None) 
        self.controller.var_ritmo.set(None)
        self.controller.var_complejidad.set(None)
        self.controller.show_frame("IntroFrame")

# --- EJECUCIÓN DEL SISTEMA ---
if __name__ == "__main__":
    crear_y_cargar_bd_libros(DB_FILE, LIBROS_EJEMPLO)
    app = App()
    app.mainloop()
