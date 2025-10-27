# --- IMPORTACIONES DE LIBRERÍAS ---

import tkinter as tk  # Importa la librería principal de Tkinter para crear la interfaz (GUI)
from tkinter import ttk  # Importa los widgets "tematizados" (más modernos) de Tkinter
from tkinter import messagebox  # Importa las ventanas emergentes (para mensajes de error, victoria, etc.)
import random  # Para elegir al azar la solución secreta
import json  # Para leer y escribir en formato JSON (nuestra base de datos)
from pathlib import Path  # Para manejar rutas de archivos de forma compatible con Windows, Mac y Linux
from PIL import Image, ImageTk  # De la librería Pillow (PIL), para cargar, redimensionar y mostrar imágenes (jpg, png)
import sys # para el entorno ejecutable
import os  # para el entorno ejecutable

# --- FUNCIÓN DE AYUDA PARA ENCONTRAR ARCHIVOS ---
def obtener_ruta_recurso(ruta_relativa):
    """ Obtiene la ruta absoluta al recurso, funciona para .py y para .exe """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        ruta_base = sys._MEIPASS
    except Exception:
        # Si no está "congelado" (es un .py), usa la ruta normal
        ruta_base = os.path.abspath(".")

    return os.path.join(ruta_base, ruta_relativa)

# --- 1. CONFIGURACIÓN DE ESTILO (Colores como los del video) ---
# Define constantes para los colores, facilitando cambiarlos después
BG_COLOR = "#2c2c2c"  # Fondo oscuro (Gris muy oscuro)
FG_COLOR = "#00ff41"  # Texto verde neón (Color principal)
BTN_BG = "#4f4f4f"  # Fondo de botón (Gris medio)
LBL_BG = "#2c2c2c"  # Fondo de etiquetas (Igual al fondo general)
TXT_BG = "#1e1e1e"  # Fondo de cajas de texto (Gris casi negro)
SELECT_BG = "#4a4a4a" # Color de fondo cuando se selecciona un ítem en la lista

# --- 2. LÓGICA DE CARGA DE DATOS ---
# RUTA_BASE ya no es necesaria, usamos la nueva función
RUTA_JSON = Path(obtener_ruta_recurso("misterios_con_imagenes.json"))
RUTA_IMG = Path(obtener_ruta_recurso("img"))

# Diccionario global para guardar las historias finales
# (Podrían estar en el JSON, pero así también es válido para 5 casos)
historias_finales = {
    "Dra. Evelyn Reed": "¡Correcto! La Dra. Reed usó la discusión como distracción. Más tarde, en el Salón VIP, aprovechó la cámara rota para envenenar el café de Thorne, sabiendo que era su única oportunidad de salvar su compañía.",
    "Profesor Kenji Tanaka": "¡Has descubierto la verdad! El Profesor confrontó a Thorne en el escenario. Cuando Thorne se burló de él, Tanaka, ciego de ira, usó la estatuilla limpia de huellas para golpearlo. Las luces fallando cubrieron su huida.",
    "Glitch": "¡Impresionante! 'Glitch' se infiltró en el Demo Lab para plantar la USB. Thorne lo sorprendió. Durante el forcejo, 'Glitch' conectó la USB al terminal personal de Thorne, sobrecargando su marcapasos.",
    "Bryce Wagner": "¡Exacto! Wagner citó a Thorne en el Muelle de Carga con una excusa. Sus 'llamadas urgentes' eran para hackear el dron. Lo soltó sobre Thorne, haciéndolo parecer un accidente trágico para cobrar el seguro.",
    "Chloe Jenkins": "¡Increíble, era ella! Chloe, sabiendo que Thorne la despediría, lo confrontó en la Sala de Servidores. Usó el cable de red robado para estrangularlo, confiando en que el ruido de los servidores ocultaría todo."
}

