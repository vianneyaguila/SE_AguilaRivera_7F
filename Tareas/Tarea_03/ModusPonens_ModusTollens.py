# Modus Ponens : Se aplica cuando afirmamos la premisa “estudio_motor = True” y derivamos que el coche debería arrancar.
# Modus Tollens : Se aplica cuando el coche no arranca , deduciendo que el motor no está funcionando correctamente.
# Ejemplo combinado de Modus Ponens y Modus Tollens
# Contexto: Sistema de diagnóstico de un coche

def diagnosticar_coche(estudio_motor: bool, coche_arranca: bool):
    """
    Diagnóstico del coche usando Modus Ponens y Modus Tollens.
    estudio_motor: indica si se revisó y estudió el motor correctamente
    coche_arranca: indica si el coche arranca
    """

    # ===== MODUS PONENS =====
    # Regla: Si se estudia el motor y todo está correcto, entonces el coche debería arrancar
    if estudio_motor:
        print("Se ha revisado el motor. Según Modus Ponens, el coche debería arrancar.")
        if coche_arranca:
            print("El coche arranca. Diagnóstico correcto.")
        else:
            print("El coche no arranca. Posible fallo inesperado.")

    # ===== MODUS TOLLENS =====
    # Regla: Si el coche no arranca, entonces el motor no está funcionando
    if not coche_arranca:
        print("El coche no arranca. Según Modus Tollens, el motor no funciona correctamente.")
    else:
        print("El coche arranca. No podemos concluir problemas en el motor.")

# ===== EJEMPLOS DE USO =====
# Caso 1: Se revisó el motor y el coche arranca
print("---- Caso 1 ----")
diagnosticar_coche(estudio_motor=True, coche_arranca=True)

print("\n---- Caso 2 ----")
# Caso 2: Se revisó el motor y el coche no arranca
diagnosticar_coche(estudio_motor=True, coche_arranca=False)

print("\n---- Caso 3 ----")
# Caso 3: No se revisó el motor y el coche no arranca
diagnosticar_coche(estudio_motor=False, coche_arranca=False)
