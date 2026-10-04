import os

# DICCIONARIO: cada color tiene su etiqueta y su código de consola
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    codigo = COLORES.get(color, COLORES["BLANCO"])   # .get evita el error si el color no existe
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    # Devuelve True si el usuario respondió algo de la tupla RESPUESTAS_SI
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    # Validación mínima: un @, algo antes, algo después y un punto al final
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")


# =====================================================================
#Pruebas =====================================================================

if __name__ == "__main__":
    # 1. Probar impresión de título y limpieza de pantalla
    imprimir_titulo("MI PRIMERA PRUEBA DE FUNCIONES")

    # 2. Probar mensajes de estado (Éxito, Error, Info)
    imprimir_info("Iniciando la fase de pruebas automatizadas...")
    imprimir_exito("La pantalla se limpió y el título se imprimió correctamente.")
    imprimir_error("Esto es una simulación de un error (¡pero todo va bien!).")
    print()

    # 3. Probar la función de colores con un color personalizado y uno inexistente
    imprimir_info("Probando colores personalizados:")
    imprimir_color("Texto en amarillo brillante", "AMARILLO")
    imprimir_color("Texto con color inexistente (debe salir blanco)", "MORADO")
    print()

    # 4. Probar la validación de emails con diferentes casos
    imprimir_info("Probando validador de correos electrónicos:")
    
    emails_a_probar = [
        "correo@dominio.com",  # Válido
        "sin_arroba.com",      # Inválido
        "@sin_usuario.com",    # Inválido
        "usuario@nodotcom",    # Inválido
    ]

    for email in emails_a_probar:
        if es_email_valido(email):
            imprimir_exito(f"El correo '{email}' es VÁLIDO.")
        else:
            imprimir_error(f"El correo '{email}' es INVÁLIDO.")
    print()

    # 5. Probar la función de confirmación interactiva
    imprimir_info("Probando interacción con el usuario:")
    if confirmar("¿Te gustó cómo funcionan las pruebas hasta ahora?"):
        imprimir_exito("¡Excelente! El sistema de confirmación funciona.")
    else:
        imprimir_error("Oh, marcaste que no o tu respuesta no está en la lista.")
    
    print("\n--- Fin de la prueba ---")