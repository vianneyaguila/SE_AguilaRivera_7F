# El de Modus Tollens: niegas el consecuente para deducir la negación del antecedente.
# Modus Tollens: Si el motor funciona, entonces el coche arranca

def motor_funciona(coche_arranca: bool) -> bool:
    """
    Determina si el motor funciona usando Modus Tollens.
    """
    # Regla: Si el motor funciona, el coche arranca
    if not coche_arranca:
        return False  # Conclusión: el motor no funciona
    else:
        return True  # No podemos concluir que el motor funciona solo porque arranca

# Uso
coche_arranca = False
if motor_funciona(coche_arranca):
    print("El motor funciona.")
else:
    print("El motor no funciona.")