# --- Función para cargar los datos desde el archivo JSON ---
def cargar_datos(archivo_json):
    """Carga tanto el expediente como los escenarios desde un archivo JSON."""
    try:
        # 'with open' abre el archivo y se asegura de cerrarlo al terminar
        # 'r' = modo lectura, 'encoding='utf-8'' = para que lea acentos y caracteres especiales
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos_completos = json.load(f) # Convierte el texto JSON en un diccionario de Python
            # Devuelve las dos secciones principales de nuestra base de datos
            return datos_completos["expediente"], datos_completos["escenarios"]
    except FileNotFoundError: # Se ejecuta si no encuentra el archivo
        messagebox.showerror("Error Fatal", f"No se encontró el archivo '{archivo_json}'.\nAsegúrate de que esté en la misma carpeta que el script.")
        return None, None
    except Exception as e: # Se ejecuta para cualquier otro error (JSON mal escrito, permisos, etc.)
        messagebox.showerror("Error Fatal", f"Error al leer el archivo JSON: {e}")
        return None, None

# --- Carga inicial de datos al arrancar el programa ---
expediente, lista_escenarios = cargar_datos(RUTA_JSON)

# Si la carga falló (expediente está vacío o no se encontró), cerramos el programa
if not expediente or not lista_escenarios:
    exit() # Termina la ejecución del script

# --- Preparación de datos para el juego ---
# Crea listas simples solo con los nombres (para usarlas en los menús desplegables y listas)
lista_personajes = [p["nombre"] for p in expediente["personajes"]]
lista_armas = [a["nombre"] for a in expediente["armas"]]
lista_locaciones = [l["nombre"] for l in expediente["locaciones"]]

# Crea "mapas" (diccionarios) para buscar RÁPIDAMENTE la información de un ítem por su nombre
# La clave es el nombre (ej: "Dra. Evelyn Reed")
# El valor es una tupla (un conjunto ordenado) de datos: (rol, suceso, imagen)
mapa_personajes = {p["nombre"]: (p["rol"], p["suceso"], p["imagen"]) for p in expediente["personajes"]}
# El valor es una tupla: (suceso, imagen)
mapa_armas = {a["nombre"]: (a["suceso"], a["imagen"]) for a in expediente["armas"]}
# El valor es una tupla: (suceso, imagen) (Aquí estaba el error de 'a' por 'l', ya corregido)
mapa_locaciones = {l["nombre"]: (l["suceso"], l["imagen"]) for l in expediente["locaciones"]}

# --- ¡EL CEREBRO DEL JUEGO! ---
# Elige aleatoriamente 1 de los 5 escenarios de la lista
solucion_secreta = random.choice(lista_escenarios)

# Diccionario global para guardar las referencias de las imágenes
# Tkinter/Pillow a veces "pierde" las imágenes si no se guarda una referencia global a ellas.
image_references = {} 

# --- 3. CLASE PRINCIPAL DE LA APLICACIÓN ---

