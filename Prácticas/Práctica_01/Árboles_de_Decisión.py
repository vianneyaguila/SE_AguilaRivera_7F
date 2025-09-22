# Importación de las bibliotecas necesarias
import numpy as np  # Se usa para operaciones numéricas, especialmente para crear el array de tiempo (t_eval).
import matplotlib.pyplot as plt  # Es la biblioteca principal para crear gráficas y visualizaciones en Python.
from scipy.integrate import solve_ivp  # 'solve_ivp' es una función específica de la biblioteca SciPy para resolver problemas de valor inicial (Initial Value Problem) de ecuaciones diferenciales ordinarias (EDO).

# --- Definición de los Parámetros Físicos del Microrobot ---
# Estos son valores constantes que describen las propiedades físicas del sistema.
J = 1e-10  # Momento de inercia del microrobot (en kg*m^2). Mide la resistencia del robot a cambiar su velocidad de rotación.
b = 3e-9   # Coeficiente de fricción viscosa (en N*m*s/rad). Representa el amortiguamiento o la fricción que frena al robot.
k = 6e-7   # Constante de torsión del resorte (en N*m/rad). Representa la fuerza de un "resorte" que intenta devolver al robot a su posición de equilibrio.

# --- Definición de la Ecuación Diferencial Ordinaria (EDO) que modela el sistema ---
# Esta función es el corazón del modelo. Describe matemáticamente cómo cambia el estado del robot en el tiempo.
def microrobot_system(t, y):
    # 't' es el tiempo actual (aunque no se usa explícitamente en esta ecuación, es requerido por el solver).
    # 'y' es un vector que contiene el estado actual del sistema. En este caso:
    # y[0] es la posición angular, theta (θ)
    # y[1] es la velocidad angular, omega (ω)
    theta, omega = y

    # La primera ecuación diferencial: la tasa de cambio de la posición angular (dθ/dt) es la velocidad angular (ω).
    dtheta_dt = omega

    # La segunda ecuación diferencial: la tasa de cambio de la velocidad angular (dω/dt) o aceleración angular.
    # Esta es la ecuación de movimiento del sistema: J * (dω/dt) + b * ω + k * θ = 0
    # Despejando dω/dt, obtenemos:
    domega_dt = (-k / J) * theta - (b / J) * omega

    # La función debe devolver una lista o array con las derivadas calculadas [dθ/dt, dω/dt].
    return [dtheta_dt, domega_dt]

# --- Configuración de la Simulación ---

# Condiciones iniciales: el estado del sistema en el tiempo t=0.
# Formato: [posición angular inicial, velocidad angular inicial]
initial_conditions = [1, 0]  # El robot empieza en una posición de 1 radián y con una velocidad de 0 rad/s (en reposo).

# Intervalo de tiempo para la simulación.
t_span = [0, 0.5]  # Se simulará desde el tiempo t=0 segundos hasta t=0.5 segundos.

# Puntos de tiempo específicos donde queremos la solución.
# np.linspace crea 500 puntos equidistantes entre 0 y 0.5. Esto nos dará una gráfica suave.
t_eval = np.linspace(t_span[0], t_span[1], 500)

# --- Resolución de la Ecuación Diferencial ---
# Aquí es donde ocurre la "magia". La función solve_ivp toma el modelo matemático,
# las condiciones iniciales y el intervalo de tiempo, y calcula el estado del sistema en cada punto.
solution = solve_ivp(
    fun=microrobot_system,      # La función que define la EDO.
    t_span=t_span,              # El intervalo de tiempo.
    y0=initial_conditions,      # Las condiciones iniciales.
    t_eval=t_eval               # Los puntos de tiempo para guardar la solución.
)

# El objeto 'solution' contiene varios datos, los más importantes son:
# solution.t: un array con los valores de tiempo (igual a t_eval).
# solution.y: un array donde cada fila corresponde a una de las variables de estado.
#             solution.y[0] es la historia de la posición angular (θ).
#             solution.y[1] es la historia de la velocidad angular (ω).

# --- Visualización de los Resultados ---

# Crear una figura y un conjunto de ejes para la gráfica.
plt.figure(figsize=(10, 6))

# Graficar la posición angular (θ) a lo largo del tiempo.
# En el eje X va el tiempo (solution.t) y en el eje Y va la primera variable de estado (solution.y[0]).
plt.plot(solution.t, solution.y[0], label='Posición Angular θ(t) (rad)')

# Añadir títulos y etiquetas para que la gráfica sea fácil de entender.
plt.title('Respuesta del Microrrobot: Posición Angular vs. Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición Angular (rad)')
plt.grid(True)  # Muestra una cuadrícula para facilitar la lectura de los valores.
plt.legend()    # Muestra la leyenda de la línea graficada (el 'label').
plt.show()      # Muestra la gráfica en una ventana.