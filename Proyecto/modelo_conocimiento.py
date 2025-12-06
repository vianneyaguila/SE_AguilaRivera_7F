# ==================================
# 1. modelo_conocimiento.py
# ==================================

class ReglaInferencia:
    """Define la estructura de una regla IF-THEN."""
    def __init__(self, respuesta_usuario, atributo_esperado, fc):
        self.respuesta_usuario = respuesta_usuario
        self.atributo_esperado = atributo_esperado
        self.fc = fc
        
    def __repr__(self):
        return f"IF User chose '{self.respuesta_usuario}' THEN expect '{self.atributo_esperado}' (FC: {self.fc})"