# Usamos una "Clase" para organizar toda la aplicación (Programación Orientada a Objetos)
# Nuestra clase 'App' hereda de 'tk.Tk', que es la ventana principal de Tkinter
class App(tk.Tk):
    # El método __init__ es el "constructor", se llama automáticamente al crear la App
    def __init__(self):
        super().__init__() # Llama al constructor de la clase padre (tk.Tk)
        
        self.title("Clue: Misterio en Innovatech 2025") # Título de la ventana
        self.geometry("800x600") # Tamaño inicial (ancho x alto)
        self.configure(bg=BG_COLOR) # Asigna el color de fondo general
        
        # Llama a la función (definida abajo) que configura todos los estilos
        self.configurar_estilos_globales()

        # Crea un "frame" (marco) contenedor que ocupará toda la ventana
        # Este frame contendrá todas nuestras "pantallas" (Intro, Hub, Detalles, etc.)
        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="both", expand=True) # fill="both" y expand=True hacen que ocupe todo el espacio
        
        # Configura la grilla interna del contenedor para que las pantallas se expandan
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        # Diccionario vacío para guardar todas las "pantallas" (frames)
        self.frames = {}
        
        # Bucle que crea una instancia de CADA pantalla (las clases de pantallas están definidas más abajo)
        for F in (FrameIntro, FrameHub, FrameDetallePersonajes, FrameDetalleArmas, FrameDetalleLocaciones, FrameAcusacion):
            frame = F(container, self) # Crea la pantalla (ej: FrameIntro(container, self))
            self.frames[F] = frame # La guarda en el diccionario (ej: self.frames[FrameIntro] = ...)
            
            # Coloca la pantalla en la grilla (una encima de otra en la misma celda 0,0)
            frame.grid(row=0, column=0, sticky="nsew") # sticky="nsew" (norte, sur, este, oeste) hace que se estire

        # Llama a la función (definida abajo) para mostrar la primera pantalla
        self.mostrar_frame(FrameIntro)

    # Función que aplica los estilos globales a los widgets de ttk
    def configurar_estilos_globales(self):
        style = ttk.Style(self)
        style.theme_use("clam") # 'clam' es un tema que permite personalización avanzada de colores

        # Estilo para Frames (TFrame)
        style.configure("TFrame", background=BG_COLOR)
        
        # Estilo para Etiquetas (TLabel)
        style.configure("TLabel", background=LBL_BG, foreground=FG_COLOR, font=("Consolas", 12))
        style.configure("Titulo.TLabel", font=("Consolas", 18, "bold")) # Estilo especial para títulos
        
        # Estilo para Botones (TButton)
        style.configure("TButton", background=BTN_BG, foreground=FG_COLOR, font=("Consolas", 12, "bold"), borderwidth=0)
        style.map("TButton", background=[('active', SELECT_BG)]) # 'active' = cuando el mouse está encima

        # Estilo para Botón de Acusar (Rojo)
        style.configure("Accent.TButton", background="#ff003c", foreground="white", font=("Consolas", 14, "bold"))
        style.map("Accent.TButton", background=[('active', "#c0002a")]) # Color al pasar el mouse
        
        # Estilo para Menús Desplegables
        style.configure("TMenubutton", background=BTN_BG, foreground=FG_COLOR, font=("Consolas", 11), arrowcolor=FG_COLOR)

    # Esta función es la que maneja el cambio de pantallas
    def mostrar_frame(self, frame_clase):
        """Muestra el frame deseado y oculta los demás."""
        frame = self.frames[frame_clase] # Busca la pantalla en el diccionario
        frame.tkraise() # La "eleva" al frente, poniéndola visible

    # Esta es la lógica central de revisión de la acusación
    def hacer_acusacion(self, guess_culpable, guess_arma, guess_locacion):
        # Compara la selección del usuario (recibida como argumento) con la solución secreta
        if (guess_culpable == solucion_secreta["culpable"] and
            guess_arma == solucion_secreta["arma"] and
            guess_locacion == solucion_secreta["locacion"]):
            
            # Si gana, busca la historia ganadora en el diccionario 'historias_finales'
            historia_ganadora = historias_finales.get(solucion_secreta["culpable"], "¡Caso Resuelto!")
            messagebox.showinfo("¡FELICIDADES!", historia_ganadora) # Muestra ventana de victoria
            self.destroy() # Cierra la ventana y termina el juego
        else:
            # Si falla, muestra ventana de error
            messagebox.showerror("INCORRECTO", "Esa no es la solución. Sigue investigando.")
            # Lo manda de vuelta al Hub para que siga intentando
            self.mostrar_frame(FrameHub) 

# --- 4. DEFINICIÓN DE CADA PANTALLA (FRAMES) ---
# Cada pantalla es una Clase que hereda de 'ttk.Frame'

# --- Pantalla 1: Introducción ---
class FrameIntro(ttk.Frame):
    def __init__(self, parent, controller):
        # 'parent' es el 'container', 'controller' es la 'App' principal
        ttk.Frame.__init__(self, parent, style="TFrame", padding="20")
        
        # Crea la etiqueta del título y le aplica el estilo "Titulo.TLabel"
        titulo = ttk.Label(self, text="MISTERIO EN INNOVATECH 2025", style="Titulo.TLabel")
        titulo.pack(pady=20) # .pack() es una forma de poner widgets (los apila verticalmente)
        
        historia_texto = (
            "¡Asesinato en la convención!\n\n"
            "El brillante Dr. Aris Thorne ha sido encontrado muerto.\n"
            "El asesino, el arma y la locación son un misterio.\n\n"
            "Tu trabajo es revisar las pistas y encontrar al culpable."
        )
        # 'justify="center"' centra el texto si tiene varias líneas
        historia = ttk.Label(self, text=historia_texto, justify="center")
        historia.pack(pady=40)
        
        # Crea el botón para empezar
        boton = ttk.Button(self, text="Iniciar Investigación", 
                           # 'command' define qué función llamar al hacer clic
                           # 'lambda' se usa para poder pasar el 'controller' a la función
                           command=lambda: controller.mostrar_frame(FrameHub))
        # ipady/ipadx es "internal padding", hace el botón más grande
        boton.pack(pady=20, ipady=15, ipadx=10) 

