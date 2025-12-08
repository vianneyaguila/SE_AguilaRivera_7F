# =========================================================
# SISTEMA EXPERTO DE RECOMENDACIÓN DE LIBROS (VERSION CORREGIDA CON CARPETA IMAGENES)
# =========================================================
import os
import customtkinter as ctk 
from PIL import Image 

# Importamos la clase del motor real
try:
    from motor_inferencia import MotorRecomendacion
except ImportError:
    print("Error: No se encontró motor_inferencia.py. Asegúrate de que el archivo existe.")
    exit()

# --- CONFIGURACIÓN GLOBAL DE COLORES Y FUENTE ---
COLOR_PRIMARIO = "#D48B9A"       
COLOR_SECUNDARIO = "#A59097"     
COLOR_FONDO_TARJETA = "white"    
COLOR_TEXTO_OSCURO = "#000000"   
COLOR_FONDO_INACTIVO = "#ECE0E4"

FUENTE_PRINCIPAL = "Arial"   
IMAGEN_FONDO = "fondo_app.jpg" 

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
IMAGENES_DIR = os.path.join(BASE_DIR, 'Imágenes') # <-- RUTA DE IMAGENES CORREGIDA

# ----------------------------------------------------------------------
## 1. DEFINICIÓN DE CLASES DE LA INTERFAZ
# ----------------------------------------------------------------------

class IntroFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent") 
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.label_container = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20) 
        self.label_container.grid(row=0, column=0, pady=(100, 50), sticky="n") 
        
        self.label = ctk.CTkLabel(self.label_container, 
                                  text="Encuentra tu próxima\ngran lectura", 
                                  font=controller.font_intro, 
                                  text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, padx=20, pady=10)
        
        self.start_button = ctk.CTkButton(self, 
                                          text="Comenzar", 
                                          command=controller.go_next,
                                          fg_color=COLOR_PRIMARIO, 
                                          hover_color="#B57A86", 
                                          text_color="white", 
                                          font=controller.font_button,
                                          width=250, height=55, corner_radius=28) 
        self.start_button.grid(row=1, column=0, pady=(50, 50), sticky="s")

    def update_buttons(self):
        pass

class BaseQuestionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure((0, 2), weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        
        self.content_card = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20)
        self.content_card.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=(30, 0))
        self.content_card.grid_columnconfigure(0, weight=1)
        
        self.question_container = ctk.CTkFrame(self.content_card, fg_color=COLOR_FONDO_TARJETA, corner_radius=10)
        self.question_container.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.question_container.grid_columnconfigure(0, weight=1)
        
        self.options_container = ctk.CTkFrame(self.content_card, fg_color="transparent")
        self.options_container.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.options_container.grid_columnconfigure(0, weight=1)

        self.back_button = ctk.CTkButton(self, text="←", 
                                         width=50, height=50, corner_radius=25, 
                                         fg_color=COLOR_PRIMARIO, 
                                         hover_color="#B57A86",
                                         text_color="white",
                                         font=ctk.CTkFont(size=24, weight="bold"),
                                         command=controller.go_back)

        self.back_button.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="w")
        
        self.next_button = ctk.CTkButton(self, text="→", 
                                         width=50, height=50, corner_radius=25, 
                                         fg_color=COLOR_PRIMARIO, 
                                         hover_color="#B57A86",
                                         text_color="white",
                                         font=ctk.CTkFont(size=24, weight="bold"),
                                         command=controller.go_next)

        self.next_button.grid(row=1, column=2, padx=20, pady=(20, 0), sticky="e")
    
    def select_option(self, value, variable, buttons_list):
        variable.set(value)
        
        for btn_info in buttons_list:
            button_widget = btn_info['widget']
            button_value = btn_info['value']
            
            if button_value == value:
                button_widget.configure(fg_color=COLOR_PRIMARIO, 
                                        text_color="white",
                                        hover_color="#B57A86") 
            else:
                button_widget.configure(fg_color=COLOR_SECUNDARIO, 
                                        text_color=COLOR_TEXTO_OSCURO,
                                        hover_color="#918187")
                
    def update_buttons(self):
        if self.controller.current_step == 1:
            self.back_button.grid_remove() 
        else:
            self.back_button.grid()
        
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
        self.option_buttons = [] 
        
        for i, opcion in enumerate(opciones):
            btn = ctk.CTkButton(self.options_container, 
                                 text=opcion,
                                 command=lambda val=opcion: self.select_option(val, controller.var_genero, self.option_buttons),
                                 width=300, height=50, 
                                 corner_radius=25, 
                                 fg_color=COLOR_SECUNDARIO, 
                                 text_color=COLOR_TEXTO_OSCURO,
                                 font=controller.font_opcion)
            
            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")
            
            self.option_buttons.append({'widget': btn, 'value': opcion})

    def update_buttons(self):
        super().update_buttons()
        current_value = self.controller.var_genero.get()
        if current_value:
            self.select_option(current_value, self.controller.var_genero, self.option_buttons) 

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
        
        self.option_buttons = []

        for i, (text, value) in enumerate(opciones):
            btn = ctk.CTkButton(self.options_container, 
                                 text=text,
                                 command=lambda val=value: self.select_option(val, controller.var_ritmo, self.option_buttons),
                                 width=300, height=50, 
                                 corner_radius=25, 
                                 fg_color=COLOR_SECUNDARIO, 
                                 text_color=COLOR_TEXTO_OSCURO,
                                 font=controller.font_opcion)
            
            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")
            self.option_buttons.append({'widget': btn, 'value': value})
            
    def update_buttons(self):
        super().update_buttons()
        current_value = self.controller.var_ritmo.get()
        if current_value:
            self.select_option(current_value, self.controller.var_ritmo, self.option_buttons) 

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
        
        self.option_buttons = []
        
        for i, (text, value) in enumerate(opciones):
            btn = ctk.CTkButton(self.options_container, 
                                 text=text,
                                 command=lambda val=value: self.select_option(val, controller.var_complejidad, self.option_buttons),
                                 width=300, height=50, 
                                 corner_radius=25, 
                                 fg_color=COLOR_SECUNDARIO, 
                                 text_color=COLOR_TEXTO_OSCURO,
                                 font=controller.font_opcion)
            
            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")
            self.option_buttons.append({'widget': btn, 'value': value})
            
    def update_buttons(self):
        super().update_buttons()
        current_value = self.controller.var_complejidad.get()
        if current_value:
            self.select_option(current_value, self.controller.var_complejidad, self.option_buttons) 

class MotivationFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, 
                                  text="¿Cuál es tu principal motivación\nal abrir un libro?", 
                                  font=controller.font_pregunta, 
                                  text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, padx=10, pady=5)
        
        opciones = [
            ("Busco una total evasión y sumergirme en un mundo diferente.", "Motivación_Evadir"), 
            ("Quiero aprender algo nuevo o reflexionar sobre un tema real.", "Motivación_Aprender"),
            ("Busco una fuerte conexión emocional y personajes memorables.", "Motivación_Emocional")
        ]
        
        self.option_buttons = []
        for i, (text, value) in enumerate(opciones):
            btn = ctk.CTkButton(self.options_container, 
                                 text=text,
                                 command=lambda val=value: self.select_option(val, controller.var_motivacion, self.option_buttons),
                                 width=300, 
                                 height=60, 
                                 corner_radius=25, 
                                 fg_color=COLOR_SECUNDARIO, 
                                 text_color=COLOR_TEXTO_OSCURO,
                                 font=controller.font_opcion)
            
            btn._text_label.configure(wraplength=280, justify="center") 

            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")
            self.option_buttons.append({'widget': btn, 'value': value})

    def update_buttons(self):
        super().update_buttons()
        current_value = self.controller.var_motivacion.get()
        if current_value:
            self.select_option(current_value, self.controller.var_motivacion, self.option_buttons) 

