# =========================================================
# SISTEMA EXPERTO DE RECOMENDACIÓN DE LIBROS (VERSION CORREGIDA CON CARPETA IMAGENES)
# =========================================================
import os  # Módulo para interactuar con el sistema operativo, usado para manejar rutas de archivos.
import customtkinter as ctk  # Biblioteca para crear la GUI (interfaz de usuario) con un look moderno.
from PIL import Image  # Módulo Pillow, usado para abrir, redimensionar y manipular imágenes.

# Importamos la clase del motor real
try:
    # Intenta importar la lógica del sistema experto que contiene las reglas y el conocimiento.
    from motor_inferencia import MotorRecomendacion
except ImportError:
    # Muestra un error si el archivo del motor no se encuentra y termina la aplicación.
    print("Error: No se encontró motor_inferencia.py. Asegúrate de que el archivo existe.")
    exit()

# --- CONFIGURACIÓN GLOBAL DE COLORES Y FUENTE ---
COLOR_PRIMARIO = "#D48B9A"       # Color principal (rosa/malva), usado para botones seleccionados o énfasis.
COLOR_SECUNDARIO = "#A59097"     # Color secundario (gris malva), usado para botones inactivos.
COLOR_FONDO_TARJETA = "white"    # Color de fondo de los cuadros de contenido (tarjetas).
COLOR_TEXTO_OSCURO = "#000000"   # Color estándar para el texto.
COLOR_FONDO_INACTIVO = "#ECE0E4" # Color de fondo si no se puede cargar la imagen de fondo.

FUENTE_PRINCIPAL = "Arial"   # Tipo de fuente base.
IMAGEN_FONDO = "fondo_app.jpg"  # Nombre del archivo de imagen de fondo.

# Rutas del proyecto
# Obtiene el directorio base donde se ejecuta el script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# Define la ruta corregida al directorio de imágenes.
IMAGENES_DIR = os.path.join(BASE_DIR, 'Imágenes') # <-- RUTA DE IMAGENES CORREGIDA

# ----------------------------------------------------------------------
## 1. DEFINICIÓN DE CLASES DE LA INTERFAZ
# ----------------------------------------------------------------------

class IntroFrame(ctk.CTkFrame):
    """Primer frame (pantalla) de la aplicación. Muestra el título y un botón para comenzar."""
    def __init__(self, parent, controller):
        # Inicializa el frame, haciéndolo transparente para que se vea el fondo de la ventana principal.
        super().__init__(parent, fg_color="transparent") 
        self.controller = controller  # Referencia a la clase principal App (el controlador).
        self.grid_columnconfigure(0, weight=1)  # Configura la cuadrícula para centrar el contenido.
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor para la etiqueta del título (simula una tarjeta blanca flotante).
        self.label_container = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20) 
        # Lo posiciona en la parte superior central (n) con margen.
        self.label_container.grid(row=0, column=0, pady=(100, 50), sticky="n") 
        
        # Etiqueta de bienvenida con el texto y la fuente definidos en el controlador.
        self.label = ctk.CTkLabel(self.label_container, 
                                  text="Encuentra tu próxima\ngran lectura", 
                                  font=controller.font_intro, 
                                  text_color=COLOR_TEXTO_OSCURO, justify="center")
        self.label.grid(row=0, column=0, padx=20, pady=10)
        
        # Botón para iniciar el cuestionario.
        self.start_button = ctk.CTkButton(self, 
                                          text="Comenzar", 
                                          # Llama al método de navegación go_next en el controlador.
                                          command=controller.go_next,
                                          fg_color=COLOR_PRIMARIO, 
                                          hover_color="#B57A86", 
                                          text_color="white", 
                                          font=controller.font_button,
                                          width=250, height=55, corner_radius=28) 
        # Posiciona el botón en la parte inferior central (s).
        self.start_button.grid(row=1, column=0, pady=(50, 50), sticky="s")

    def update_buttons(self):
        """Método placeholder, no hace nada en la pantalla de inicio."""
        pass

