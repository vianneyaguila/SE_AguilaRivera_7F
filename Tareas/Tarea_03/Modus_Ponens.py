# El de Modus Ponens es directo: afirmas la premisa y obtienes la conclusión.
# Modus Ponens: Si estudio, entonces apruebo

def aprobara_examen(estudio: bool) -> bool:
    """
    Determina si el estudiante aprueba el examen usando Modus Ponens.
    """
    # Regla: Si estudió, entonces aprueba
    if estudio:
        return True  # Conclusión: aprueba
    else:
        return False  # No podemos concluir que apruebe

# Uso
estudio = True
if aprobara_examen(estudio):
    print("El estudiante aprobará el examen.")
else:
    print("El estudiante no aprobará el examen o no podemos determinarlo.")

