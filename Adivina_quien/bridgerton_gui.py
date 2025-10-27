# --- Sección 0: Importaciones de Librerías ---

# Importa la biblioteca principal de interfaces gráficas (GUI) de Python.
# 'as tk' nos permite acortar su nombre a 'tk'.
import tkinter as tk

# De 'tkinter', importamos módulos específicos:
# - 'messagebox': Para mostrar ventanas emergentes de información, error o advertencia.
# - 'simpledialog': Para pedir al usuario que escriba texto (como el nombre del personaje).
# - 'font': Para poder definir fuentes personalizadas (tamaño, negrita, etc.).
from tkinter import messagebox, simpledialog, font

# Importa la biblioteca para generar números (y elecciones) aleatorias.
# La usamos para elegir qué pregunta hacer.
import random

# Importa la biblioteca para trabajar con archivos en formato JSON (nuestra base de datos).
import json

# Importa 'sys' (System), que nos permite interactuar con el sistema,
# principalmente para cerrar el programa limpiamente (sys.exit) si ocurre un error grave.
import sys

# Importa 'os' (Operating System), que nos permite interactuar con el sistema operativo.
# Lo usamos para construir rutas de archivos (os.path.join) y encontrar
# la carpeta actual (os.path.dirname), asegurando que funcione en Windows, Mac o Linux.
import os

try:
    # Intentamos importar las bibliotecas 'Image' e 'ImageTk' de 'PIL' (Pillow).
    # 'Image' nos deja abrir y manipular archivos .jpg y .png.
    # 'ImageTk' convierte esas imágenes a un formato que Tkinter puede mostrar.
    from PIL import Image, ImageTk
except ImportError:
    # Si 'Pillow' no está instalada, el 'try' falla y este 'except' se ejecuta.
    # Muestra un error y cierra el programa, dándole instrucciones al usuario.
    messagebox.showerror("Error de Librería", 
                         "No se encontró la librería 'Pillow'.\nPor favor, instálala desde tu terminal con: pip install Pillow")
    sys.exit()

# --- Sección 1: Manejo de Archivos y Rutas Globales ---

# '__file__' es una variable especial de Python que contiene la ruta del script actual.
# 'os.path.abspath(__file__)' obtiene la ruta completa (absoluta) de este archivo.
# 'os.path.dirname(...)' extrae únicamente la ruta de la CARPETA que contiene el archivo.
# Así, 'script_dir' siempre apunta a la carpeta de nuestro proyecto.
script_dir = os.path.dirname(os.path.abspath(__file__))

# 'os.path.join()' une rutas de forma inteligente (con / o \ según el SO).
# Creamos la ruta completa y correcta a nuestro archivo de base de datos.
DB_FILE = os.path.join(script_dir, 'basedatos_bridgerton.json')

# Creamos la ruta completa a nuestra imagen de bienvenida, que está en la carpeta 'imagenes'.
IMG_FILE = os.path.join(script_dir, 'imagenes', 'bridgerton.jpeg') # Asegúrate que este sea el nombre de tu imagen

def cargar_datos():
    """
    Función para leer el archivo JSON y cargarlo en la memoria de Python.
    No recibe parámetros, pero devuelve dos variables:
    la lista de personajes y el diccionario de preguntas.
    """
    try:
        # 'with open(...)' es la forma segura de abrir y cerrar archivos.
        # 'r' = modo lectura (read).
        # 'encoding="utf-8"' asegura que podamos leer acentos y caracteres especiales.
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            # 'json.load(f)' lee el archivo 'f' y convierte el texto JSON
            # en un diccionario de Python.
            datos = json.load(f)
            # Devolvemos las dos claves principales de nuestro JSON.
            return datos['personajes'], datos['preguntas']
    except FileNotFoundError:
        # Si el 'try' falla porque el archivo no existe, se ejecuta esto.
        messagebox.showerror("Error", f"No se encontró el archivo '{DB_FILE}'.\nAsegúrate de que está en la misma carpeta que el script.")
        sys.exit() # Cierra el programa.
    except json.JSONDecodeError:
        # Si el archivo JSON está mal escrito (ej. falta una coma), se ejecuta esto.
        messagebox.showerror("Error", f"El archivo '{DB_FILE}' tiene un formato JSON inválido.")
        sys.exit() # Cierra el programa.

