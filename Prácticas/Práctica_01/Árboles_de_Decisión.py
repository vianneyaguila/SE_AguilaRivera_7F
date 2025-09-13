#   Este árbol de decisión simula la forma en que decidirías qué hacer con tu dinero :

    # Si tienes deudas , lo más recomendable es pagarlas primero .
    # Si no tienes deudas y tu objetivo es ahorrar , entonces el árbol recomienda guardar dinero .
    # Si tienes un buen ingreso, no tienes deudas y tu objetivo es disfrutar , entonces puedes permitirte gastar en entretenimiento .
# ----------------------------------------------
# Árbol de Decisión: Decidir si ahorrar o gastar
# ----------------------------------------------

from sklearn import tree
import matplotlib.pyplot as plt

# -------------------------
# Datos de ejemplo (situaciones)
# -------------------------
# Ingreso: 0 = bajo, 1 = medio, 2 = alto
# Deudas: 0 = no, 1 = sí
# Objetivo: 0 = disfrutar, 1 = ahorrar, 2 = necesario

X = [
    [0, 1, 2],  # Ingreso bajo, con deudas, objetivo necesario → Pagar deudas
    [1, 1, 2],  # Ingreso medio, con deudas, necesario → Pagar deudas
    [2, 1, 1],  # Ingreso alto, con deudas, objetivo ahorrar → Ahorrar
    [2, 0, 0],  # Ingreso alto, sin deudas, objetivo disfrutar → Gastar en entretenimiento
    [1, 0, 1],  # Ingreso medio, sin deudas, objetivo ahorrar → Ahorrar
    [0, 0, 0],  # Ingreso bajo, sin deudas, objetivo disfrutar → Gastar poco
]

# Etiquetas de decisión:
# 0 = Pagar deudas, 1 = Ahorrar, 2 = Gastar en entretenimiento
y = [0, 0, 1, 2, 1, 2]

# -------------------------
# Entrenamos el árbol de decisión
# -------------------------
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

# -------------------------
# Visualización del árbol
# -------------------------
plt.figure(figsize=(10,6))
tree.plot_tree(clf, 
               feature_names=["Ingreso", "Deudas", "Objetivo"], 
               class_names=["Pagar Deudas", "Ahorrar", "Gastar"], 
               filled=True, rounded=True)
plt.show()

# -------------------------
# Ejemplo de predicción
# -------------------------
# Caso: ingreso medio, sin deudas, objetivo disfrutar
decision = clf.predict([[1, 0, 0]])  

acciones = ["Pagar Deudas", "Ahorrar", "Gastar en Entretenimiento"]
print(f"💡 Decisión recomendada: {acciones[decision[0]]}")
