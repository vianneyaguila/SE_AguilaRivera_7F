import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import json
from pathlib import Path
from PIL import Image, ImageTk  # <-- Librería para imágenes

# --- 1. CONFIGURACIÓN DE ESTILO (Colores como los del video) ---
BG_COLOR = "#2c2c2c"  # Fondo oscuro
FG_COLOR = "#00ff41"  # Texto verde neón
BTN_BG = "#4f4f4f"  # Fondo de botón
LBL_BG = "#2c2c2c"  # Fondo de etiquetas
TXT_BG = "#1e1e1e"  # Fondo de cajas de texto
SELECT_BG = "#4a4a4a" # Color al seleccionar en lista

# --- 2. LÓGICA DE CARGA DE DATOS ---
RUTA_BASE = Path(__file__).parent
RUTA_JSON = RUTA_BASE / "misterios_con_imagenes.json"
RUTA_IMG = RUTA_BASE / "img"  # <-- Nueva ruta a la carpeta de imágenes

# Diccionario global para guardar las historias (no estaban en el JSON)
historias_finales = {
    "Dra. Evelyn Reed": "¡Correcto! La Dra. Reed usó la discusión como distracción. Más tarde, en el Salón VIP, aprovechó la cámara rota para envenenar el café de Thorne, sabiendo que era su única oportunidad de salvar su compañía.",
    "Profesor Kenji Tanaka": "¡Has descubierto la verdad! El Profesor confrontó a Thorne en el escenario. Cuando Thorne se burló de él, Tanaka, ciego de ira, usó la estatuilla limpia de huellas para golpearlo. Las luces fallando cubrieron su huida.",
    "Glitch": "¡Impresionante! 'Glitch' se infiltró en el Demo Lab para plantar la USB. Thorne lo sorprendió. Durante el forcejeo, 'Glitch' conectó la USB al terminal personal de Thorne, sobrecargando su marcapasos.",
    "Bryce Wagner": "¡Exacto! Wagner citó a Thorne en el Muelle de Carga con una excusa. Sus 'llamadas urgentes' eran para hackear el dron. Lo soltó sobre Thorne, haciéndolo parecer un accidente trágico para cobrar el seguro.",
    "Chloe Jenkins": "¡Increíble, era ella! Chloe, sabiendo que Thorne la despediría, lo confrontó en la Sala de Servidores. Usó el cable de red robado para estrangularlo, confiando en que el ruido de los servidores ocultaría todo."
}

def cargar_datos(archivo_json):
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos_completos = json.load(f)
            return datos_completos["expediente"], datos_completos["escenarios"]
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al cargar JSON: {e}")
        return None, None

expediente, lista_escenarios = cargar_datos(RUTA_JSON)

if not expediente or not lista_escenarios:
    exit()

# Preparar listas y mapas de datos
lista_personajes = [p["nombre"] for p in expediente["personajes"]]
lista_armas = [a["nombre"] for a in expediente["armas"]]
lista_locaciones = [l["nombre"] for l in expediente["locaciones"]]

# Ahora guardamos (rol, suceso, imagen) para los personajes
mapa_personajes = {p["nombre"]: (p["rol"], p["suceso"], p["imagen"]) for p in expediente["personajes"]}
# Los otros mapas (suceso, imagen)
mapa_armas = {a["nombre"]: (a["suceso"], a["imagen"]) for a in expediente["armas"]}

# !!!!! AQUÍ ESTABA EL ERROR (Corregido de 'a' a 'l') !!!!!
mapa_locaciones = {l["nombre"]: (l["suceso"], l["imagen"]) for l in expediente["locaciones"]}

solucion_secreta = random.choice(lista_escenarios)

# Guardar referencias de imágenes
image_references = {} 

# --- 3. CLASE PRINCIPAL DE LA APLICACIÓN ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Clue: Misterio en Innovatech 2025")
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)
        
        self.configurar_estilos_globales()

        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (FrameIntro, FrameHub, FrameDetallePersonajes, FrameDetalleArmas, FrameDetalleLocaciones, FrameAcusacion):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(FrameIntro)

    def configurar_estilos_globales(self):
        style = ttk.Style(self)
        style.theme_use("clam") # 'clam' es un tema que permite más personalización

        # Estilo para Frames
        style.configure("TFrame", background=BG_COLOR)
        
        # Estilo para Etiquetas
        style.configure("TLabel", background=LBL_BG, foreground=FG_COLOR, font=("Consolas", 12))
        style.configure("Titulo.TLabel", font=("Consolas", 18, "bold"))
        
        # Estilo para Botones
        style.configure("TButton", background=BTN_BG, foreground=FG_COLOR, font=("Consolas", 12, "bold"), borderwidth=0)
        style.map("TButton", background=[('active', SELECT_BG)]) # Al pasar el mouse

        # Estilo para Botón de Acusar (Rojo)
        style.configure("Accent.TButton", background="#ff003c", foreground="white", font=("Consolas", 14, "bold"))
        style.map("Accent.TButton", background=[('active', "#c0002a")])
        
        # Estilo para Menús Desplegables
        style.configure("TMenubutton", background=BTN_BG, foreground=FG_COLOR, font=("Consolas", 11), arrowcolor=FG_COLOR)

    def mostrar_frame(self, frame_clase):
        frame = self.frames[frame_clase]
        frame.tkraise()

    def hacer_acusacion(self, guess_culpable, guess_arma, guess_locacion):
        if (guess_culpable == solucion_secreta["culpable"] and
            guess_arma == solucion_secreta["arma"] and
            guess_locacion == solucion_secreta["locacion"]):
            
            historia_ganadora = historias_finales.get(solucion_secreta["culpable"], "¡Caso Resuelto!")
            messagebox.showinfo("¡FELICIDADES!", historia_ganadora)
            self.destroy()
        else:
            messagebox.showerror("INCORRECTO", "Esa no es la solución. Sigue investigando.")
            self.mostrar_frame(FrameHub)