class BaseQuestionFrame(ctk.CTkFrame):
    """Clase base que define la estructura común para todas las pantallas de preguntas."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        # Configuración de la cuadrícula para centrar el contenido.
        self.grid_columnconfigure((0, 2), weight=1)  # Columnas laterales flexibles para espaciado.
        self.grid_columnconfigure(1, weight=1)  # Columna central para el contenido principal.
        
        # Contenedor principal de la pregunta (la tarjeta flotante).
        self.content_card = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20)
        # Se extiende por las 3 columnas y ocupa el espacio disponible.
        self.content_card.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=(30, 0))
        self.content_card.grid_columnconfigure(0, weight=1)
        
        # Contenedor para el texto de la pregunta.
        self.question_container = ctk.CTkFrame(self.content_card, fg_color=COLOR_FONDO_TARJETA, corner_radius=10)
        self.question_container.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.question_container.grid_columnconfigure(0, weight=1)
        
        # Contenedor para los botones de opciones de respuesta.
        self.options_container = ctk.CTkFrame(self.content_card, fg_color="transparent")
        self.options_container.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.options_container.grid_columnconfigure(0, weight=1)

        # Botón de retroceso (izquierda).
        self.back_button = ctk.CTkButton(self, text="←", 
                                         width=50, height=50, corner_radius=25, 
                                         fg_color=COLOR_PRIMARIO, 
                                         hover_color="#B57A86",
                                         text_color="white",
                                         font=ctk.CTkFont(size=24, weight="bold"),
                                         command=controller.go_back)

        self.back_button.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="w")
        
        # Botón de avance (derecha).
        self.next_button = ctk.CTkButton(self, text="→", 
                                         width=50, height=50, corner_radius=25, 
                                         fg_color=COLOR_PRIMARIO, 
                                         hover_color="#B57A86",
                                         text_color="white",
                                         font=ctk.CTkFont(size=24, weight="bold"),
                                         command=controller.go_next)

        self.next_button.grid(row=1, column=2, padx=20, pady=(20, 0), sticky="e")
    
    def select_option(self, value, variable, buttons_list):
        """
        Lógica para manejar la selección de una opción (radio button estilizado).
        Establece el valor en la variable de control y actualiza el color de los botones.
        """
        variable.set(value)
        
        for btn_info in buttons_list:
            button_widget = btn_info['widget']
            button_value = btn_info['value']
            
            if button_value == value:
                # Botón seleccionado: Color primario.
                button_widget.configure(fg_color=COLOR_PRIMARIO, 
                                        text_color="white",
                                        hover_color="#B57A86") 
            else:
                # Otros botones: Color secundario/inactivo.
                button_widget.configure(fg_color=COLOR_SECUNDARIO, 
                                        text_color=COLOR_TEXTO_OSCURO,
                                        hover_color="#918187")
                
    def update_buttons(self):
        """Controla la visibilidad del botón de retroceso."""
        if self.controller.current_step == 1:
            self.back_button.grid_remove() # Oculta el botón de retroceso en el primer paso de pregunta.
        else:
            self.back_button.grid() # Muestra el botón de retroceso en los demás pasos.
        
        self.next_button.grid() # El botón de avance siempre está visible en las preguntas.

# --- Frame de Pregunta: Género ---
class GenreFrame(BaseQuestionFrame):
    """Pregunta sobre el género o ambientación preferida."""
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
            # Crea un botón para cada opción.
            btn = ctk.CTkButton(self.options_container, 
                                   text=opcion,
                                   # El command llama a select_option, pasando el valor y la variable de control var_genero.
                                   command=lambda val=opcion: self.select_option(val, controller.var_genero, self.option_buttons),
                                   width=300, height=50, 
                                   corner_radius=25, 
                                   fg_color=COLOR_SECUNDARIO, 
                                   text_color=COLOR_TEXTO_OSCURO,
                                   font=controller.font_opcion)
            
            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")
            # Almacena el widget y su valor para que select_option pueda referenciarlos.
            self.option_buttons.append({'widget': btn, 'value': opcion})

    def update_buttons(self):
        super().update_buttons()
        current_value = self.controller.var_genero.get()
        # Vuelve a aplicar el estilo si ya se había seleccionado una opción antes de navegar de vuelta.
        if current_value:
            self.select_option(current_value, self.controller.var_genero, self.option_buttons) 

# --- Frame de Pregunta: Ritmo ---
class RhythmFrame(BaseQuestionFrame):
    """Pregunta sobre el ritmo de lectura preferido (rápido o lento)."""
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

# --- Frame de Pregunta: Complejidad ---
class ComplexityFrame(BaseQuestionFrame):
    """Pregunta sobre la complejidad intelectual deseada."""
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

# --- Frame de Pregunta: Motivación ---
class MotivationFrame(BaseQuestionFrame):
    """Pregunta sobre la motivación principal para leer."""
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
            
            # Configura el envoltorio de texto (wraplength) para que el texto largo quepa.
            btn._text_label.configure(wraplength=280, justify="center") 

            btn.grid(row=i + 1, column=0, pady=8, sticky="ew")
            self.option_buttons.append({'widget': btn, 'value': value})

    def update_buttons(self):
        super().update_buttons()
        current_value = self.controller.var_motivacion.get()
        if current_value:
            self.select_option(current_value, self.controller.var_motivacion, self.option_buttons) 

# --- Frame de Pregunta: Compromiso (Extensión) ---
class CommitmentFrame(BaseQuestionFrame):
    """Pregunta sobre el compromiso de extensión de lectura (corta, media, saga)."""
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

# --- Tarjeta de Resultado de Libro ---
class BookCard(ctk.CTkFrame):
    """Componente visual individual para mostrar la carátula y datos de un libro recomendado."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_TARJETA, corner_radius=15) 
        self.controller = controller
        # Configuración de la cuadrícula: columna 0 (imagen) no flexible, columna 1 (texto) flexible.
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
            # 💡 Cambio Clave: Usar IMAGENES_DIR para construir la ruta al archivo.
            image_path = os.path.join(IMAGENES_DIR, image_filename) 
            # Abre y redimensiona la imagen usando PIL.
            img = Image.open(image_path).resize((80, 110))
            # Convierte la imagen PIL a un formato de imagen compatible con ctk.
            ctk_img = ctk.CTkImage(light_image=img, size=(80, 110))
            
            self.image_label.image = ctk_img
            
            # Configura la etiqueta para mostrar la imagen.
            self.image_label.configure(image=ctk_img, text="", fg_color="transparent")
        except Exception:
            # En caso de error (imagen no encontrada), muestra un texto de placeholder.
            self.image_label.configure(image=None, text="No Image", fg_color=COLOR_SECUNDARIO)
            
    def update_info(self, titulo, autor, puntaje):
        """Actualiza las etiquetas de texto con la información del libro."""
        self.title_label.configure(text=f"Título: {titulo}")
        info_text = (f"Autor: {autor}\n"
                     f"Afinidad Total: {puntaje:.2f}")
        self.info_label.configure(text=info_text)

