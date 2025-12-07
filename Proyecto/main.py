# ==================================
# main.py (Versión de Alta Fidelidad con Assets .PNG y .JPG)
# ==================================
import sqlite3
import os
import customtkinter as ctk 
from motor_inferencia import MotorRecomendacion
from PIL import Image, ImageTk 

# --- CONFIGURACIÓN GLOBAL ---
COLOR_PRIMARIO = "#A59097"       
COLOR_FONDO_TARJETA = "#ECE0E4"  
COLOR_TEXTO_OSCURO = "#000000"   
COLOR_FONDO_APLICACION = "#E0E0E0" 
FUENTE_PRINCIPAL = "Arial"   

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_FILENAME = 'sistema_experto_libros.db'
DB_FILE = os.path.join(BASE_DIR, DB_FILENAME) 
ASSETS_DIR = os.path.join(BASE_DIR, "assets") 

# --- DATOS DE EJEMPLO DE LIBROS (BASE DE HECHOS) ---
LIBROS_EJEMPLO = [
    ("Orgullo y Prejuicio", "Jane Austen", "Romance", "Lento", "Media", 4.5, "URL_dummy"),
    ("Maus I", "Art Spiegelman", "Comic", "Lento", "Alta", 4.8, "URL_dummy"),
    ("Dune", "Frank Herbert", "Ciencia Ficción", "Lento", "Alta", 4.7, "URL_dummy"),
    ("Harry Potter y la Piedra Filosofal", "J.K. Rowling", "Fantasia", "Rápido", "Baja", 4.7, "URL_dummy"),
    ("Bajo la Misma Estrella", "John Green", "Romance", "Rápido", "Baja", 4.2, "URL_dummy"),
    ("Watchmen", "Alan Moore", "Comic", "Rápido", "Alta", 4.9, "URL_dummy"),
    ("Neuromante", "William Gibson", "Ciencia Ficción", "Rápido", "Media", 4.6, "URL_dummy"),
    ("El Señor de los Anillos", "J.R.R. Tolkien", "Fantasia", "Lento", "Alta", 4.9, "URL_dummy")
]

# --- FUNCIÓN DE CREACIÓN DE BD (SIN CAMBIOS) ---
def crear_y_cargar_bd_libros(db_file, libros_data):
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

        # --- CONFIGURACIÓN DE LA VENTANA ---
        self.title("SERL - Sistema Experto de Recomendación")
        self.geometry("450x750")  
        self.resizable(False, False) 
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color=COLOR_FONDO_APLICACION) 
        ctk.set_appearance_mode("Light") 
        
        # --- CARGA DE ASSETS (AJUSTE DE EXTENSIONES) ---
        self.assets = self._load_all_assets()
        if not self.assets:
             print("ADVERTENCIA: No se pudieron cargar los assets. Verifica la carpeta 'assets'.")
             self.assets = {} 

        # --- CONFIGURACIÓN DEL MOTOR Y VARIABLES (Sin cambios) ---
        self.motor = MotorRecomendacion(db_file=DB_FILE)
        self.motor.conectar_bd()
        self.motor.cargar_reglas()

        self.font_pregunta = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=20, weight="bold")
        self.font_opcion = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="normal")
        self.font_button = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        
        self.current_step = 1 
        self.max_steps = 3 
        
        self.var_genero = ctk.StringVar(value="")
        self.var_ritmo = ctk.StringVar(value="")
        self.var_complejidad = ctk.StringVar(value="")

        # --- CONTENEDOR CENTRAL ---
        self.main_container = ctk.CTkFrame(self, 
                                           fg_color="white", 
                                           corner_radius=40) 
        self.main_container.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # --- SISTEMA DE GESTIÓN DE PÁGINAS ---
        self.frames = {}
        for F in (GenreFrame, RhythmFrame, ComplexityFrame, ResultFrame):
            frame = F(self.main_container, self)
            self.frames[F.__name__] = frame 
            frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            
        self.show_frame("GenreFrame")

    def _load_all_assets(self):
        """Carga todos los assets de imagen del directorio ASSETS_DIR con las extensiones especificadas."""
        assets = {}
        
        # Diccionario de ASSETS de FIGMA y sus nombres de archivo:
        asset_files = {
            'flecha_atras': 'flecha_atras.png',
            'flecha_siguiente': 'flecha_siguiente.png',
            'radio_normal': 'radio_normal.png',         # <<<< USANDO .PNG
            'radio_seleccionado': 'radio_seleccionado.png', # <<<< USANDO .PNG
            'placeholder_book': 'placeholder_book.jpg', # <<<< USANDO .JPG
            'boton_recomendar': 'boton_recomendar.png'
        }
        
        for key, filename in asset_files.items():
            try:
                path = os.path.join(ASSETS_DIR, filename)
                img = Image.open(path)
                
                # Asignar un tamaño por defecto para consistencia
                size = (25, 25) if 'flecha' in key or 'radio' in key else ((150, 50) if 'boton' in key else (150, 200))
                
                assets[key] = ctk.CTkImage(light_image=img.resize(size), 
                                           dark_image=img.resize(size), 
                                           size=size)
            except FileNotFoundError:
                print(f"❌ ERROR: El asset '{filename}' no se encontró en {ASSETS_DIR}")
                return None
            except Exception as e:
                print(f"❌ Error al cargar el asset '{filename}': {e}")
                return None
                
        return assets
    
    # --- Métodos de Navegación y Ejecución (Sin cambios) ---
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        if hasattr(frame, 'update_buttons'):
            frame.update_buttons()

    def go_next(self):
        if self.current_step == 1 and not self.var_genero.get():
             return
        if self.current_step == 2 and not self.var_ritmo.get():
             return
        
        if self.current_step < self.max_steps:
            self.current_step += 1
            if self.current_step == 2:
                self.show_frame("RhythmFrame")
            elif self.current_step == 3:
                self.show_frame("ComplexityFrame")
        elif self.current_step == self.max_steps:
            self.ejecutar_inferencia()

    def go_back(self):
        if self.current_step > 1:
            self.current_step -= 1
            if self.current_step == 1:
                self.show_frame("GenreFrame")
            elif self.current_step == 2:
                self.show_frame("RhythmFrame")
        
    def ejecutar_inferencia(self):
        respuestas_usuario = [
            self.var_genero.get(),
            self.var_ritmo.get(),
            self.var_complejidad.get()
        ]
        
        if not self.var_complejidad.get():
            return

        recomendaciones, trazabilidad = self.motor.inferir_recomendaciones(respuestas_usuario)
        
        result_frame = self.frames["ResultFrame"]
        result_frame.update_results(recomendaciones, trazabilidad)
        
        self.current_step += 1 
        self.show_frame("ResultFrame")