# --- 4. DEFINICIÓN DE CADA PANTALLA (FRAMES) ---

class FrameIntro(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame", padding="20")
        
        titulo = ttk.Label(self, text="MISTERIO EN INNOVATECH 2025", style="Titulo.TLabel")
        titulo.pack(pady=20)
        
        historia_texto = (
            "¡Asesinato en la convención!\n\n"
            "El brillante Dr. Aris Thorne ha sido encontrado muerto.\n"
            "El asesino, el arma y la locación son un misterio.\n\n"
            "Tu trabajo es revisar las pistas y encontrar al culpable."
        )
        historia = ttk.Label(self, text=historia_texto, justify="center")
        historia.pack(pady=40)
        
        boton = ttk.Button(self, text="Iniciar Investigación", 
                           command=lambda: controller.mostrar_frame(FrameHub))
        boton.pack(pady=20, ipady=15, ipadx=10)

class FrameHub(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame", padding="20")
        
        titulo = ttk.Label(self, text="Panel de Investigación", style="Titulo.TLabel")
        titulo.pack(pady=20)
        
        btn_personajes = ttk.Button(self, text="Revisar Sospechosos",
                                    command=lambda: controller.mostrar_frame(FrameDetallePersonajes))
        btn_personajes.pack(fill="x", pady=10, ipady=10)
        
        btn_armas = ttk.Button(self, text="Examinar Armas",
                               command=lambda: controller.mostrar_frame(FrameDetalleArmas))
        btn_armas.pack(fill="x", pady=10, ipady=10)

        btn_locaciones = ttk.Button(self, text="Inspeccionar Locaciones",
                                    command=lambda: controller.mostrar_frame(FrameDetalleLocaciones))
        btn_locaciones.pack(fill="x", pady=10, ipady=10)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=30)

        btn_acusar = ttk.Button(self, text="HACER ACUSACIÓN FINAL", style="Accent.TButton",
                                command=lambda: controller.mostrar_frame(FrameAcusacion))
        btn_acusar.pack(fill="x", pady=10, ipady=15)


# --- Frame Genérico para mostrar detalles (Listbox + Texto + IMAGEN) ---

class FrameDetalleBase(ttk.Frame):
    def __init__(self, parent, controller, titulo_frame, lista_items, mapa_sucesos, volver_a):
        ttk.Frame.__init__(self, parent, style="TFrame", padding="10")
        
        titulo = ttk.Label(self, text=titulo_frame, style="Titulo.TLabel")
        titulo.pack(pady=10)
        
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True)
        content_frame.grid_columnconfigure(1, weight=1) 
        content_frame.grid_columnconfigure(2, weight=2) 
        content_frame.grid_rowconfigure(0, weight=1)

        # 1. Listbox (izquierda)
        listbox = tk.Listbox(content_frame, font=("Consolas", 11), height=15, 
                             bg=TXT_BG, fg=FG_COLOR, selectbackground=SELECT_BG, 
                             selectforeground=FG_COLOR, borderwidth=0, highlightthickness=0)
        for item in lista_items:
            listbox.insert(tk.END, item)
        listbox.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        # --- Frame para la imagen y el texto (derecha) ---
        detalle_frame = ttk.Frame(content_frame)
        detalle_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10)
        detalle_frame.grid_rowconfigure(0, weight=1) # Imagen
        detalle_frame.grid_rowconfigure(1, weight=1) # Texto
        detalle_frame.grid_columnconfigure(0, weight=1)

        # 2. Etiqueta para la Imagen
        self.image_label = ttk.Label(detalle_frame, background=LBL_BG)
        self.image_label.grid(row=0, column=0, sticky="nsew", pady=10)

        # 3. Cuadro de Texto
        self.texto_suceso = tk.Text(detalle_frame, font=("Consolas", 12), wrap="word", 
                                    height=8, bg=TXT_BG, fg=FG_COLOR, borderwidth=0, highlightthickness=0)
        self.texto_suceso.grid(row=1, column=0, sticky="nsew")
        self.texto_suceso.insert(tk.END, "Selecciona un ítem de la lista para ver su información.")
        
        # Añadimos una "tag" de estilo para el rol
        self.texto_suceso.tag_configure("bold", font=("Consolas", 12, "bold"))
        self.texto_suceso.configure(state="disabled")

        # 4. Evento al seleccionar (lógica actualizada)
        def on_select(event):
            try:
                idx = listbox.curselection()[0]
                item_seleccionado = listbox.get(idx)
                
                datos = mapa_sucesos[item_seleccionado]
                rol = None
                
                # Comprobamos cuántos datos recibimos
                if len(datos) == 3: # Es un personaje (rol, suceso, imagen)
                    rol, suceso, img_filename = datos
                elif len(datos) == 2: # Es arma o locación (suceso, imagen)
                    suceso, img_filename = datos
                
                # Actualizar Texto
                self.texto_suceso.configure(state="normal")
                self.texto_suceso.delete("1.0", tk.END)
                
                if rol:
                    # Insertamos el ROL con la tag "bold"
                    self.texto_suceso.insert(tk.END, f"{rol}\n\n", "bold")
                
                # Insertamos el suceso normal
                self.texto_suceso.insert(tk.END, suceso)
                self.texto_suceso.configure(state="disabled")
                
                # Actualizar Imagen
                self.cargar_imagen(img_filename)

            except IndexError:
                pass
        
        listbox.bind("<<ListboxSelect>>", on_select)

        # 5. Botón de Volver
        boton_volver = ttk.Button(self, text="Volver al Panel",
                                  command=lambda: controller.mostrar_frame(volver_a))
        boton_volver.pack(pady=10)

    def cargar_imagen(self, filename):
        try:
            ruta_completa = RUTA_IMG / filename
            
            # Cargar y redimensionar imagen
            img_original = Image.open(ruta_completa)
            img_original.thumbnail((250, 250)) # Redimensiona sin deformar
            
            photo = ImageTk.PhotoImage(img_original)
            
            # Mostrar la imagen
            self.image_label.configure(image=photo)
            
            # Guardar referencia
            image_references[filename] = photo 
            
        except FileNotFoundError:
            self.image_label.configure(image=None, text=f"Imagen no encontrada:\n{filename}")
        except Exception as e:
            self.image_label.configure(image=None, text=f"Error al cargar:\n{filename}")

