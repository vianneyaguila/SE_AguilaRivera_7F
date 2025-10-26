import tkinter as tk
from tkinter import messagebox, simpledialog  # Importamos ventanas emergentes
import random
import json
import sys
import os

# --- Sección 1: Manejo de la Base de Conocimientos (JSON) ---
# Esta parte es IDÉNTICA a tu script anterior.
# Se encarga de encontrar, cargar y guardar el archivo JSON.

script_dir = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(script_dir, 'basedatos_bridgerton.json')

def cargar_datos():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos['personajes'], datos['preguntas']
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo '{DB_FILE}'. Asegúrate de que está en la misma carpeta.")
        sys.exit()
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"El archivo '{DB_FILE}' tiene un formato JSON inválido.")
        sys.exit()

def guardar_datos(personajes, preguntas):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            datos_completos = {'preguntas': preguntas, 'personajes': personajes}
            json.dump(datos_completos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        messagebox.showerror("Error", f"Error al guardar los datos: {e}")

# --- Sección 2: Clase de la Aplicación del Juego ---
# Aquí es donde ocurre toda la magia de la interfaz.

class AdivinaQuienGUI:
    def __init__(self, root):
        # 1. Configuración de la ventana principal
        self.root = root
        self.root.title("Adivina Quién: Bridgerton")
        self.root.geometry("500x250") # Tamaño de la ventana (ancho x alto)

        # 2. Cargar los datos al iniciar
        self.personajes, self.preguntas = cargar_datos()

        # 3. Crear los "widgets" (elementos gráficos)
        
        # Etiqueta para mostrar la pregunta
        self.pregunta_label = tk.Label(root, text="Piensa en un personaje...", font=("Helvetica", 14), wraplength=450)
        self.pregunta_label.pack(pady=30) # .pack() es el "pegamento" que lo pone en la ventana

        # Un "frame" o marco para agrupar los botones de Sí/No
        self.botones_frame = tk.Frame(root)
        self.botones_frame.pack()

        # Botón de SÍ
        self.si_button = tk.Button(self.botones_frame, text="Sí", font=("Helvetica", 12), width=10, command=self.responder_si)
        self.si_button.pack(side=tk.LEFT, padx=15) # side=tk.LEFT pone un botón al lado del otro

        # Botón de NO
        self.no_button = tk.Button(self.botones_frame, text="No", font=("Helvetica", 12), width=10, command=self.responder_no)
        self.no_button.pack(side=tk.LEFT, padx=15)

        # Botón de Reiniciar
        self.reiniciar_button = tk.Button(root, text="Reiniciar Juego", font=("Helvetica", 10), command=self.iniciar_juego)
        self.reiniciar_button.pack(side=tk.BOTTOM, pady=20)

        # 4. Iniciar el juego por primera vez
        self.iniciar_juego()

    def iniciar_juego(self):
        """Reinicia todas las variables para una nueva partida."""
        self.posibles = self.personajes.copy()
        self.preguntas_hechas = []
        self.respuestas_dadas = {}
        self.atributo_actual = None
        
        # Habilitamos los botones por si estaban deshabilitados
        self.si_button.config(state=tk.NORMAL)
        self.no_button.config(state=tk.NORMAL)
        
        # Hacemos la primera pregunta
        self.siguiente_pregunta()

    def responder_si(self):
        """Se llama cuando el usuario presiona 'Sí'."""
        self.procesar_respuesta('si')

    def responder_no(self):
        """Se llama cuando el usuario presiona 'No'."""
        self.procesar_respuesta('no')

    def procesar_respuesta(self, respuesta):
        """Lógica de filtrado (tu motor de inferencia)."""
        if self.atributo_actual:
            self.respuestas_dadas[self.atributo_actual] = respuesta
            
            # Filtramos la lista de posibles
            posibles_actualizados = []
            for personaje in self.posibles:
                if personaje.get(self.atributo_actual) == respuesta:
                    posibles_actualizados.append(personaje)
            self.posibles = posibles_actualizados

        # Comprobamos el estado del juego
        if not self.posibles:
            # No quedan sospechosos
            messagebox.showwarning("¡Oh no!", "No conozco a ningún personaje que coincida con tus respuestas.")
            self.iniciar_juego()
        elif len(self.posibles) == 1:
            # Solo queda 1: ¡vamos a adivinar!
            self.adivinanza_final(self.posibles[0])
        else:
            # Quedan varios: siguiente pregunta
            self.siguiente_pregunta()

    def siguiente_pregunta(self):
        """Busca y muestra la siguiente pregunta aleatoria."""
        atributos_disponibles = [attr for attr in self.preguntas.keys() if attr not in self.preguntas_hechas]
        
        if not atributos_disponibles:
            # No hay más preguntas, pero sí varios sospechosos. Adivinamos al azar.
            self.adivinanza_final(random.choice(self.posibles))
        else:
            self.atributo_actual = random.choice(atributos_disponibles)
            self.preguntas_hechas.append(self.atributo_actual)
            # Actualizamos el texto de la etiqueta
            self.pregunta_label.config(text=self.preguntas[self.atributo_actual])

    def adivinanza_final(self, personaje_adivinado):
        """Deshabilita botones y pregunta si hemos acertado."""
        # Deshabilitamos los botones de Sí/No mientras adivinamos
        self.si_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)
        
        # Usamos una ventana emergente para la pregunta final
        respuesta = messagebox.askyesno("Adivinanza Final", f"¿Tu personaje es {personaje_adivinado['nombre']}?")
        
        if respuesta: # Si el usuario dice "Sí"
            messagebox.showinfo("¡Gané!", "¡Excelente! He adivinado una vez más.")
            self.iniciar_juego()
        else: # Si el usuario dice "No"
            self.iniciar_aprendizaje(personaje_adivinado)

    def iniciar_aprendizaje(self, personaje_adivinado):
        """Inicia el proceso de aprendizaje con ventanas emergentes."""
        
        # Pedimos los datos usando 'simpledialog'
        nombre_correcto = simpledialog.askstring("Aprender", "¡Me has vencido! ¿Cuál era el nombre de tu personaje?")
        if not nombre_correcto:
            self.iniciar_juego() # Canceló el aprendizaje
            return

        nueva_pregunta = simpledialog.askstring("Aprender", f"Escribe una pregunta que diferencie a {personaje_adivinado['nombre']} de {nombre_correcto}:")
        if not nueva_pregunta:
            self.iniciar_juego()
            return

        respuesta_para_nuevo = simpledialog.askstring("Aprender", f"Y para {nombre_correcto}, ¿la respuesta a esa pregunta sería 'si' o 'no'?")
        if not respuesta_para_nuevo or respuesta_para_nuevo.lower() not in ['si', 'no']:
            messagebox.showerror("Error", "Respuesta inválida. El aprendizaje ha fallado.")
            self.iniciar_juego()
            return
        
        respuesta_para_nuevo = respuesta_para_nuevo.lower()

        # --- Esta es la misma lógica de aprendizaje de tu script anterior ---
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
        
        # Guardamos los cambios en el archivo JSON
        guardar_datos(self.personajes, self.preguntas)
        
        messagebox.showinfo("¡Gracias!", "¡He actualizado mi base de conocimientos! El juego se reiniciará.")
        self.iniciar_juego()

# --- Sección 3: Ejecución Principal ---
# Esto es lo que "enciende" la aplicación

if __name__ == "__main__":
    root = tk.Tk()           # Crea la ventana principal
    app = AdivinaQuienGUI(root) # Carga nuestra clase de juego en la ventana
    root.mainloop()          # Mantiene la ventana abierta esperando clics