# --- Pantalla 2: Hub (Menú Principal) ---
class FrameHub(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame", padding="20")
        
        titulo = ttk.Label(self, text="Panel de Investigación", style="Titulo.TLabel")
        titulo.pack(pady=20)
        
        # Botón para ir a la pantalla de Personajes
        btn_personajes = ttk.Button(self, text="Revisar Sospechosos",
                                    command=lambda: controller.mostrar_frame(FrameDetallePersonajes))
        btn_personajes.pack(fill="x", pady=10, ipady=10) # fill="x" hace que ocupe todo el ancho
        
        # Botón para ir a la pantalla de Armas
        btn_armas = ttk.Button(self, text="Examinar Armas",
                               command=lambda: controller.mostrar_frame(FrameDetalleArmas))
        btn_armas.pack(fill="x", pady=10, ipady=10)

        # Botón para ir a la pantalla de Locaciones
        btn_locaciones = ttk.Button(self, text="Inspeccionar Locaciones",
                                    command=lambda: controller.mostrar_frame(FrameDetalleLocaciones))
        btn_locaciones.pack(fill="x", pady=10, ipady=10)
        
        # Una línea gris separadora visual
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=30)

        # Botón rojo para ir a la Acusación Final
        btn_acusar = ttk.Button(self, text="HACER ACUSACIÓN FINAL", style="Accent.TButton",
                                command=lambda: controller.mostrar_frame(FrameAcusacion))
        btn_acusar.pack(fill="x", pady=10, ipady=15)


