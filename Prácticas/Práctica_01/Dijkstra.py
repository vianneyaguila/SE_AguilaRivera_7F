# ----------------------------------------------
# Algoritmo de Dijkstra aplicado a la vida diaria:
# Escenario: Ir desde CASA hasta la ESCUELA.
# El algoritmo calcula la ruta más corta considerando
# calles y paradas de autobús como puntos intermedios.
# ----------------------------------------------

# --- Importación de Bibliotecas ---
import heapq  # Fundamental para implementar la cola de prioridad, que hace eficiente a Dijkstra.
import networkx as nx  # Biblioteca para la creación, manipulación y estudio de grafos.
import matplotlib.pyplot as plt  # Se usa para dibujar y mostrar el grafo.


# ----------------------------------------------------
# Función principal que implementa el Algoritmo de Dijkstra
# ----------------------------------------------------
def dijkstra_ruta(grafo, inicio, destino):
    """
    Encuentra la ruta más corta entre 'inicio' y 'destino' en un grafo ponderado.
    Retorna la ruta como una lista de nodos y la distancia total.
    """

    # --- Inicialización ---
    # Paso 1: Crear una estructura para almacenar la distancia más corta desde 'inicio' a cada nodo.
    # Al principio, no conocemos ninguna ruta, así que asumimos que todas las distancias son infinitas.
    distancias = {nodo: float('inf') for nodo in grafo}
    
    # La distancia desde el nodo de inicio hasta sí mismo es siempre 0.
    distancias[inicio] = 0

    # Diccionario para reconstruir el camino al final. Guardará el nodo previo en la ruta más corta.
    # Ejemplo: si para llegar a 'PLAZA' el camino más corto es desde 'PARADA_2', guardaremos predecesores['PLAZA'] = 'PARADA_2'.
    predecesores = {nodo: None for nodo in grafo}

    # Conjunto para llevar un registro de los nodos que ya hemos visitado y procesado.
    # Esto evita ciclos y trabajo innecesario.
    visitados = set()

    # --- Cola de Prioridad ---
    # Es el corazón de la eficiencia de Dijkstra. Siempre nos dará el nodo no visitado más cercano al origen.
    # Guardamos tuplas (distancia_acumulada, nombre_del_nodo).
    # heapq la mantendrá ordenada por el primer elemento (la distancia).
    cola = [(0, inicio)]

    # --- Bucle Principal del Algoritmo ---
    # El bucle se ejecuta mientras haya nodos por visitar en la cola de prioridad.
    while cola:
        # Paso 2: Extraer el nodo con la menor distancia de la cola.
        # heapq.heappop() garantiza que sea el nodo no visitado más cercano al inicio.
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Si ya hemos encontrado una ruta más corta a este nodo y lo procesamos, lo ignoramos.
        if nodo_actual in visitados:
            continue

        # Marcamos el nodo actual como visitado. Ya no necesitamos volver a procesarlo.
        visitados.add(nodo_actual)

        # Si hemos llegado al destino, podríamos detenernos aquí como optimización.
        # Sin embargo, el algoritmo completo explora hasta que la cola esté vacía.
        if nodo_actual == destino:
            break # Optimización: si solo nos interesa un destino, podemos parar.

        # Paso 3: Explorar los vecinos del nodo actual.
        # 'vecino' es el nodo conectado (ej: 'PARADA_1') y 'peso' es la distancia (ej: 5).
        for vecino, peso in grafo[nodo_actual].items():
            
            # Calculamos la nueva distancia desde el 'inicio' hasta este 'vecino' pasando por el 'nodo_actual'.
            nueva_distancia = distancia_actual + peso

            # Paso 4: Relajación del arco.
            # Si la nueva ruta que acabamos de encontrar es más corta que la que teníamos registrada...
            if nueva_distancia < distancias[vecino]:
                # ...actualizamos la distancia más corta para ese vecino.
                distancias[vecino] = nueva_distancia
                # Guardamos que para llegar a 'vecino', el mejor camino pasa por 'nodo_actual'.
                predecesores[vecino] = nodo_actual
                # Añadimos el vecino a la cola de prioridad con su nueva y mejorada distancia.
                heapq.heappush(cola, (nueva_distancia, vecino))

    # --- Reconstrucción del Camino ---
    # Una vez que el bucle termina, 'distancias' y 'predecesores' tienen la información completa.
    # Ahora, construimos la ruta yendo hacia atrás desde el 'destino' hasta el 'inicio'.
    camino = []
    actual = destino
    while actual is not None:
        camino.insert(0, actual) # Insertamos al principio para que la ruta quede en el orden correcto.
        actual = predecesores[actual] # Saltamos al nodo anterior en la ruta.

    # --- Presentación de Resultados ---
    # Si la distancia al destino sigue siendo infinita, significa que no hay un camino posible.
    if distancias[destino] == float('inf'):
        print(f"No existe una ruta de {inicio} a {destino}")
        return None, None

    # Imprimimos los resultados en la consola.
    print(f"\n🚶 Ruta más corta desde {inicio} hasta {destino}")
    print(f"Distancia total: {distancias[destino]} km")
    print(f"Ruta: {' → '.join(camino)}")

    return camino, distancias[destino]