class CommitmentFrame(BaseQuestionFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.label = ctk.CTkLabel(self.question_container, 
                                  text="¿Qué tipo de compromiso de lectura\nprefieres en extensión?", 
                                  font=controller.font_pregunta, 
                                  text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, padx=10, pady=5)
        
        opciones = [
            ("Algo autocontenido y rápido (novela corta o cuento).", "Compromiso_Corto"), 
            ("Una novela completa pero independiente (sin sagas).", "Compromiso_Medio"),
            ("Una saga o serie de varios volúmenes para sumergirme por largo tiempo.", "Compromiso_Largo")
        ]
        
        self.option_buttons = []
        for i, (text, value) in enumerate(opciones):
            btn = ctk.CTkButton(self.options_container, 
                                 text=text,
                                 command=lambda val=value: self.select_option(val, controller.var_compromiso, self.option_buttons),
                                 width=300, 
                                 height=60, 
                                 corner_radius=25, 
                                 fg_color=COLOR_SECUNDARIO, 
                                 text_color=COLOR_TEXTO_OSCURO,
                                 font=controller.font_opcion)
            
            btn._text_label.configure(wraplength=280, justify="center") 

            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")
            self.option_buttons.append({'widget': btn, 'value': value})

    def update_buttons(self):
        super().update_buttons()
        current_value = self.controller.var_compromiso.get()
        if current_value:
            self.select_option(current_value, self.controller.var_compromiso, self.option_buttons) 

class BookCard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_TARJETA, corner_radius=15) 
        self.controller = controller
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Marco para la imagen (se cargará dinámicamente)
        self.image_label = ctk.CTkLabel(self, text="", fg_color=COLOR_SECUNDARIO, width=80, height=110, corner_radius=10)
        self.image_label.grid(row=0, column=0, padx=15, pady=15, sticky="nsw")
        
        # Contenedor de texto
        self.text_container = ctk.CTkFrame(self, fg_color="transparent")
        self.text_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.text_container.grid_columnconfigure(0, weight=1)
        
        # Etiquetas de texto
        self.title_label = ctk.CTkLabel(self.text_container, text="", justify="left", 
                                         font=controller.font_card_title, text_color=COLOR_TEXTO_OSCURO)
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 2))
        
        self.info_label = ctk.CTkLabel(self.text_container, text="", justify="left", 
                                        font=controller.font_card_info, text_color=COLOR_TEXTO_OSCURO)
        self.info_label.grid(row=1, column=0, sticky="w")
        
    def update_image(self, image_filename):
        """Carga y muestra la imagen del libro."""
        try:
            # 💡 Cambio Clave: Usar IMAGENES_DIR para construir la ruta
            image_path = os.path.join(IMAGENES_DIR, image_filename) 
            img = Image.open(image_path).resize((80, 110))
            ctk_img = ctk.CTkImage(light_image=img, size=(80, 110))
            
            self.image_label.image = ctk_img
            
            self.image_label.configure(image=ctk_img, text="", fg_color="transparent")
        except Exception:
            self.image_label.configure(image=None, text="No Image", fg_color=COLOR_SECUNDARIO)
            
    def update_info(self, titulo, autor, puntaje):
        self.title_label.configure(text=f"Título: {titulo}")
        info_text = (f"Autor: {autor}\n"
                     f"Afinidad Total: {puntaje:.2f}")
        self.info_label.configure(text=info_text)

class ResultFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent") 
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        
        self.result_card = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20)
        self.result_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.result_card.grid_columnconfigure(0, weight=1)
        
        self.label_titulo = ctk.CTkLabel(self.result_card, text="Recomendación Personalizada", 
                                         font=controller.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label_titulo.grid(row=0, column=0, pady=(20, 10))
        
        self.cards_container = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.cards_container.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.cards_container.grid_columnconfigure(0, weight=1)
        
        self.book_card_1 = BookCard(self.cards_container, controller)
        self.book_card_2 = BookCard(self.cards_container, controller)
        
        self.book_card_1.grid(row=0, column=0, padx=0, pady=10, sticky="ew")
        self.book_card_2.grid(row=1, column=0, padx=0, pady=10, sticky="ew")
        
        self.start_over_button = ctk.CTkButton(self.result_card, text="Volver a Empezar", 
                                                 command=self.reset_app,
                                                 fg_color=COLOR_PRIMARIO, 
                                                 hover_color="#B57A86", 
                                                 text_color="white", 
                                                 font=controller.font_button,
                                                 width=250, height=55, corner_radius=28) 
                                                     
        self.start_over_button.grid(row=2, column=0, padx=10, pady=(30, 20))


    def update_results(self, recomendaciones):
        """Recibe una lista de diccionarios con la información completa de los libros."""
        card_widgets = [self.book_card_1, self.book_card_2]
        
        if not recomendaciones:
            self.book_card_1.update_info("No se encontró una recomendación adecuada.", "Motor inactivo", 0.0)
            self.book_card_1.update_image("no_image.jpg")
            self.book_card_2.grid_remove()
            return

        for i, libro_info in enumerate(recomendaciones[:2]):
            if i < len(card_widgets):
                card = card_widgets[i]
                
                # Accedemos a los datos directamente del diccionario
                titulo = libro_info['Titulo']
                autor = libro_info['Autor']
                puntaje = libro_info['Puntaje_Total']
                ruta_imagen = libro_info['Ruta_Imagen']
                
                card.update_info(titulo, autor, puntaje)
                card.update_image(ruta_imagen)
                card.grid()
            
        if len(recomendaciones) < 2:
            self.book_card_2.grid_remove()
        elif len(recomendaciones) >= 2:
            self.book_card_2.grid(row=1, column=0, padx=0, pady=10, sticky="ew")

    def reset_app(self):
        self.controller.current_step = 0
        self.controller.var_genero.set(None) 
        self.controller.var_ritmo.set(None)
        self.controller.var_complejidad.set(None) 
        self.controller.var_motivacion.set(None) 
        self.controller.var_compromiso.set(None) 
        self.controller.show_frame("IntroFrame")


# ----------------------------------------------------------------------
## 2. CLASE PRINCIPAL DE LA APLICACIÓN
# ----------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self, bg_image_name):
        super().__init__()
        
        self.title("SERL - Sistema Experto de Recomendación")
        self.geometry("550x650")  
        self.resizable(False, False) 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        ctk.set_appearance_mode("Light") 

        # --- IMAGEN DE FONDO ---
        self.bg_image = None
        self.bg_label = None
        try:
            # Si el fondo_app.jpg también está en 'Imágenes', usa IMAGENES_DIR aquí también.
            # Asumiendo que 'fondo_app.jpg' sigue en la carpeta principal por ahora.
            image_path = os.path.join(BASE_DIR, bg_image_name) 
            img = Image.open(image_path).resize((550, 650))
            self.bg_image = ctk.CTkImage(light_image=img, size=img.size)
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1) 
            self.configure(fg_color="transparent") 
        except Exception:
            self.configure(fg_color=COLOR_FONDO_INACTIVO) 
            
        # --- CONFIGURACIÓN DEL MOTOR ---
        self.motor = MotorRecomendacion()
        self.motor.cargar_reglas()
        self.motor.cargar_conocimiento_json()

        # --- FUENTES ---
        self.font_pregunta = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=22, weight="bold")
        self.font_opcion = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="normal")
        self.font_button = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        self.font_card_title = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        self.font_card_info = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=14, weight="normal")
        self.font_intro = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=30, weight="bold")
        
        # --- VARIABLES DE CONTROL ---
        self.current_step = 0 
        self.max_steps = 5 
        self.var_genero = ctk.StringVar(value=None) 
        self.var_ritmo = ctk.StringVar(value=None)
        self.var_complejidad = ctk.StringVar(value=None)
        self.var_motivacion = ctk.StringVar(value=None) 
        self.var_compromiso = ctk.StringVar(value=None) 

        # --- CONTENEDOR PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent") 
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew") 
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # --- SISTEMA DE GESTIÓN DE PÁGINAS ---  
        self.frames = {}
        
        for F in (IntroFrame, GenreFrame, RhythmFrame, ComplexityFrame, MotivationFrame, CommitmentFrame, ResultFrame):
            frame = F(self.main_container, self) 
            self.frames[F.__name__] = frame 
            frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Inicia la interfaz
        self.show_frame("IntroFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        if hasattr(frame, 'update_buttons'):
            frame.update_buttons()
            
    # --- NAVEGACIÓN ---
    def go_next(self):
        if self.current_step == 0:
            self.current_step = 1
            self.show_frame("GenreFrame")
            return
        elif self.current_step == 1:
            if self.var_genero.get() in [None, ""]: return
            self.current_step = 2
            self.show_frame("RhythmFrame")
        elif self.current_step == 2:
            if self.var_ritmo.get() in [None, ""]: return
            self.current_step = 3
            self.show_frame("ComplexityFrame")
        elif self.current_step == 3:
            if self.var_complejidad.get() in [None, ""]: return
            self.current_step = 4
            self.show_frame("MotivationFrame") 
        elif self.current_step == 4:
            if self.var_motivacion.get() in [None, ""]: return
            self.current_step = 5
            self.show_frame("CommitmentFrame") 
        elif self.current_step == 5: 
            if self.var_compromiso.get() in [None, ""]: return
            self.ejecutar_inferencia()
            return
        
    def go_back(self):
        if self.current_step == 2:
            self.current_step = 1
            self.show_frame("GenreFrame")
        elif self.current_step == 3:
            self.current_step = 2
            self.show_frame("RhythmFrame")
        elif self.current_step == 4:
            self.current_step = 3
            self.show_frame("ComplexityFrame") 
        elif self.current_step == 5:
            self.current_step = 4
            self.show_frame("MotivationFrame") 
        
    def ejecutar_inferencia(self):
        respuestas_usuario = [
            self.var_genero.get(),
            self.var_ritmo.get(),
            self.var_complejidad.get(),
            self.var_motivacion.get(),
            self.var_compromiso.get()
        ]
        
        recomendaciones_data, _ = self.motor.inferir_recomendaciones(respuestas_usuario) 
        
        result_frame = self.frames["ResultFrame"]
        result_frame.update_results(recomendaciones_data)
        
        self.current_step = 6 
        self.show_frame("ResultFrame")


# ----------------------------------------------------------------------
## 3. EJECUCIÓN DEL SISTEMA
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = App(bg_image_name=IMAGEN_FONDO)
    app.mainloop()