# --- Clases específicas que heredan de FrameDetalleBase ---

class FrameDetallePersonajes(FrameDetalleBase):
    def __init__(self, parent, controller):
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

class FrameAcusacion(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame", padding="20")
        
        titulo = ttk.Label(self, text="Acusación Final", style="Titulo.TLabel")
        titulo.pack(pady=20)
        
        info = ttk.Label(self, text="Elige tu acusación. ¡Si fallas, el culpable escapará!", justify="center")
        info.pack(pady=10)
        
        menus_frame = ttk.Frame(self)
        menus_frame.pack(pady=20)

        self.culpable_var = tk.StringVar(value="Elige un sospechoso")
        self.arma_var = tk.StringVar(value="Elige un arma")
        self.locacion_var = tk.StringVar(value="Elige una locación")
        
        culpable_menu = ttk.OptionMenu(menus_frame, self.culpable_var, self.culpable_var.get(), *lista_personajes)
        culpable_menu.pack(fill="x", pady=5, ipady=5)

        arma_menu = ttk.OptionMenu(menus_frame, self.arma_var, self.arma_var.get(), *lista_armas)
        arma_menu.pack(fill="x", pady=5, ipady=5)

        locacion_menu = ttk.OptionMenu(menus_frame, self.locacion_var, self.locacion_var.get(), *lista_locaciones)
        locacion_menu.pack(fill="x", pady=5, ipady=5)
        
        boton_acusar = ttk.Button(self, text="¡CONFIRMAR ACUSACIÓN!", style="Accent.TButton",
                                  command=lambda: self.validar_y_acusar(controller))
        boton_acusar.pack(pady=20, fill="x", ipady=15)
        
        boton_volver = ttk.Button(self, text="Volver al Panel",
                                  command=lambda: controller.mostrar_frame(FrameHub))
        boton_volver.pack(pady=5)

    def validar_y_acusar(self, controller):
        culpable = self.culpable_var.get()
        arma = self.arma_var.get()
        locacion = self.locacion_var.get()
        
        if culpable == "Elige un sospechoso" or arma == "Elige un arma" or locacion == "Elige una locación":
            messagebox.showwarning("Acusación Incompleta", "Debes elegir un sospechoso, un arma y una locación.")
        else:
            controller.hacer_acusacion(culpable, arma, locacion)

# --- 5. EJECUTAR EL JUEGO ---
if __name__ == "__main__":
    app = App()
    app.mainloop()