# ------------------------------------------
# Función para visualizar el grafo y la ruta
# ------------------------------------------
def graficar_ruta(grafo, ruta_destacada=None):
    """
    Visualiza el grafo de rutas y resalta en rojo la ruta más corta encontrada.
    """
    # Crea un objeto de grafo dirigido (las flechas importan) de NetworkX.
    G = nx.DiGraph()

    # Itera sobre el diccionario del grafo para añadir las aristas (conexiones) y sus pesos.
    for origen in grafo:
        for destino, peso in grafo[origen].items():
            G.add_edge(origen, destino, weight=peso)

    # Calcula la posición de los nodos para que el dibujo se vea bien (algoritmo de Fruchterman-Reingold).
    pos = nx.spring_layout(G, seed=42)
    
    # Obtiene las etiquetas de las aristas (los pesos o distancias).
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Define los colores de las aristas. Por defecto grises, pero rojas si forman parte de la ruta encontrada.
    edge_colors = []
    if ruta_destacada:
        # Crea una lista de tuplas (origen, destino) para la ruta destacada.
        ruta_edges = list(zip(ruta_destacada, ruta_destacada[1:]))
        for u, v in G.edges():
            if (u, v) in ruta_edges:
                edge_colors.append('red') # Ruta más corta
            else:
                edge_colors.append('gray') # Otras rutas
    else:
        edge_colors = 'gray'

    # --- Dibujado con Matplotlib ---
    # Dibuja los nodos.
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_weight='bold', arrows=True)
    # Dibuja las etiquetas de las distancias en las aristas.
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # Dibuja las aristas con los colores que definimos antes.
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=3)

    plt.title("Ruta más corta: Casa → Escuela")
    plt.show() # Muestra la ventana con el gráfico.


# ---------------------------------
# Definición del Grafo y Ejecución
# ---------------------------------
# Un diccionario de diccionarios representa el grafo.
# La clave externa es el nodo de origen.
# La clave interna es el nodo destino, y el valor es el peso (distancia).
grafo_ciudad = {
    'CASA': {'PARADA_1': 5, 'PARADA_2': 7},
    'PARADA_1': {'PARADA_3': 3, 'PLAZA': 6},
    'PARADA_2': {'PLAZA': 2},
    'PARADA_3': {'ESCUELA': 4},
    'PLAZA': {'ESCUELA': 5},
    'ESCUELA': {} # El destino no tiene salidas en este modelo.
}

# Puntos de inicio y fin de nuestro viaje.
origen = 'CASA'
destino = 'ESCUELA'

# Llamamos a la función principal para que haga el cálculo.
camino, distancia_total = dijkstra_ruta(grafo_ciudad, origen, destino)

# Si se encontró un camino, llamamos a la función para visualizarlo.
if camino:
    graficar_ruta(grafo_ciudad, camino)