def guardar_datos(personajes, preguntas):
    """
    Función para guardar el conocimiento "aprendido" de vuelta en el archivo JSON.
    Recibe la lista de personajes (actualizada) y el diccionario de preguntas (actualizado).
    """
    try:
        # 'w' = modo escritura (write). ¡Esto SOBREESCRIBE el archivo!
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            # Preparamos la estructura completa del diccionario que queremos guardar.
            datos_completos = {'preguntas': preguntas, 'personajes': personajes}
            # 'json.dump()' escribe la variable de Python en el archivo 'f' en formato JSON.
            # 'indent=4' hace que el JSON se guarde de forma "bonita" y legible.
            # 'ensure_ascii=False' permite que se guarden acentos (como en "Quién").
            json.dump(datos_completos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        # Si hay un error de permisos (ej. el archivo está "solo lectura"), lo notifica.
        messagebox.showerror("Error", f"Error al guardar los datos: {e}")

# --- Sección 2: Clase Principal de la Aplicación (GUI) ---

# Usamos una "Clase" para organizar toda la lógica y variables de nuestra
# interfaz gráfica en un solo lugar.
class AdivinaQuienGUI:
    def __init__(self, root):
        """
        El "constructor" de la clase. Es lo primero que se ejecuta cuando
        creamos la aplicación. 'root' es la ventana principal.
        """
        # Guardamos una referencia a la ventana principal para usarla en otras funciones.
        self.root = root
        self.root.title("Adivina Quién: Bridgerton") # Título de la ventana.
        self.root.geometry("600x600") # Tamaño inicial (ancho x alto)
        self.root.configure(bg="#f0f0f0") # Color de fondo gris claro.

        # --- Definimos las fuentes que usaremos en la app ---
        self.font_titulo = font.Font(family="Helvetica", size=24, weight="bold")
        self.font_texto = font.Font(family="Helvetica", size=16)
        self.font_pregunta = font.Font(family="Helvetica", size=14)
        self.font_boton = font.Font(family="Helvetica", size=12)

        # --- Creamos los dos "frames" o "pantallas" ---
        # Un 'Frame' es un contenedor invisible. Usamos dos para simular dos pantallas.
        self.welcome_frame = tk.Frame(self.root, bg="#E0EBF5") # Pantalla de bienvenida
        self.game_frame = tk.Frame(self.root, bg="#f0f0f0")    # Pantalla de juego
        
        # Llamamos a las funciones que "llenarán" estos frames con botones y texto.
        self.create_welcome_widgets()
        self.create_game_widgets()

        # Mostramos la pantalla de bienvenida al inicio.
        # .pack() es el método que "dibuja" el widget en la ventana.
        # 'fill="both"' y 'expand=True' hacen que ocupe todo el espacio disponible.
        self.welcome_frame.pack(fill="both", expand=True)

    # --- Sección 2a: Creación de Widgets (Elementos Gráficos) ---

    def create_welcome_widgets(self):
        """Crea todos los widgets para la pantalla de bienvenida."""
        
        try:
            # 1. Abre la imagen de bienvenida con Pillow
            img = Image.open(IMG_FILE)
            # 2. Redimensiona la imagen. 'Image.LANCZOS' es un filtro de alta calidad.
            img = img.resize((500, 280), Image.LANCZOS)
            # 3. Convierte la imagen de Pillow a un formato que Tkinter entiende.
            self.photo_img = ImageTk.PhotoImage(img)

            # 4. Crea una Etiqueta (Label) para mostrar la imagen.
            img_label = tk.Label(self.welcome_frame, image=self.photo_img, bg="#E0EBF5")
            # 5. Guarda una referencia a la imagen (¡MUY IMPORTANTE!)
            #    Si no, Python la borra (recolector de basura) y la imagen no se ve.
            img_label.image = self.photo_img 
            # 6. Dibuja la imagen en la pantalla de bienvenida.
            #    'pady=(20, 10)' significa 20px de espacio arriba, 10px abajo.
            img_label.pack(pady=(20, 10))

        except FileNotFoundError:
            # Si no se encuentra la imagen, muestra un texto de error.
            tk.Label(self.welcome_frame, text=f"No se encontró la imagen '{os.path.basename(IMG_FILE)}' en la carpeta 'imagenes'", 
                     font=("Helvetica", 10, "italic"), fg="red", bg="#E0EBF5").pack(pady=20)
        except Exception as e:
            # Captura cualquier otro error (ej. archivo corrupto).
            tk.Label(self.welcome_frame, text=f"Error al cargar la imagen: {e}", 
                     font=("Helvetica", 10, "italic"), fg="red", bg="#E0EBF5").pack(pady=20)

        # --- LEYENDA DE BIENVENIDA ---
        # Crea la etiqueta del título
        tk.Label(self.welcome_frame, text="¡Bienvenido al Juego de Adivina Quién!", 
                 font=self.font_titulo, bg="#E0EBF5", fg="#4a69bd").pack(pady=(10, 5))
        
        # Crea la etiqueta de descripción
        tk.Label(self.welcome_frame, text="Piensa en un personaje del universo Bridgerton\ny yo intentaré adivinarlo con tus respuestas.", 
                 font=self.font_texto, bg="#E0EBF5", wraplength=450, justify=tk.CENTER).pack(pady=(0, 20))

        # Crea el botón de "Comenzar"
        # 'command=self.show_game_frame' le dice al botón qué función ejecutar al hacerle clic.
        start_button = tk.Button(self.welcome_frame, text="Comenzar a Jugar", 
                                 font=self.font_boton, command=self.show_game_frame, 
                                 bg="#4a69bd", fg="white", relief=tk.FLAT, padx=20, pady=10)
        start_button.pack(pady=10)

    def create_game_widgets(self):
        """Crea todos los widgets para la pantalla de juego (que está oculta)."""
        
        # Etiqueta que mostrará la pregunta. El texto '...' se actualizará después.
        self.pregunta_label = tk.Label(self.game_frame, text="...", 
                                     font=self.font_pregunta, wraplength=450, bg="#f0f0f0")
        self.pregunta_label.pack(pady=(50, 30))

        # Frame para agrupar los botones Sí/No
        botones_frame = tk.Frame(self.game_frame, bg="#f0f0f0")
        botones_frame.pack()

        # Botón de SÍ. 'command=self.responder_si'
        self.si_button = tk.Button(botones_frame, text="Sí", font=self.font_boton, 
                                   width=10, command=self.responder_si, bg="#2ecc71", fg="white", relief=tk.FLAT)
        self.si_button.pack(side=tk.LEFT, padx=15, pady=20) # 'side=tk.LEFT' los pone uno al lado del otro.

        # Botón de NO. 'command=self.responder_no'
        self.no_button = tk.Button(botones_frame, text="No", font=self.font_boton, 
                                  width=10, command=self.responder_no, bg="#e74c3c", fg="white", relief=tk.FLAT)
        self.no_button.pack(side=tk.LEFT, padx=15, pady=20)
        
        # Botón para volver al inicio. 'side=tk.BOTTOM' lo pone abajo.
        self.reiniciar_button = tk.Button(self.game_frame, text="Volver al Inicio", 
                                        font=("Helvetica", 10), command=self.show_welcome_frame)
        self.reiniciar_button.pack(side=tk.BOTTOM, pady=20)

    # --- Sección 2b: Lógica de Navegación (Cambio de Pantalla) ---

    def show_game_frame(self):
        """Oculta la pantalla de bienvenida y muestra la de juego."""
        # .pack_forget() quita el widget de la vista sin destruirlo.
        self.welcome_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        
        # (Re)Cargamos los datos por si se aprendió algo en una partida anterior.
        self.personajes, self.preguntas = cargar_datos()
        # Inicia la lógica del juego.
        self.iniciar_juego()

    def show_welcome_frame(self):
        """Oculta la pantalla de juego y muestra la de bienvenida."""
        self.game_frame.pack_forget()
        self.welcome_frame.pack(fill="both", expand=True)

    # --- Sección 3: Lógica del Juego (Motor de Inferencia) ---

    def iniciar_juego(self):
        """
        (RE)INICIA EL JUEGO.
        Establece todas las variables de la partida a sus valores iniciales.
        """
        # Hacemos una copia de la lista de personajes. Esta lista se irá reduciendo.
        self.posibles = self.personajes.copy()
        # Lista para no repetir preguntas.
        self.preguntas_hechas = []
        # Diccionario para guardar las respuestas del usuario (para el aprendizaje).
        self.respuestas_dadas = {}
        # Variable para guardar la pregunta actual.
        self.atributo_actual = None
        
        # *** LÓGICA DE 5 PREGUNTAS (REQUERIMIENTO) ***
        # Se reinicia el contador de preguntas a 0 para esta partida.
        self.numero_de_preguntas = 0 
        
        # Habilitamos los botones (podrían estar deshabilitados de una partida anterior).
        self.si_button.config(state=tk.NORMAL)
        self.no_button.config(state=tk.NORMAL)
        
        # Hacemos la primera pregunta.
        self.siguiente_pregunta()

    # Estas dos funciones simples "conectan" los botones (eventos) con la lógica principal.
    def responder_si(self):
        self.procesar_respuesta('si') # Llama a la lógica con la respuesta 'si'

    def responder_no(self):
        self.procesar_respuesta('no') # Llama a la lógica con la respuesta 'no'

    def procesar_respuesta(self, respuesta):
        """
        Este es el CORAZÓN del motor de inferencia (Encadenamiento Adelante).
        Filtra la lista de 'posibles' basándose en la 'respuesta' del usuario.
        """
        if self.atributo_actual:
            # Guardamos la respuesta para el aprendizaje
            self.respuestas_dadas[self.atributo_actual] = respuesta
            
            # --- FILTRADO (LA REGLA) ---
            # REGLA: SI el usuario dio una respuesta,
            # ENTONCES nos quedamos solo con los personajes que coinciden con esa respuesta.
            
            posibles_actualizados = [] # Lista temporal
            for personaje in self.posibles:
                # .get() busca el atributo; si no existe, no da error.
                if personaje.get(self.atributo_actual) == respuesta:
                    # Si coincide, lo añadimos a la lista de actualizados.
                    posibles_actualizados.append(personaje)
            
            # Reemplazamos la lista de sospechosos con la lista filtrada.
            self.posibles = posibles_actualizados

        # --- REVISIÓN DE ESTADO (Lógica de 5 Preguntas) ---
        
        if not self.posibles:
            # CASO 1: Lista vacía. No quedan sospechosos.
            messagebox.showwarning("¡Oh no!", "No conozco a ningún personaje que coincida con tus respuestas.")
            self.iniciar_juego() # Reinicia el juego
        elif len(self.posibles) == 1:
            # CASO 2: Solo queda 1. ¡GANA EL JUEGO!
            # Adivinamos, aunque no hayamos llegado a 5 preguntas.
            self.adivinanza_final(self.posibles[0])
        elif self.numero_de_preguntas == 5:
            # CASO 3: (REQUERIMIENTO) Llegamos a 5 preguntas y aún hay varios.
            # Forzamos una adivinanza al azar entre los restantes.
            messagebox.showinfo("¡Momento de la verdad!", "He hecho 5 preguntas. ¡Voy a adivinar!")
            self.adivinanza_final(random.choice(self.posibles)) # Elige uno al azar de los que quedan
        else:
            # CASO 4: Menos de 5 preguntas y más de 1 sospechoso.
            # Continuamos a la siguiente pregunta.
            self.siguiente_pregunta()

    def siguiente_pregunta(self):
        """Busca y muestra la siguiente pregunta aleatoria."""
        
        # 1. Crea una lista de atributos que AÚN NO se han preguntado.
        atributos_disponibles = [attr for attr in self.preguntas.keys() if attr not in self.preguntas_hechas]
        
        if not atributos_disponibles:
            # 2. Si no hay más preguntas (y aún hay >1 sospechoso), adivina al azar.
            self.adivinanza_final(random.choice(self.posibles))
        else:
            # 3. Si hay preguntas disponibles:
            
            # *** LÓGICA DE 5 PREGUNTAS (REQUERIMIENTO) ***
            self.numero_de_preguntas += 1 # Aumenta el contador.
            
            # Elige una pregunta al azar de las disponibles.
            self.atributo_actual = random.choice(atributos_disponibles)
            # La añade a la lista de "hechas" para no repetirla.
            self.preguntas_hechas.append(self.atributo_actual)
            # Actualiza el texto de la etiqueta en la GUI.
            self.pregunta_label.config(text=self.preguntas[self.atributo_actual])

    # --- Sección 4: Adivinanza Final y Aprendizaje ---

    def adivinanza_final(self, personaje_adivinado):
        """
        Muestra la ventana emergente (Toplevel) con la imagen del personaje.
        'personaje_adivinado' es el diccionario del personaje que el sistema cree que es.
        """
        # Deshabilita los botones de Sí/No de la ventana principal.
        self.si_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)

        # Crea una NUEVA ventana (Toplevel) que se superpone a la principal.
        self.ventana_adivinanza = tk.Toplevel(self.root)
        self.ventana_adivinanza.title("¿Es este tu personaje?")
        self.ventana_adivinanza.geometry("300x450")
        self.ventana_adivinanza.configure(bg="#f0f0f0")
        # .grab_set() "congela" la ventana principal. No puedes hacer clic
        # en la ventana de atrás hasta que cierres esta.
        self.ventana_adivinanza.grab_set() 

        try:
            # 1. Obtiene el nombre del archivo de imagen desde el JSON.
            # .get("imagen", "default.png") es una forma segura: si no encuentra la clave "imagen",
            # usará "default.png" para evitar un error.
            nombre_img_personaje = personaje_adivinado.get("imagen", "default.png")
            # 2. Crea la ruta completa a la imagen del personaje.
            ruta_img_personaje = os.path.join(script_dir, 'imagenes', nombre_img_personaje)
            
            # 3. Carga y redimensiona la imagen.
            img = Image.open(ruta_img_personaje)
            img = img.resize((250, 250), Image.LANCZOS)
            self.photo_personaje = ImageTk.PhotoImage(img) # La convierte para Tkinter

            # 4. La muestra en la nueva ventana.
            img_label = tk.Label(self.ventana_adivinanza, image=self.photo_personaje, bg="#f0f0f0")
            img_label.image = self.photo_personaje
            img_label.pack(pady=(20, 10))

        except FileNotFoundError:
            tk.Label(self.ventana_adivinanza, text=f"No se encontró la imagen '{nombre_img_personaje}'", 
                     font=("Helvetica", 10, "italic"), fg="red", bg="#f0f0f0").pack(pady=20)
        except Exception as e:
            tk.Label(self.ventana_adivinanza, text=f"Error al cargar imagen: {e}", 
                     font=("Helvetica", 10, "italic"), fg="red", bg="#f0f0f0").pack(pady=20)

        # Muestra el nombre del personaje.
        tk.Label(self.ventana_adivinanza, text=f"¿Tu personaje es\n{personaje_adivinado['nombre']}?", 
                 font=self.font_pregunta, bg="#f0f0f0").pack(pady=10)

        # Crea un frame para los botones de esta ventana.
        botones_frame = tk.Frame(self.ventana_adivinanza, bg="#f0f0f0")
        botones_frame.pack(pady=20)

        # Botón SÍ (en la ventana emergente).
        # 'lambda:' es necesario para pasar argumentos (True/False) a la función 'command'.
        si_btn_adivinanza = tk.Button(botones_frame, text="Sí, ¡adivinaste!", font=self.font_boton, 
                                     width=15, command=lambda: self.procesar_adivinanza_final(True, personaje_adivinado), 
                                     bg="#2ecc71", fg="white", relief=tk.FLAT)
        si_btn_adivinanza.pack(side=tk.LEFT, padx=10)

        # Botón NO (en la ventana emergente).
        no_btn_adivinanza = tk.Button(botones_frame, text="No", font=self.font_boton, 
                                     width=10, command=lambda: self.procesar_adivinanza_final(False, personaje_adivinado), 
                                     bg="#e74c3c", fg="white", relief=tk.FLAT)
        no_btn_adivinanza.pack(side=tk.LEFT, padx=10)

    def procesar_adivinanza_final(self, respuesta, personaje_adivinado):
        """
        Esta función maneja el clic de SÍ/NO en la ventana de adivinanza.
        'respuesta' será True si el usuario hizo clic en "Sí", False si hizo clic en "No".
        """
        # Cerramos la ventana emergente ('Toplevel')
        self.ventana_adivinanza.destroy()

        if respuesta: # Si el usuario dijo "Sí"
            messagebox.showinfo("¡Gané!", "¡Excelente! He adivinado una vez más.")
            self.iniciar_juego() # Reinicia el juego principal
        else: # Si el usuario dijo "No"
            # Inicia el proceso de aprendizaje (Adquisición de Conocimiento).
            self.iniciar_aprendizaje(personaje_adivinado)

    def iniciar_aprendizaje(self, personaje_adivinado):
        """
        Inicia el proceso de aprendizaje de un nuevo personaje
        usando ventanas emergentes (simpledialog).
        """
        # 1. Pide el nombre del personaje correcto.
        nombre_correcto = simpledialog.askstring("Aprender", "¡Me has vencido! ¿Cuál era el nombre de tu personaje?")
        # Si el usuario presiona "Cancelar", 'nombre_correcto' será 'None'.
        if not nombre_correcto:
            self.iniciar_juego() # Reinicia sin aprender
            return # Termina la función aquí.

        # 2. Pide la pregunta diferenciadora.
        nueva_pregunta = simpledialog.askstring("Aprender", f"Escribe una pregunta (si/no) que diferencie a {personaje_adivinado['nombre']} de {nombre_correcto}:")
        if not nueva_pregunta:
            self.iniciar_juego()
            return

        # 3. Pide la respuesta para el personaje NUEVO.
        respuesta_para_nuevo = simpledialog.askstring("Aprender", f"Y para {nombre_correcto}, ¿la respuesta a esa pregunta sería 'si' o 'no'?")
        if not respuesta_para_nuevo or respuesta_para_nuevo.lower() not in ['si', 'no']:
            messagebox.showerror("Error", "Respuesta inválida. El aprendizaje ha fallado.")
            self.iniciar_juego()
            return
        
        respuesta_para_nuevo = respuesta_para_nuevo.lower()

        # --- ACTUALIZACIÓN DE LA BASE DE CONOCIMIENTOS EN MEMORIA ---
        
        # 4. Convierte la pregunta en una clave de atributo (ej. "¿Es reina?" -> "es_reina")
        nuevo_atributo = nueva_pregunta.lower().replace(" ", "_").replace("¿", "").replace("?","")
        
        # 5. Añade la nueva pregunta al diccionario de preguntas (en memoria).
        self.preguntas[nuevo_atributo] = nueva_pregunta
        
        # 6. Crea el nuevo personaje usando las respuestas que el usuario ya dio en esta partida.
        nuevo_personaje = self.respuestas_dadas.copy()
        nuevo_personaje['nombre'] = nombre_correcto
        # Añade la respuesta a la nueva pregunta.
        nuevo_personaje[nuevo_atributo] = respuesta_para_nuevo
        # (Opcional) Deberías añadirle un nombre de archivo de imagen
        # nuevo_personaje['imagen'] = f"{nombre_correcto.lower().split(' ')[0]}.png"
        
        # 7. Actualiza al personaje con el que nos confundimos.
        # Recorremos la lista MAESTRA 'self.personajes'.
        for p in self.personajes:
            if p['nombre'] == personaje_adivinado['nombre']:
                # Le asignamos la respuesta OPUESTA.
                p[nuevo_atributo] = 'no' if respuesta_para_nuevo == 'si' else 'si'
            elif nuevo_atributo not in p:
                # Asigna un valor por defecto ('no') a todos los demás personajes
                # para que la base de datos siga siendo consistente.
                p[nuevo_atributo] = 'no' 
        
        # 8. Añade el diccionario del nuevo personaje a la lista maestra.
        self.personajes.append(nuevo_personaje)
        
        # 9. Llama a la función para GUARDAR estos cambios en el archivo JSON.
        guardar_datos(self.personajes, self.preguntas)
        
        messagebox.showinfo("¡Gracias!", "¡He actualizado mi base de conocimientos! El juego se reiniciará.")
        self.iniciar_juego() # Reinicia el juego.

# --- Sección 5: Ejecución Principal ---

# Este bloque 'if' especial solo se ejecuta cuando corres este archivo
# directamente (y no cuando es importado por otro script).
if __name__ == "__main__":
    # 1. Crea la ventana raíz (principal) de Tkinter.
    root = tk.Tk()
    # 2. Crea una "instancia" de nuestra clase AdivinaQuienGUI,
    #    pasándole la ventana raíz para que la controle.
    app = AdivinaQuienGUI(root)
    # 3. Inicia el "bucle principal" (mainloop) de Tkinter.
    #    Esto mantiene la ventana abierta y esperando a que el usuario
    #    haga clic en botones, escriba, etc. (controlado por eventos).
    root.mainloop()