# --- CLASE PERSONALIZADA PARA BOTONES DE RADIO BASADOS EN IMÁGENES ---
class ImageRadioButton(ctk.CTkButton):
    def __init__(self, master, variable, value, text, controller, **kwargs):
        
        self.img_normal = controller.assets.get('radio_normal')
        self.img_seleccionado = controller.assets.get('radio_seleccionado')
        
        self.variable = variable
        self.value = value
        
        super().__init__(master, 
                         text=text, 
                         image=self.img_normal, 
                         command=self._select_option,
                         compound="left", 
                         width=300, 
                         height=50, 
                         corner_radius=15, 
                         fg_color="transparent", 
                         text_color=COLOR_TEXTO_OSCURO,
                         hover_color=COLOR_FONDO_TARJETA, 
                         font=controller.font_opcion, 
                         **kwargs)
        
        self.variable.trace_add("write", self._update_image)
        self._update_image()
        
    def _select_option(self):
        self.variable.set(self.value)

    def _update_image(self, *args):
        if self.variable.get() == self.value:
            self.configure(image=self.img_seleccionado, text_color=COLOR_PRIMARIO) 
        else:
            self.configure(image=self.img_normal, text_color=COLOR_TEXTO_OSCURO)

# --- PANTALLAS DE LA INTERFAZ ---

class BaseQuestionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure((0, 2), weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        
        self.question_container = ctk.CTkFrame(self, fg_color="transparent")
        self.question_container.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=0, pady=(40, 0))
        self.question_container.grid_columnconfigure(0, weight=1)
        
        # Botones de Navegación con Assets de Flecha
        self.back_button = ctk.CTkButton(self, text="", 
                                        image=controller.assets.get('flecha_atras'), 
                                        width=50, height=50, corner_radius=25, 
                                        fg_color="transparent", 
                                        hover_color=COLOR_FONDO_TARJETA, 
                                        command=controller.go_back)
        self.back_button.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="w")
        
        self.next_button = ctk.CTkButton(self, text="", 
                                        image=controller.assets.get('flecha_siguiente'), 
                                        width=50, height=50, corner_radius=25, 
                                        fg_color="transparent", 
                                        hover_color=COLOR_FONDO_TARJETA, 
                                        command=controller.go_next)
        self.next_button.grid(row=1, column=2, padx=10, pady=(20, 0), sticky="e")
    
    def update_buttons(self):
        if self.controller.current_step == 1:
            self.back_button.configure(state="disabled", hover_color="white")
        else:
            self.back_button.configure(state="normal", hover_color=COLOR_FONDO_TARJETA)

class GenreFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, text="¿Qué género o ambientación\nprefiere?", 
                                  font=controller.font_pregunta, text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, pady=(0, 20))
        
        opciones = ["Romance", "Comic", "Ciencia Ficción", "Fantasia"]
        for i, opcion in enumerate(opciones):
            btn = ImageRadioButton(self.question_container, 
                                     controller.var_genero,
                                     opcion,
                                     opcion,
                                     controller)
            btn.grid(row=i + 1, column=0, pady=10, sticky="ew")

class RhythmFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, text="¿Prefiere un ritmo de lectura?", 
                                  font=controller.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label.grid(row=0, column=0, pady=(0, 20))
        
        opciones = [("Acción y giros rápidos", "Ritmo Rápido"), 
                    ("Desarrollo profundo y pausado", "Ritmo Lento")]
        
        for i, (text, value) in enumerate(opciones):
            btn = ImageRadioButton(self.question_container, 
                                     controller.var_ritmo,
                                     value,
                                     text,
                                     controller)
            btn.grid(row=i + 1, column=0, pady=10, sticky="ew")

class ComplexityFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, text="¿Busca un reto intelectual\nen la lectura?", 
                                  font=controller.font_pregunta, text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, pady=(0, 20))
        
        opciones = [("Sí (vocabulario y trama compleja)", "Complejidad Alta"), 
                    ("Intermedia", "Complejidad Media"), 
                    ("No (lectura ligera)", "Complejidad Baja")]
        
        for i, (text, value) in enumerate(opciones):
            btn = ImageRadioButton(self.question_container, 
                                     controller.var_complejidad,
                                     value,
                                     text,
                                     controller)
            btn.grid(row=i + 1, column=0, pady=10, sticky="ew")
        
        # Configurar botón Siguiente como "Recomendar" usando el asset
        self.next_button.configure(text="Recomendar", 
                                  image=controller.assets.get('boton_recomendar'), 
                                  compound="left",
                                  width=150, height=50, corner_radius=15, 
                                  fg_color=COLOR_PRIMARIO, text_color="white", 
                                  hover_color="#89777E", 
                                  font=controller.font_button)
        self.next_button.grid(row=1, column=1, padx=10, pady=(20, 0), sticky="") # Centrar

class ResultFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        
        self.label_titulo = ctk.CTkLabel(self, text="Recomendación Personalizada", 
                                         font=controller.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label_titulo.grid(row=0, column=0, pady=(20, 10))
        
        self.book_card = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20, width=400)
        self.book_card.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.book_card.grid_columnconfigure(0, weight=0) 
        self.book_card.grid_columnconfigure(1, weight=1) 
        
        self.image_label = ctk.CTkLabel(self.book_card, text="", 
                                        image=controller.assets.get('placeholder_book')) 
        self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        
        self.book_info = ctk.CTkLabel(self.book_card, text="Selecciona tus preferencias...", justify="left", 
                                      font=controller.font_opcion, text_color=COLOR_TEXTO_OSCURO)
        self.book_info.grid(row=0, column=1, padx=10, pady=10, sticky="nsw")

        self.start_over_button = ctk.CTkButton(self, text="Volver a Empezar", 
                                            command=self.reset_app,
                                            fg_color=COLOR_PRIMARIO, text_color="white", 
                                            hover_color="#89777E", 
                                            font=controller.font_button)
        self.start_over_button.grid(row=2, column=0, padx=10, pady=(10, 5))

        self.label_trazabilidad = ctk.CTkLabel(self, text="Trazabilidad:", font=controller.font_opcion, text_color=COLOR_TEXTO_OSCURO)
        self.label_trazabilidad.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.textbox_trazabilidad = ctk.CTkTextbox(self, height=150, width=400, font=ctk.CTkFont(family="Consolas", size=10))
        self.textbox_trazabilidad.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

    def update_results(self, recomendaciones, trazabilidad):
        self.textbox_trazabilidad.delete("1.0", "end")
        
        if recomendaciones:
            libro_id, puntaje = recomendaciones[0] 
            
            cursor = self.controller.motor.conn.cursor()
            cursor.execute("SELECT Titulo, Autor FROM LIBROS WHERE ID_Libro = ?", (libro_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                titulo, autor = resultado
                
                info_text = (f"Título: {titulo}\nAutor: {autor}\n"
                             f"Afinidad Total: {puntaje:.2f}")
                self.book_info.configure(text=info_text)
                
                self.image_label.configure(image=self.controller.assets.get('placeholder_book'), text="")
            
            self.textbox_trazabilidad.insert("end", "\n--- TRAZABILIDAD DETALLADA ---\n")
            for line in trazabilidad:
                self.textbox_trazabilidad.insert("end", line + "\n")
        else:
            self.book_info.configure(text="No se encontró una recomendación adecuada.")
            self.image_label.configure(image=None, text="Sin Imagen")
            self.textbox_trazabilidad.insert("end", "El motor no activó suficientes reglas.")

    def reset_app(self):
        self.controller.current_step = 1
        self.controller.var_genero.set("")
        self.controller.var_ritmo.set("")
        self.controller.var_complejidad.set("")
        self.controller.show_frame("GenreFrame")
        self.textbox_trazabilidad.delete("1.0", "end")

# --- EJECUCIÓN DEL SISTEMA ---
if __name__ == "__main__":
    crear_y_cargar_bd_libros(DB_FILE, LIBROS_EJEMPLO)
    app = App()
    app.mainloop()