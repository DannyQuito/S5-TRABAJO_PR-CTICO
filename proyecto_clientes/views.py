from models import Cliente, CAMPOS_CLIENTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/clientes.json")

# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """CONJUNTO con los emails ya usados. Sirve para detectar duplicados al instante."""
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_cliente(datos):
    """datos: diccionario con las claves de CAMPOS_CLIENTE. Devuelve (exito, mensaje)."""
    try:
        # 1) Normalizo: un diccionario con todos los campos, sin espacios sobrantes
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_CLIENTE}

        # 2) Reviso obligatorios recorriendo la TUPLA
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) Formato del email
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # 4) Duplicado: búsqueda instantánea dentro del CONJUNTO
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        # 5) Creo el objeto del Modelo. ** convierte el diccionario en argumentos
        cliente = Cliente(siguiente_id(), **valores)

        # 6) Agrego a la LISTA y guardo
        registros = gestor.leer()
        registros.append(cliente.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Cliente {cliente.obtener_nombre_completo()} creado con id {cliente.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """LISTA de objetos Cliente."""
    return [Cliente.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_cliente):
    for cliente in obtener_todos():
        if cliente.id == id_cliente:
            return cliente
    return None


# ===================== S · SEARCH =====================

def buscar_clientes(termino):
    """Búsqueda lineal: revisa registro por registro los campos de CAMPOS_BUSCABLES."""
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:                 # recorro la TUPLA de campos
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Cliente.desde_diccionario(registro))
                break                                   # ya coincidió: paso al siguiente cliente
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_cliente(id_cliente, cambios):
    """cambios: diccionario solo con los campos que se quieren modificar."""
    try:
        # DIFERENCIA DE CONJUNTOS: ¿mandaron algún campo que no existe?
        desconocidos = set(cambios) - set(CAMPOS_CLIENTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_cliente):
                return False, "Ese email ya lo usa otro cliente"

        registros = gestor.leer()
        posicion = None
        for indice, registro in enumerate(registros):   # enumerate me da índice y valor
            if registro["id"] == id_cliente:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un cliente con id {id_cliente}"

        registros[posicion].update(cambios)             # actualizo el diccionario en su lugar
        gestor.guardar(registros)
        return True, f"Cliente {id_cliente} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_cliente(id_cliente):
    registros = gestor.leer()
    # Construyo una LISTA NUEVA sin ese registro: nunca borro mientras recorro
    quedan = [registro for registro in registros if registro["id"] != id_cliente]

    if len(quedan) == len(registros):
        return False, f"No existe un cliente con id {id_cliente}"

    gestor.guardar(quedan)
    return True, f"Cliente {id_cliente} eliminado"


# ===================== EXTRA: estadísticas con conjuntos =====================

def estadisticas():
    """Devuelve un DICCIONARIO de resumen. Práctica pura de colecciones."""
    registros = gestor.leer()
    ciudades = {r.get("ciudad", "").title() for r in registros if r.get("ciudad")}
    dominios = {r["email"].split("@")[1].lower() for r in registros if "@" in r["email"]}
    sin_telefono = [r["nombre"] for r in registros if not r.get("telefono")]

    return {
        "total": len(registros),
        "ciudades": sorted(ciudades),
        "dominios": sorted(dominios),
        "sin_telefono": sin_telefono,
    }

# =====================================================================
# SCRIPT DE PRUEBA ()
# =====================================================================

if __name__ == "__main__":
    import os        # <--- AGREGA ESTA LÍNEA AQUÍ
    import shutil

    print("--- INICIANDO PRUEBAS DEL CONTROLADOR (CRUD) ---\n")

    # 1. CONFIGURACIÓN SEGURA PARA PRUEBAS
    # Redirigimos el gestor a un archivo temporal para no dañar tus datos reales
    ruta_original = gestor.ruta
    ruta_temporal = "data/clientes_prueba.json"
    gestor.ruta = ruta_temporal

    # Nos aseguramos de empezar con un archivo limpio y vacío
    if os.path.exists(ruta_temporal):
        os.remove(ruta_temporal)

    print(f"-> Entorno de pruebas configurado en: {ruta_temporal}\n")

    # =================================================================
    # PRUEBA 1: C · CREATE (Creación de clientes y validaciones)
    # =================================================================
    print("1. PROBANDO CREACIÓN (CREATE):")
    
    cliente_valido_1 = {"nombre": "Juan", "apellido": "Pérez", "email": "juan@test.com", "telefono": "12345", "ciudad": "Milagro"}
    cliente_valido_2 = {"nombre": "María", "apellido": "Alvarado", "email": "maria@demo.com", "ciudad": "Guayaquil"} # Sin teléfono
    cliente_invalido_faltante = {"nombre": "Carlos", "email": "carlos@test.com"} # Falta apellido
    cliente_invalido_email = {"nombre": "Luis", "apellido": "Torres", "email": "luis_error.com"} # Email mal estructurado

    # Caso A: Éxito
    exito, msg = crear_cliente(cliente_valido_1)
    print(f"   [OK Esperado]  {msg if exito else 'Falló'}")
    
    # Agregar segundo cliente para tener más datos
    crear_cliente(cliente_valido_2)

    # Caso B: Faltan campos obligatorios
    exito, msg = crear_cliente(cliente_invalido_faltante)
    print(f"   [Error Validado] Faltan campos: {msg if not exito else 'Pasó de largo'}")

    # Caso C: Email inválido
    exito, msg = crear_cliente(cliente_invalido_email)
    print(f"   [Error Validado] Formato de email: {msg if not exito else 'Pasó de largo'}")

    # Caso D: Email duplicado
    exito, msg = crear_cliente(cliente_valido_1) # Intentamos meter a Juan otra vez
    print(f"   [Error Validado] Email duplicado: {msg if not exito else 'Pasó de largo'}")
    print()

    # =================================================================
    # PRUEBA 2: R · READ & S · SEARCH (Lectura y búsquedas)
    # =================================================================
    print("2. PROBANDO LECTURA Y BÚSQUEDA (READ & SEARCH):")
    
    todos = obtener_todos()
    print(f"   -> Total de clientes guardados: {len(todos)} (Debe ser 2)")
    
    # Buscar por ID existente
    cliente_id_1 = obtener_por_id(1)
    print(f"   -> Buscar ID 1: {cliente_id_1.obtener_nombre_completo() if cliente_id_1 else 'No encontrado'}")

    # Búsqueda lineal por texto
    resultados_busqueda = buscar_clientes("Guayaquil")
    print(f"   -> Buscando 'Guayaquil': Encontrados {len(resultados_busqueda)} cliente/s")
    print()

    # =================================================================
    # PRUEBA 3: U · UPDATE (Actualización de datos)
    # =================================================================
    print("3. PROBANDO ACTUALIZACIÓN (UPDATE):")
    
    # Caso A: Actualización exitosa
    cambios_validos = {"telefono": "0999999", "ciudad": "milagro"} # 'milagro' en minúsculas para probar estadísticas
    exito, msg = actualizar_cliente(1, cambios_validos)
    print(f"   [OK Esperado]  {msg}")

    # Caso B: Intentar meter un campo inventado que no existe en CAMPOS_CLIENTE
    cambios_invalidos = {"edad": 25, "ciudad": "Quito"}
    exito, msg = actualizar_cliente(1, cambios_invalidos)
    print(f"   [Error Validado] Campos raros: {msg if not exito else 'Pasó de largo'}")
    print()

    # =================================================================
    # PRUEBA 4: EXTRA · ESTADÍSTICAS (Prueba de colecciones y sets)
    # =================================================================
    print("4. PROBANDO ESTADÍSTICAS:")
    
    resumen = estadisticas()
    print(f"   -> Resumen total generado: {resumen}")
    print(f"   -> Ciudades únicas (Deben salir ordenadas y con Mayúscula): {resumen['ciudades']}")
    print(f"   -> Dominios únicos de email: {resumen['dominios']}")
    print(f"   -> Clientes sin teléfono guardado: {resumen['sin_telefono']} (Debe ser ['María'])")
    print()

    # =================================================================
    # PRUEBA 5: D · DELETE (Eliminación de registros)
    # =================================================================
    print("5. PROBANDO ELIMINACIÓN (DELETE):")
    
    # Caso A: Eliminar ID que existe
    exito, msg = eliminar_cliente(1)
    print(f"   [OK Esperado]  {msg}")

    # Caso B: Intentar borrar un ID que ya no existe
    exito, msg = eliminar_cliente(1)
    print(f"   [Error Validado] Borrar inexistente: {msg if not exito else 'Pasó de largo'}")
    print()

    # =================================================================
    # LIMPIEZA FINAL
    # =================================================================
    # Restauramos la ruta original del gestor y borramos los archivos temporales
    gestor.ruta = ruta_original
    try:
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        # Opcional: si la carpeta 'data' se creó solo para la prueba y está vacía, se puede quitar.
        print("--- PRUEBAS FINALIZADAS CON ÉXITO: Archivos temporales removidos ---")
    except OSError:
        print("--- PRUEBAS FINALIZADAS ---")
