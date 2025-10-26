import tkinter as tk
from tkinter import messagebox, simpledialog, font
import random
import json
import sys
import os  # <-- Importación para manejar rutas de archivos

try:
    # Importamos la librería de imágenes (Pillow)
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Error de Librería", 
                         "No se encontró la librería 'Pillow'.\nPor favor, instálala desde tu terminal con: pip install Pillow")
    sys.exit()

# --- Sección 1: Manejo de Archivos ---

# Encuentra la carpeta donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Crea la ruta completa al archivo JSON
DB_FILE = os.path.join(script_dir, 'basedatos_bridgerton.json')
# Crea la ruta completa a la imagen
IMG_FILE = os.path.join(script_dir, 'imagenes', 'bridgerton.jpeg') # <-- Nombre de tu imagen

def cargar_datos():
    """Carga los personajes y preguntas desde el archivo JSON."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos['personajes'], datos['preguntas']
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo '{DB_FILE}'.\nAsegúrate de que está en la misma carpeta que el script.")
        sys.exit()
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"El archivo '{DB_FILE}' tiene un formato JSON inválido.")
        sys.exit()

def guardar_datos(personajes, preguntas):
    """Guarda los datos actualizados (aprendizaje) de vuelta en el archivo JSON."""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            datos_completos = {'preguntas': preguntas, 'personajes': personajes}
            json.dump(datos_completos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        messagebox.showerror("Error", f"Error al guardar los datos: {e}")

# --- Sección 2: Clase de la Aplicación (GUI) ---

class AdivinaQuienGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina Quién: Bridgerton")
        self.root.geometry("600x600") # Tamaño de la ventana
        self.root.configure(bg="#f0f0f0")

        # --- Definimos las fuentes ---
        self.font_titulo = font.Font(family="Helvetica", size=24, weight="bold")
        self.font_texto = font.Font(family="Helvetica", size=16)
        self.font_pregunta = font.Font(family="Helvetica", size=14)
        self.font_boton = font.Font(family="Helvetica", size=12)

        # --- Creamos los dos "frames" o "pantallas" ---
        self.welcome_frame = tk.Frame(self.root, bg="#E0EBF5")
        self.game_frame = tk.Frame(self.root, bg="#f0f0f0")
        
        # Construimos el contenido de cada pantalla
        self.create_welcome_widgets()
        self.create_game_widgets()

        # Mostramos la pantalla de bienvenida al inicio
        self.welcome_frame.pack(fill="both", expand=True)

    def create_welcome_widgets(self):
        """Crea la pantalla de bienvenida con la imagen y leyenda."""
        
        # --- Cargar y mostrar la imagen ---
        try:
            img = Image.open(IMG_FILE)
            img = img.resize((500, 280), Image.LANCZOS) # Redimensiona la imagen
            self.photo_img = ImageTk.PhotoImage(img)

            img_label = tk.Label(self.welcome_frame, image=self.photo_img, bg="#E0EBF5")
            img_label.image = self.photo_img 
            img_label.pack(pady=(20, 10))

        except FileNotFoundError:
            tk.Label(self.welcome_frame, text=f"No se encontró la imagen '{os.path.basename(IMG_FILE)}' en la carpeta 'imagenes'", 
                     font=("Helvetica", 10, "italic"), fg="red", bg="#E0EBF5").pack(pady=20)
        except Exception as e:
            tk.Label(self.welcome_frame, text=f"Error al cargar la imagen: {e}", 
                     font=("Helvetica", 10, "italic"), fg="red", bg="#E0EBF5").pack(pady=20)

        # --- LEYENDA DE BIENVENIDA ---
        tk.Label(self.welcome_frame, text="¡Bienvenido al Juego de Adivina Quién!", 
                 font=self.font_titulo, bg="#E0EBF5", fg="#4a69bd").pack(pady=(10, 5))
        
        tk.Label(self.welcome_frame, text="Piensa en un personaje del universo Bridgerton\ny yo intentaré adivinarlo con tus respuestas.", 
                 font=self.font_texto, bg="#E0EBF5", wraplength=450, justify=tk.CENTER).pack(pady=(0, 20))

        start_button = tk.Button(self.welcome_frame, text="Comenzar a Jugar", 
                                 font=self.font_boton, command=self.show_game_frame, 
                                 bg="#4a69bd", fg="white", relief=tk.FLAT, padx=20, pady=10)
        start_button.pack(pady=10)

    def create_game_widgets(self):
        """Crea la pantalla de juego (inicialmente oculta)."""
        
        self.pregunta_label = tk.Label(self.game_frame, text="...", 
                                     font=self.font_pregunta, wraplength=450, bg="#f0f0f0")
        self.pregunta_label.pack(pady=(50, 30))

        botones_frame = tk.Frame(self.game_frame, bg="#f0f0f0")
        botones_frame.pack()

        self.si_button = tk.Button(botones_frame, text="Sí", font=self.font_boton, 
                                   width=10, command=self.responder_si, bg="#2ecc71", fg="white", relief=tk.FLAT)
        self.si_button.pack(side=tk.LEFT, padx=15, pady=20)

        self.no_button = tk.Button(botones_frame, text="No", font=self.font_boton, 
                                  width=10, command=self.responder_no, bg="#e74c3c", fg="white", relief=tk.FLAT)
        self.no_button.pack(side=tk.LEFT, padx=15, pady=20)
        
        self.reiniciar_button = tk.Button(self.game_frame, text="Volver al Inicio", 
                                        font=("Helvetica", 10), command=self.show_welcome_frame)
        self.reiniciar_button.pack(side=tk.BOTTOM, pady=20)

    def show_game_frame(self):
        """Oculta la bienvenida y muestra el juego."""
        self.welcome_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        
        self.personajes, self.preguntas = cargar_datos()
        self.iniciar_juego()

    def show_welcome_frame(self):
        """Oculta el juego y muestra la bienvenida."""
        self.game_frame.pack_forget()
        self.welcome_frame.pack(fill="both", expand=True)

    # --- LÓGICA DEL JUEGO ---

    def iniciar_juego(self):
        """Reinicia todas las variables para una nueva partida."""
        self.posibles = self.personajes.copy()
        self.preguntas_hechas = []
        self.respuestas_dadas = {}
        self.atributo_actual = None
        self.numero_de_preguntas = 0 # <-- Se reinicia el contador de preguntas
        
        self.si_button.config(state=tk.NORMAL)
        self.no_button.config(state=tk.NORMAL)
        
        self.siguiente_pregunta()

    def responder_si(self):
        self.procesar_respuesta('si')

    def responder_no(self):
        self.procesar_respuesta('no')

    def procesar_respuesta(self, respuesta):
        """Filtra la lista de personajes basada en la respuesta."""
        if self.atributo_actual:
            self.respuestas_dadas[self.atributo_actual] = respuesta
            
            posibles_actualizados = []
            for personaje in self.posibles:
                if personaje.get(self.atributo_actual) == respuesta:
                    posibles_actualizados.append(personaje)
            self.posibles = posibles_actualizados

        # --- Lógica de 5 Preguntas ---
        if not self.posibles:
            # CASO 1: No quedan sospechosos
            messagebox.showwarning("¡Oh no!", "No conozco a ningún personaje que coincida con tus respuestas.")
            self.iniciar_juego()
        elif len(self.posibles) == 1:
            # CASO 2: Solo queda 1 (¡Adivinamos aunque sea antes de 5 preguntas!)
            self.adivinanza_final(self.posibles[0])
        elif self.numero_de_preguntas == 5:
            # CASO 3: Llegamos a 5 preguntas y aún hay varios sospechosos
            messagebox.showinfo("¡Momento de la verdad!", "He hecho 5 preguntas. ¡Voy a adivinar!")
            self.adivinanza_final(random.choice(self.posibles))
        else:
            # CASO 4: Menos de 5 preguntas y más de 1 sospechoso -> Siguiente pregunta
            self.siguiente_pregunta()

    def siguiente_pregunta(self):
        """Busca y muestra la siguiente pregunta aleatoria."""
        atributos_disponibles = [attr for attr in self.preguntas.keys() if attr not in self.preguntas_hechas]
        
        if not atributos_disponibles:
            # Si no hay más preguntas, adivina al azar entre los restantes
            self.adivinanza_final(random.choice(self.posibles))
        else:
            self.numero_de_preguntas += 1 # <-- Aumenta el contador de preguntas
            self.atributo_actual = random.choice(atributos_disponibles)
            self.preguntas_hechas.append(self.atributo_actual)
            self.pregunta_label.config(text=self.preguntas[self.atributo_actual])

    def adivinanza_final(self, personaje_adivinado):
        """Pregunta al usuario si el personaje adivinado es correcto."""
        self.si_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)
        
        respuesta = messagebox.askyesno("Adivinanza Final", f"¿Tu personaje es {personaje_adivinado['nombre']}?")
        
        if respuesta:
            messagebox.showinfo("¡Gané!", "¡Excelente! He adivinado una vez más.")
            self.iniciar_juego()
        else:
            self.iniciar_aprendizaje(personaje_adivinado)

    def iniciar_aprendizaje(self, personaje_adivinado):
        """Inicia el proceso de aprendizaje de un nuevo personaje."""
        nombre_correcto = simpledialog.askstring("Aprender", "¡Me has vencido! ¿Cuál era el nombre de tu personaje?")
        if not nombre_correcto:
            self.iniciar_juego()
            return

        nueva_pregunta = simpledialog.askstring("Aprender", f"Escribe una pregunta (si/no) que diferencie a {personaje_adivinado['nombre']} de {nombre_correcto}:")
        if not nueva_pregunta:
            self.iniciar_juego()
            return

        respuesta_para_nuevo = simpledialog.askstring("Aprender", f"Y para {nombre_correcto}, ¿la respuesta a esa pregunta sería 'si' o 'no'?")
        if not respuesta_para_nuevo or respuesta_para_nuevo.lower() not in ['si', 'no']:
            messagebox.showerror("Error", "Respuesta inválida. El aprendizaje ha fallado.")
            self.iniciar_juego()
            return
        
        respuesta_para_nuevo = respuesta_para_nuevo.lower()

        # Actualiza la base de conocimientos
        nuevo_atributo = nueva_pregunta.lower().replace(" ", "_").replace("¿", "").replace("?","")
        
        self.preguntas[nuevo_atributo] = nueva_pregunta
        
        nuevo_personaje = self.respuestas_dadas.copy()
        nuevo_personaje['nombre'] = nombre_correcto
        nuevo_personaje[nuevo_atributo] = respuesta_para_nuevo
        
        for p in self.personajes:
            if p['nombre'] == personaje_adivinado['nombre']:
                p[nuevo_atributo] = 'no' if respuesta_para_nuevo == 'si' else 'si'
            elif nuevo_atributo not in p:
                p[nuevo_atributo] = 'no' 
        
        self.personajes.append(nuevo_personaje)
        
        # Guarda los cambios en el archivo JSON
        guardar_datos(self.personajes, self.preguntas)
        
        messagebox.showinfo("¡Gracias!", "¡He actualizado mi base de conocimientos! El juego se reiniciará.")
        self.iniciar_juego()

# --- Sección 3: Ejecución Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AdivinaQuienGUI(root)
    root.mainloop()