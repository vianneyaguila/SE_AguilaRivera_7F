# ----------------------------------------------
# Algoritmo de Dijkstra aplicado a la vida diaria:
# Escenario: Ir desde CASA hasta la ESCUELA.
# El algoritmo calcula la ruta más corta considerando
# calles y paradas de autobús como puntos intermedios.
# ----------------------------------------------

import heapq
import networkx as nx
import matplotlib.pyplot as plt


# -------------------------
# Función principal: Dijkstra
# -------------------------
def dijkstra_ruta(grafo, inicio, destino):
    """
    Encuentra la ruta más corta entre 'inicio' y 'destino' en un grafo ponderado.
    Retorna la ruta como lista de nodos y la distancia total.
    """

    # Distancias iniciales: infinito para todos
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0  # El punto de inicio siempre tiene distancia 0

    # Diccionario para guardar el camino recorrido
    predecesores = {nodo: None for nodo in grafo}

    # Conjunto de nodos visitados
    visitados = set()

    # Cola de prioridad (distancia acumulada, nodo)
    cola = [(0, inicio)]

    while cola:
        # Tomamos el nodo con menor distancia
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Si ya lo visitamos, lo saltamos
        if nodo_actual in visitados:
            continue

        visitados.add(nodo_actual)

        # Revisamos vecinos del nodo actual
        for vecino, peso in grafo[nodo_actual].items():
            nueva_distancia = distancia_actual + peso

            # Si encontramos una ruta más corta, actualizamos
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    # Reconstruimos el camino desde destino hasta inicio
    camino = []
    actual = destino
    while actual is not None:
        camino.insert(0, actual)
        actual = predecesores[actual]

    # Validamos si existe camino
    if distancias[destino] == float('inf'):
        print(f"No existe una ruta de {inicio} a {destino}")
        return None, None

    # Mostramos resultado
    print(f"\n🚶 Ruta más corta desde {inicio} hasta {destino}")
    print(f"Distancia total: {distancias[destino]} km")
    print(f"Ruta: {' → '.join(camino)}")

    return camino, distancias[destino]


# -------------------------
# Función para graficar la red de rutas
# -------------------------
def graficar_ruta(grafo, ruta_destacada=None):
    """
    Visualiza el grafo de rutas y resalta en rojo la ruta más corta encontrada.
    """

    G = nx.DiGraph()

    # Agregamos conexiones con su distancia
    for origen in grafo:
        for destino, peso in grafo[origen].items():
            G.add_edge(origen, destino, weight=peso)

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Colores de las rutas
    edge_colors = []
    for u, v in G.edges():
        if ruta_destacada and (u, v) in zip(ruta_destacada, ruta_destacada[1:]):
            edge_colors.append('red')
        else:
            edge_colors.append('gray')

    # Dibujar nodos y conexiones
    nx.draw(G, pos, with_labels=True,
            node_color='lightgreen', node_size=2000,
            font_weight='bold', arrows=True)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=3)

    plt.title("Ruta más corta: Casa → Escuela")
    plt.show()


# -------------------------
# Definición del grafo (mapa de ejemplo)
# -------------------------
grafo_ciudad = {
    'CASA': {'PARADA_1': 5, 'PARADA_2': 7},
    'PARADA_1': {'PARADA_3': 3, 'PLAZA': 6},
    'PARADA_2': {'PLAZA': 2},
    'PARADA_3': {'ESCUELA': 4},
    'PLAZA': {'ESCUELA': 5},
    'ESCUELA': {}
}

# Origen y destino
origen = 'CASA'
destino = 'ESCUELA'

# Ejecutamos el algoritmo
camino, distancia_total = dijkstra_ruta(grafo_ciudad, origen, destino)

# Si existe camino, lo graficamos
if camino:
    graficar_ruta(grafo_ciudad, camino)