# --- Frame de Resultados Finales ---
class ResultFrame(ctk.CTkFrame):
    """Frame que muestra las recomendaciones finales de los libros."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent") 
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        
        # Tarjeta principal de resultados.
        self.result_card = ctk.CTkFrame(self, fg_color=COLOR_FONDO_TARJETA, corner_radius=20)
        self.result_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.result_card.grid_columnconfigure(0, weight=1)
        
        self.label_titulo = ctk.CTkLabel(self.result_card, text="Recomendación Personalizada", 
                                         font=controller.font_pregunta, text_color=COLOR_TEXTO_OSCURO)
        self.label_titulo.grid(row=0, column=0, pady=(20, 10))
        
        # Contenedor para las tarjetas de libros.
        self.cards_container = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.cards_container.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.cards_container.grid_columnconfigure(0, weight=1)
        
        # Instancia de las dos tarjetas de libros.
        self.book_card_1 = BookCard(self.cards_container, controller)
        self.book_card_2 = BookCard(self.cards_container, controller)
        
        self.book_card_1.grid(row=0, column=0, padx=0, pady=10, sticky="ew")
        self.book_card_2.grid(row=1, column=0, padx=0, pady=10, sticky="ew")
        
        # Botón para reiniciar la aplicación.
        self.start_over_button = ctk.CTkButton(self.result_card, text="Volver a Empezar", 
                                               command=self.reset_app,
                                               fg_color=COLOR_PRIMARIO, 
                                               hover_color="#B57A86", 
                                               text_color="white", 
                                               font=controller.font_button,
                                               width=250, height=55, corner_radius=28) 
                                                       
        self.start_over_button.grid(row=2, column=0, padx=10, pady=(30, 20))


    def update_results(self, recomendaciones):
        """Recibe una lista de diccionarios con la información completa de los libros y actualiza las tarjetas."""
        card_widgets = [self.book_card_1, self.book_card_2]
        
        if not recomendaciones:
            # Caso sin resultados: muestra un mensaje de error o inactividad.
            self.book_card_1.update_info("No se encontró una recomendación adecuada.", "Motor inactivo", 0.0)
            self.book_card_1.update_image("no_image.jpg")
            self.book_card_2.grid_remove() # Oculta la segunda tarjeta.
            return

        # Itera sobre las dos primeras recomendaciones (si existen).
        for i, libro_info in enumerate(recomendaciones[:2]):
            if i < len(card_widgets):
                card = card_widgets[i]
                
                # Accedemos a los datos directamente del diccionario.
                titulo = libro_info['Titulo']
                autor = libro_info['Autor']
                puntaje = libro_info['Puntaje_Total']
                ruta_imagen = libro_info['Ruta_Imagen']
                
                card.update_info(titulo, autor, puntaje)
                card.update_image(ruta_imagen)
                card.grid() # Asegura que la tarjeta esté visible.
            
        # Controla la visibilidad de la segunda tarjeta si solo hay una recomendación.
        if len(recomendaciones) < 2:
            self.book_card_2.grid_remove()
        elif len(recomendaciones) >= 2:
            self.book_card_2.grid(row=1, column=0, padx=0, pady=10, sticky="ew")

    def reset_app(self):
        """Reinicia el estado de la aplicación para comenzar un nuevo cuestionario."""
        self.controller.current_step = 0
        # Restablece todas las variables de respuesta a None.
        self.controller.var_genero.set(None) 
        self.controller.var_ritmo.set(None)
        self.controller.var_complejidad.set(None) 
        self.controller.var_motivacion.set(None) 
        self.controller.var_compromiso.set(None) 
        # Vuelve a mostrar la pantalla de introducción.
        self.controller.show_frame("IntroFrame")


# ----------------------------------------------------------------------
## 2. CLASE PRINCIPAL DE LA APLICACIÓN
# ----------------------------------------------------------------------
class App(ctk.CTk):
    """Clase principal que gestiona la ventana, el estado y la navegación."""
    def __init__(self, bg_image_name):
        super().__init__()
        
        self.title("SERL - Sistema Experto de Recomendación")
        self.geometry("550x650")  # Establece el tamaño de la ventana.
        self.resizable(False, False) # Desactiva el redimensionamiento.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        ctk.set_appearance_mode("Light") # Configura el tema claro.

        # --- IMAGEN DE FONDO ---
        self.bg_image = None
        self.bg_label = None
        try:
            # Carga la imagen de fondo, asumiendo que está en BASE_DIR.
            image_path = os.path.join(BASE_DIR, bg_image_name) 
            img = Image.open(image_path).resize((550, 650))
            self.bg_image = ctk.CTkImage(light_image=img, size=img.size)
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            # Coloca la imagen para que cubra toda la ventana.
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1) 
            self.configure(fg_color="transparent") 
        except Exception:
            # Si no se carga la imagen, usa el color de fondo inactivo.
            self.configure(fg_color=COLOR_FONDO_INACTIVO) 
            
        # --- CONFIGURACIÓN DEL MOTOR ---
        self.motor = MotorRecomendacion() # Instancia el motor de inferencia.
        self.motor.cargar_reglas() # Carga las reglas lógicas (e.g., IF genero AND ritmo THEN libro).
        self.motor.cargar_conocimiento_json() # Carga la base de hechos (e.g., la lista de libros).

        # --- FUENTES ---
        self.font_pregunta = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=22, weight="bold")
        self.font_opcion = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="normal")
        self.font_button = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        self.font_card_title = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=16, weight="bold")
        self.font_card_info = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=14, weight="normal")
        self.font_intro = ctk.CTkFont(family=FUENTE_PRINCIPAL, size=30, weight="bold")
        
        # --- VARIABLES DE CONTROL ---
        self.current_step = 0 # Contador para el paso actual (0=Intro, 1-5=Preguntas, 6=Resultado).
        self.max_steps = 5 # Número total de preguntas.
        # Variables de control que almacenan la respuesta del usuario para cada pregunta.
        self.var_genero = ctk.StringVar(value=None) 
        self.var_ritmo = ctk.StringVar(value=None)
        self.var_complejidad = ctk.StringVar(value=None)
        self.var_motivacion = ctk.StringVar(value=None) 
        self.var_compromiso = ctk.StringVar(value=None) 

        # --- CONTENEDOR PRINCIPAL ---
        # Marco transparente que contendrá todas las pantallas (Frames).
        self.main_container = ctk.CTkFrame(self, fg_color="transparent") 
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew") 
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # --- SISTEMA DE GESTIÓN DE PÁGINAS ---  
        self.frames = {} # Diccionario para almacenar las instancias de cada frame por su nombre.
        
        # Itera sobre todas las clases de frame.
        for F in (IntroFrame, GenreFrame, RhythmFrame, ComplexityFrame, MotivationFrame, CommitmentFrame, ResultFrame):
            frame = F(self.main_container, self) # Instancia el frame.
            self.frames[F.__name__] = frame # Almacena la instancia en el diccionario.
            # Coloca todos los frames en la misma posición (se usa tkraise para alternar la vista).
            frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Inicia la interfaz mostrando la pantalla de introducción.
        self.show_frame("IntroFrame")

    def show_frame(self, frame_name):
        """Muestra un frame específico y lo trae al frente."""
        frame = self.frames[frame_name]
        frame.tkraise() # Trae el frame deseado al frente.
        if hasattr(frame, 'update_buttons'):
            # Llama al método update_buttons para actualizar el estado del botón 'atrás'.
            frame.update_buttons()
            
    # --- NAVEGACIÓN ---
    def go_next(self):
        """Avanza al siguiente paso (pregunta) o ejecuta la inferencia si es el último paso."""
        if self.current_step == 0:
            self.current_step = 1
            self.show_frame("GenreFrame")
            return
        elif self.current_step == 1:
            if self.var_genero.get() in [None, ""]: return # Validación: No avanza si no hay selección.
            self.current_step = 2
            self.show_frame("RhythmFrame")
        elif self.current_step == 2:
            if self.var_ritmo.get() in [None, ""]: return # Validación.
            self.current_step = 3
            self.show_frame("ComplexityFrame")
        elif self.current_step == 3:
            if self.var_complejidad.get() in [None, ""]: return # Validación.
            self.current_step = 4
            self.show_frame("MotivationFrame") 
        elif self.current_step == 4:
            if self.var_motivacion.get() in [None, ""]: return # Validación.
            self.current_step = 5
            self.show_frame("CommitmentFrame") 
        elif self.current_step == 5: 
            if self.var_compromiso.get() in [None, ""]: return # Validación.
            self.ejecutar_inferencia() # Último paso: ejecuta la lógica del sistema experto.
            return
        
    def go_back(self):
        """Retrocede al paso (pregunta) anterior."""
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
        """Recopila las respuestas del usuario y pide recomendaciones al motor."""
        respuestas_usuario = [
            self.var_genero.get(),
            self.var_ritmo.get(),
            self.var_complejidad.get(),
            self.var_motivacion.get(),
            self.var_compromiso.get()
        ]
        
        # Llama al método del motor con las respuestas del usuario.
        recomendaciones_data, _ = self.motor.inferir_recomendaciones(respuestas_usuario) 
        
        # Muestra los resultados en el ResultFrame.
        result_frame = self.frames["ResultFrame"]
        result_frame.update_results(recomendaciones_data)
        
        self.current_step = 6 # Establece el paso a Resultados.
        self.show_frame("ResultFrame")


# ----------------------------------------------------------------------
## 3. EJECUCIÓN DEL SISTEMA
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Crea la instancia principal de la aplicación.
    app = App(bg_image_name=IMAGEN_FONDO)
    # Inicia el bucle principal de la GUI.
    app.mainloop()