# --- Pantalla 3: Clase Base para Detalles ---
# Esta es una clase "plantilla" para no repetir el mismo código
# en las pantallas de Personajes, Armas y Locaciones.
class FrameDetalleBase(ttk.Frame):
    # Recibe argumentos extra (titulo_frame, lista_items, etc.) para saber qué mostrar
    def __init__(self, parent, controller, titulo_frame, lista_items, mapa_sucesos, volver_a):
        ttk.Frame.__init__(self, parent, style="TFrame", padding="10")
        
        titulo = ttk.Label(self, text=titulo_frame, style="Titulo.TLabel")
        titulo.pack(pady=10)
        
        # Frame contenedor para organizar la lista (izq) y los detalles (der)
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True)
        # Configura la grilla interna de este frame
        content_frame.grid_columnconfigure(2, weight=2) # Columna de texto/imagen más ancha
        content_frame.grid_rowconfigure(0, weight=1) # Fila única que se expande

        # 1. Listbox (la lista de la izquierda)
        # Se usa tk.Listbox (el normal) porque ttk.Listbox no existe.
        # Le aplicamos los colores manualmente.
        listbox = tk.Listbox(content_frame, font=("Consolas", 11), height=15, 
                             bg=TXT_BG, fg=FG_COLOR, selectbackground=SELECT_BG, 
                             selectforeground=FG_COLOR, borderwidth=0, highlightthickness=0)
        for item in lista_items:
            listbox.insert(tk.END, item) # Inserta cada ítem en la lista
        listbox.grid(row=0, column=0, sticky="ns", padx=(0, 10)) # sticky="ns" = estirar verticalmente

        # --- Frame para la imagen y el texto (derecha) ---
        detalle_frame = ttk.Frame(content_frame)
        detalle_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10)
        detalle_frame.grid_rowconfigure(0, weight=1) # Fila 0 para la imagen
        detalle_frame.grid_rowconfigure(1, weight=1) # Fila 1 para el texto
        detalle_frame.grid_columnconfigure(0, weight=1)

        # 2. Etiqueta para la Imagen (estará vacía al inicio)
        self.image_label = ttk.Label(detalle_frame, background=LBL_BG)
        self.image_label.grid(row=0, column=0, sticky="nsew", pady=10)

        # 3. Cuadro de Texto (para el suceso y rol)
        self.texto_suceso = tk.Text(detalle_frame, font=("Consolas", 12), wrap="word", 
                                    height=8, bg=TXT_BG, fg=FG_COLOR, borderwidth=0, highlightthickness=0)
        self.texto_suceso.grid(row=1, column=0, sticky="nsew")
        self.texto_suceso.insert(tk.END, "Selecciona un ítem de la lista para ver su información.")
        
        # Define una "tag" de estilo llamada "bold" para poner texto en negrita
        self.texto_suceso.tag_configure("bold", font=("Consolas", 12, "bold"))
        self.texto_suceso.configure(state="disabled") # Lo hace de solo lectura

        # 4. Evento al seleccionar (función definida dentro de __init__)
        def on_select(event):
            """Se ejecuta cada vez que el usuario hace clic en un ítem de la lista."""
            try:
                # Obtiene el índice (posición) del ítem seleccionado
                idx = listbox.curselection()[0] 
                # Obtiene el nombre (texto) del ítem en esa posición
                item_seleccionado = listbox.get(idx) 
                
                # Busca los datos de ese ítem en el mapa correspondiente
                datos = mapa_sucesos[item_seleccionado] 
                rol = None
                
                # Comprobamos cuántos datos recibimos
                if len(datos) == 3: # Es un personaje (rol, suceso, imagen)
                    rol, suceso, img_filename = datos
                elif len(datos) == 2: # Es arma o locación (suceso, imagen)
                    suceso, img_filename = datos
                
                # --- Actualizar Texto ---
                self.texto_suceso.configure(state="normal") # Permite escribir en el cuadro
                self.texto_suceso.delete("1.0", tk.END) # Borra todo el texto
                
                if rol:
                    # Inserta el ROL y le aplica la tag "bold" que definimos
                    self.texto_suceso.insert(tk.END, f"{rol}\n\n", "bold")
                
                # Inserta el suceso (sin negrita)
                self.texto_suceso.insert(tk.END, suceso) 
                self.texto_suceso.configure(state="disabled") # Vuelve a ser solo lectura
                
                # --- Actualizar Imagen ---
                self.cargar_imagen(img_filename) # Llama a la función de cargar imagen

            except IndexError:
                pass # Ignora clics fuera de la lista
        
        # Asocia el evento "seleccionar" de la lista (<<ListboxSelect>>) con la función on_select
        listbox.bind("<<ListboxSelect>>", on_select)

        # 5. Botón de Volver
        boton_volver = ttk.Button(self, text="Volver al Panel",
                                  # Vuelve al frame que se le pasó como argumento (FrameHub)
                                  command=lambda: controller.mostrar_frame(volver_a))
        boton_volver.pack(pady=10)

    # Función para cargar y mostrar la imagen
    def cargar_imagen(self, filename):
        try:
            ruta_completa = RUTA_IMG / filename # Arma la ruta completa (ej: .../Clue/Ima/p_reed.png)
            
            # Carga la imagen usando Pillow
            img_original = Image.open(ruta_completa)
            # Redimensiona la imagen (máximo 250x250) manteniendo la proporción
            img_original.thumbnail((250, 250)) 
            
            # Convierte la imagen de Pillow a un formato que Tkinter entiende (PhotoImage)
            photo = ImageTk.PhotoImage(img_original)
            
            # Asigna la imagen a la etiqueta (Label)
            self.image_label.configure(image=photo)
            
            # Guarda la referencia global para que Python no la borre (garbage collector)
            image_references[filename] = photo 
            
        except FileNotFoundError:
            # Si no encuentra el archivo, muestra un texto de error
            self.image_label.configure(image=None, text=f"Imagen no encontrada:\n{filename}")
        except Exception as e:
            # Para cualquier otro error de imagen
            self.image_label.configure(image=None, text=f"Error al cargar:\n{filename}")

# --- Clases de Detalles (Heredan de la Base) ---
# Estas clases son muy simples. Solo heredan de FrameDetalleBase
# y le pasan los datos correctos (lista de personajes, mapa de personajes, etc.) al constructor.

class FrameDetallePersonajes(FrameDetalleBase):
    def __init__(self, parent, controller):
        # Llama al constructor de la clase padre (FrameDetalleBase)
        FrameDetalleBase.__init__(self, parent, controller, 
                                  titulo_frame="Sospechosos",
                                  lista_items=lista_personajes,
                                  mapa_sucesos=mapa_personajes,
                                  volver_a=FrameHub)

