import json
import os


class GestorJSON:
    """Lee y guarda una lista de diccionarios en un archivo JSON."""

    def __init__(self, ruta):
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        # Devuelve SIEMPRE una lista: vacía si el archivo no existe o está dañado
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            # Capturamos errores concretos, nunca un "except:" pelado
            return []

    def guardar(self, datos):
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
        except (TypeError, OSError):
            # TypeError aparece si intentas guardar un set: JSON no lo conoce
            return False


# =====================================================================
# SCRIPT DE PRUEBA ()
# =====================================================================

if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DEL GESTOR JSON ---\n")

    # 1. Definimos el nombre del archivo de prueba
    # Usaremos una carpeta llamada 'datos' para probar que tu código la cree sola.
    ruta_prueba = "datos/usuarios_prueba.json"
    gestor = GestorJSON(ruta_prueba)
    
    print(f"1. Gestor inicializado para la ruta: '{ruta_prueba}'")

    # 2. Probar lectura cuando el archivo NO existe
    # Tu código debería manejarlo devolviendo una lista vacía en lugar de fallar.
    datos_iniciales = gestor.leer()
    print(f"2. Leyendo archivo inexistente... ¿Resultado es lista vacía?: {datos_iniciales == []}")

    # 3. Probar guardar datos válidos (una lista de diccionarios)
    usuarios_a_guardar = [
        {"nombre": "Ana", "email": "ana@correo.com", "activo": True},
        {"nombre": "Carlos", "email": "carlos@correo.com", "activo": False}
    ]
    
    print("3. Intentando guardar una lista de usuarios...")
    se_guardo = gestor.guardar(usuarios_a_guardar)
    
    if se_guardo:
        print("   ✓ ¡Éxito! Los datos se guardaron correctamente.")
    else:
        print("   ✗ Error al guardar los datos.")

    # 4. Probar leer el archivo que acabamos de crear
    print("4. Leyendo el archivo recién creado para verificar el contenido...")
    datos_leidos = gestor.leer()
    print(f"   Datos recuperados: {datos_leidos}")
    print(f"   ¿Los datos coinciden exactamente?: {datos_leidos == usuarios_a_guardar}")

    # 5. Probar el manejo de errores (Guardar algo inválido)
    # Tu comentario en el código dice que un 'set' (conjunto) da TypeError. ¡Vamos a forzarlo!
    print("5. Forzando un error al intentar guardar un 'set' (conjunto de datos)...")
    datos_invalidos = {"manzana", "perra", "platano"} # Esto es un set en Python
    
    se_guardo_invalido = gestor.guardar(datos_invalidos)
    if not se_guardo_invalido:
        print("   ✓ ¡Excelente! El gestor atrapó el TypeError de forma segura y devolvió False.")
    else:
        print("   ✗ Alerta: El gestor no debería haber podido guardar un set.")

    # Limpieza (Opcional): Borrar el archivo de prueba al terminar
    # Si quieres ver el archivo .json en tu computadora, comenta las líneas de abajo.
    try:
        os.remove(ruta_prueba)
        os.rmdir("datos")
        print("\n--- Pruebas finalizadas. Archivos temporales de prueba eliminados con éxito ---")
    except OSError:
        print("\n--- Pruebas finalizadas ---")
