# -----------------------------------------------------------------
# Regla de la Cadena - Versión Mejorada
# Escenario: Aprobar un examen (con cálculo y grafo corregido)
# -----------------------------------------------------------------

import matplotlib.pyplot as plt
import networkx as nx

# --- 1. Definición del Grafo (Estructura Lógica Correcta) ---
# Usamos nombres únicos para cada nodo para representar su camino único.
# Ejemplo: 'E_D' = Estudió y Durmió. 'NE_ND' = No Estudió y No Durmió.
G = nx.DiGraph()

# Definimos las probabilidades condicionales en un diccionario para más claridad
# P(B|A) se representa como ('A', 'B'): prob
probs = {
    ('Inicio', 'E'): 0.7,  # P(Estudia)
    ('Inicio', 'NE'): 0.3, # P(No Estudia)

    ('E', 'E_D'): 0.8,     # P(Duerme | Estudia)
    ('E', 'E_ND'): 0.2,    # P(No Duerme | Estudia)
    ('NE', 'NE_D'): 0.6,   # P(Duerme | No Estudia)
    ('NE', 'NE_ND'): 0.4,  # P(No Duerme | No Estudia)

    ('E_D', 'E_D_C'): 0.9,     # P(Concentrado | Estudia, Duerme)
    ('E_D', 'E_D_NC'): 0.1,
    ('E_ND', 'E_ND_C'): 0.5,   # P(Concentrado | Estudia, No Duerme)
    ('E_ND', 'E_ND_NC'): 0.5,
    ('NE_D', 'NE_D_C'): 0.5,   # P(Concentrado | No Estudia, Duerme)
    ('NE_D', 'NE_D_NC'): 0.5,
    ('NE_ND', 'NE_ND_C'): 0.2, # P(Concentrado | No Estudia, No Duerme)
    ('NE_ND', 'NE_ND_NC'): 0.8,
}

# Añadimos las aristas al grafo con sus probabilidades
for (origen, destino), prob in probs.items():
    G.add_edge(origen, destino, probability=prob)

# --- 2. Cálculo de Probabilidades (La Parte Funcional que Faltaba) ---

def calcular_probabilidad_total(grafo, inicio, evento_final_identificador):
    """
    Calcula la probabilidad total de un evento final sumando la probabilidad
    de todas las rutas que llevan a él.
    """
    # Encuentra todos los nodos hoja (los que no tienen sucesores)
    nodos_finales = [nodo for nodo in grafo.nodes() if grafo.out_degree(nodo) == 0]
    
    probabilidad_total = 0
    print("--- Calculando Probabilidades de cada Ruta ---")

    # Iteramos sobre todos los caminos posibles desde el inicio hasta cada hoja
    for nodo_final in nodos_finales:
        # all_simple_paths genera todas las rutas sin ciclos
        for path in nx.all_simple_paths(grafo, source=inicio, target=nodo_final):
            prob_path = 1.0 # Probabilidad inicial de la ruta es 1
            
            # Aplicamos la Regla de la Cadena: multiplicamos las probabilidades
            for i in range(len(path) - 1):
                origen = path[i]
                destino = path[i+1]
                prob_edge = grafo[origen][destino]['probability']
                prob_path *= prob_edge
            
            # Si el nodo final de esta ruta es el que nos interesa, lo sumamos
            if evento_final_identificador in nodo_final:
                print(f"Ruta a favor: {' → '.join(path)} | Probabilidad: {prob_path:.3f}")
                probabilidad_total += prob_path
            else:
                print(f"Ruta en contra: {' → '.join(path)} | Probabilidad: {prob_path:.3f}")

    return probabilidad_total

# Ejecutamos el cálculo. Buscamos todos los resultados que terminen en '_C' (Concentrado)
prob_aprobar = calcular_probabilidad_total(G, 'Inicio', '_C')
print("\n--- Resultado Final ---")
print(f"📊 La probabilidad total de estar concentrado (aprobar) es: {prob_aprobar:.3f} o {prob_aprobar*100:.1f}%")


# --- 3. Visualización del Grafo (Ahora Automática y Correcta) ---
plt.figure(figsize=(16, 10))

# El layout 'dot' de graphviz es excelente para árboles jerárquicos
# Necesita instalar `pygraphviz` (pip install pygraphviz)
try:
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
except ImportError:
    print("\nADVERTENCIA: Para un layout jerárquico perfecto, instala 'graphviz' y 'pygraphviz'.")
    print("Usando un layout estándar como alternativa.")
    pos = nx.spring_layout(G, seed=42)


# Etiquetas personalizadas para los nodos para que sean más legibles en el gráfico
labels = {
    'E': 'Estudia', 'NE': 'No Estudia',
    'E_D': 'Duerme', 'E_ND': 'No Duerme',
    'NE_D': 'Duerme', 'NE_ND': 'No Duerme',
    'E_D_C': 'Concentrado', 'E_D_NC': 'No Concentrado',
    'E_ND_C': 'Concentrado', 'E_ND_NC': 'No Concentrado',
    'NE_D_C': 'Concentrado', 'NE_D_NC': 'No Concentrado',
    'NE_ND_C': 'Concentrado', 'NE_ND_NC': 'No Concentrado',
    'Inicio': 'Inicio'
}

nx.draw(G, pos, labels=labels, with_labels=True, node_size=4000, node_color='skyblue', font_size=10, arrows=True, arrowsize=20)

# Etiquetas de probabilidad en las aristas
edge_labels = {k: f"{v*100:.0f}%" for k, v in probs.items()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9)

plt.title("Árbol de Probabilidades (Corregido y Funcional)")
plt.show()