#Definimos las probabilidades base para cada evento: estudiar, dormir y concentrarse.

    #Creamos un gráfico dirigido ( networkx.DiGraph) que representa el árbol de decisiones/probabilidades .
    #Calculamos todas las ramas posibles usando la regla de la cadena
    #Solo las ramas donde el estudiante está concentrado representan aprobar.
    #Visualizamos el árbol con las probabilidades de cada arista, mostrando cómo se encadenan los eventos.

# ----------------------------------------------
# Regla de la Cadena - Visualización con árbol
# Escenario: Aprobar un examen
# ----------------------------------------------

import matplotlib.pyplot as plt
import networkx as nx

# Crear grafo dirigido
G = nx.DiGraph()

# Nodo raíz
G.add_node("Inicio")

# Nivel 1: Estudiar o no
G.add_edge("Inicio", "Estudia", probability=0.7)
G.add_edge("Inicio", "No Estudia", probability=0.3)

# Nivel 2: Dormir o no
G.add_edge("Estudia", "Duerme", probability=0.8)
G.add_edge("Estudia", "No Duerme", probability=0.2)
G.add_edge("No Estudia", "Duerme", probability=0.6)
G.add_edge("No Estudia", "No Duerme", probability=0.4)

# Nivel 3: Concentración
G.add_edge("Duerme", "Concentrado", probability=0.9)
G.add_edge("Duerme", "No Concentrado", probability=0.1)
G.add_edge("No Duerme", "Concentrado", probability=0.5)
G.add_edge("No Duerme", "No Concentrado", probability=0.5)
G.add_edge("Duerme", "Concentrado NE", probability=0.5)  # Para No Estudia / Duerme
G.add_edge("No Duerme", "Concentrado NE", probability=0.2)  # Para No Estudia / No Duerme

# -------------------------
# Layout jerárquico manual
# -------------------------
pos = {
    "Inicio": (0, 3),
    "Estudia": (-1, 2),
    "No Estudia": (1, 2),
    "Duerme": (-1.5, 1),
    "No Duerme": (-0.5, 1),
    "Duerme NE": (0.5, 1),
    "No Duerme NE": (1.5, 1),
    "Concentrado": (-1.5, 0),
    "No Concentrado": (-0.5, 0),
    "Concentrado NE": (1, 0)
}

# -------------------------
# Dibujar el grafo
# -------------------------
plt.figure(figsize=(12,6))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)

# Etiquetas de probabilidad
edge_labels = nx.get_edge_attributes(G, 'probability')
edge_labels_percent = {k: f"{v*100:.1f}%" for k,v in edge_labels.items()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_percent, font_size=9)

plt.title("Árbol de Probabilidades Mejorado - Aprobar Examen")
plt.axis('off')
plt.show()