class FrameDetalleArmas(FrameDetalleBase):
    def __init__(self, parent, controller):
        FrameDetalleBase.__init__(self, parent, controller, 
                                  titulo_frame="Posibles Armas",
                                  lista_items=lista_armas,
                                  mapa_sucesos=mapa_armas,
                                  volver_a=FrameHub)

class FrameDetalleLocaciones(FrameDetalleBase):
    def __init__(self, parent, controller):
        FrameDetalleBase.__init__(self, parent, controller, 
                                  titulo_frame="Locaciones del Crimen",
                                  lista_items=lista_locaciones,
                                  mapa_sucesos=mapa_locaciones,
                                  volver_a=FrameHub)

# --- Pantalla 4: Acusación Final ---
class FrameAcusacion(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame", padding="20")
        
        titulo = ttk.Label(self, text="Acusación Final", style="Titulo.TLabel")
        titulo.pack(pady=20)
        info = ttk.Label(self, text="Elige tu acusación. ¡Si fallas, el culpable escapará!", justify="center")
        info.pack(pady=10)
        
        # Frame para agrupar los menús desplegables
        menus_frame = ttk.Frame(self)
        menus_frame.pack(pady=20)

        # Variables especiales de Tkinter para guardar la selección de los menús
        self.culpable_var = tk.StringVar(value="Elige un sospechoso")
        self.arma_var = tk.StringVar(value="Elige un arma")
        self.locacion_var = tk.StringVar(value="Elige una locación")
        
        # Menú desplegable para Culpable
        # El '*' (asterisco) "desempaca" la lista de personajes
        culpable_menu = ttk.OptionMenu(menus_frame, self.culpable_var, self.culpable_var.get(), *lista_personajes)
        culpable_menu.pack(fill="x", pady=5, ipady=5)

        # Menú desplegable para Arma
        arma_menu = ttk.OptionMenu(menus_frame, self.arma_var, self.arma_var.get(), *lista_armas)
        arma_menu.pack(fill="x", pady=5, ipady=5)

        # Menú desplegable para Locación
        locacion_menu = ttk.OptionMenu(menus_frame, self.locacion_var, self.locacion_var.get(), *lista_locaciones)
        locacion_menu.pack(fill="x", pady=5, ipady=5)
        
        # Botón de Acusar (Rojo)
        boton_acusar = ttk.Button(self, text="¡CONFIRMAR ACUSACIÓN!", style="Accent.TButton",
                                  # Llama a la función de validación de esta misma clase
                                  command=lambda: self.validar_y_acusar(controller))
        boton_acusar.pack(pady=20, fill="x", ipady=15)
        
        # Botón para volver al Hub si el usuario se arrepiente
        boton_volver = ttk.Button(self, text="Volver al Panel",
                                  command=lambda: controller.mostrar_frame(FrameHub))
        boton_volver.pack(pady=5)

    def validar_y_acusar(self, controller):
        """Revisa que todo esté seleccionado antes de acusar."""
        culpable = self.culpable_var.get()
        arma = self.arma_var.get()
        locacion = self.locacion_var.get()
        
        # Revisa si el usuario dejó alguna opción con el valor por defecto
        if culpable == "Elige un sospechoso" or arma == "Elige un arma" or locacion == "Elige una locación":
            messagebox.showwarning("Acusación Incompleta", "Debes elegir un sospechoso, un arma y una locación.")
        else:
            # Si todo está seleccionado, llama a la función principal 'hacer_acusacion' en la App
            controller.hacer_acusacion(culpable, arma, locacion)

# --- 5. EJECUTAR EL JUEGO ---

# Esta es la parte que realmente inicia todo
# 'if __name__ == "__main__":' es una comprobación estándar de Python.
# Asegura que este código solo se ejecute cuando se corre este archivo directamente
# (y no si es importado por otro script).
if __name__ == "__main__":
    app = App() # 1. Crea una instancia de nuestra clase principal App
    app.mainloop() # 2. Inicia el bucle principal de Tkinter (se queda esperando clics, teclas, etc.)