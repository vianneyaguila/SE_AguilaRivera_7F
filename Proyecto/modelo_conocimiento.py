# =========================================================
# 1. modelo_conocimiento.py
# Define la estructura de las reglas para la inferencia.
# =========================================================

class ReglaInferencia:
    """
    Define la estructura de una regla IF-THEN (Si-Entonces). 
    
    Cada regla mapea una respuesta del usuario a una característica deseada en un libro, 
    asignándole un Factor de Certeza (FC).
    """
    
    def __init__(self, respuesta_usuario, atributo_esperado, fc):
        """
        Método constructor para inicializar una nueva ReglaInferencia.

        :param respuesta_usuario: La premisa (IF). La opción seleccionada por el usuario (ej: "Fantasia").
        :param atributo_esperado: La conclusión (THEN). La característica que se busca en el libro (ej: "Genero_Fantasia").
        :param fc: El Factor de Certeza (FC) asociado a esta conclusión (ej: 0.8 o 1.0).
        """
        # Premisa de la regla: La respuesta específica dada por el usuario.
        self.respuesta_usuario = respuesta_usuario
        
        # Conclusión de la regla: El atributo que se busca en los hechos (libros) del sistema.
        self.atributo_esperado = atributo_esperado
        
        # Factor de Certeza: Determina la fuerza con la que esta regla contribuye a la recomendación.
        self.fc = fc
        
    def __repr__(self):
        """
        Define la representación en cadena del objeto, útil para la depuración 
        o para imprimir la regla en un formato legible.
        """
        return (f"IF User chose '{self.respuesta_usuario}' "
                f"THEN expect '{self.atributo_esperado}' (FC: {self.fc})")