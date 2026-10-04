import json

# TUPLA de campos: el orden y los nombres son fijos, por eso no es una lista.
# La usan el Controlador y la Vista para no repetir textos sueltos.
CAMPOS_CLIENTE = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")


class Cliente:
    """MODELO: representa a un cliente."""

    def __init__(self, id_cliente, nombre, apellido, email, telefono, ciudad, direccion):
        self.id = id_cliente          # no usamos 'id' como parámetro: es una función de Python
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        # Objeto -> diccionario (listo para JSON)
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        # Diccionario -> objeto. Es un método de la CLASE, no de un objeto:
        # se usa así -> Cliente.desde_diccionario({...})
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["telefono"],
            datos.get("ciudad", ""),      # .get por si el archivo es de una versión vieja
            datos.get("direccion", ""),
        )

    def a_json(self):
        return json.dumps(self.a_diccionario(), ensure_ascii=False)

    def __str__(self):
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.email}"


class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones."""

    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet                      # ej: EST2026001
        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        self.notas = notas if notas else {}
        # CONJUNTO: materias en las que está inscrito, sin repetidos
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        # add() no duplica: si ya estaba inscrito, no pasa nada
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)
        # setdefault crea la lista vacía la primera vez que aparece la materia
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        todas = []
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)
        if not todas:
            return 0
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        # INTERSECCIÓN de conjuntos: qué materias comparten dos estudiantes
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            # y al leer lo volvemos a convertir en set
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"



# =====================================================================
# SCRIPT DE PRUEBA ()
# =====================================================================

if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DE MODELOS (POO) ---\n")

    # =================================================================
    # 1. PRUEBA DE LA CLASE CLIENTE
    # =================================================================
    print("[1] Probando Clase Cliente:")
    
    # Creamos un objeto cliente
    cliente1 = Cliente(1, "Carlos", "Mendoza", "carlos@correo.com", "555-1234", "Quito", "Av. Amazonas")
    
    # Probar método __str__ y nombre completo
    print(f"   -> Cliente creado (str): {cliente1}")
    print(f"   -> Nombre completo: {cliente1.obtener_nombre_completo()}")
    
    # Probar conversión a diccionario (Simulación para guardar en JSON)
    diccionario_cliente = cliente1.a_diccionario()
    print(f"   -> ¿Se convirtió a diccionario?: {isinstance(diccionario_cliente, dict)}")
    
    # Probar reconstrucción desde diccionario (Simulación de lectura)
    cliente_recuperado = Cliente.desde_diccionario(diccionario_cliente)
    print(f"   -> ¿Reconstruido con éxito?: {cliente_recuperado.nombre} == {cliente1.nombre}")
    print()


    # =================================================================
    # 2. PRUEBA DE LA CLASE ESTUDIANTE
    # =================================================================
    print("[2] Probando Clase Estudiante (Notas y Conjuntos):")
    
    # Creamos dos estudiantes para la prueba
    estudiante1 = Estudiante(101, "Ana", "Gómez", "ana@correo.com", "EST2026001")
    estudiante2 = Estudiante(102, "Luis", "Pérez", "luis@correo.com", "EST2026002")

    # Agregar notas y probar materias automáticas
    estudiante1.agregar_nota("Matemática", 18)
    estudiante1.agregar_nota("Matemática", 20)
    estudiante1.agregar_nota("Programación", 19)
    
    # El estudiante 2 comparte una materia
    estudiante2.inscribir_materia("Programación")
    estudiante2.inscribir_materia("Historia")

    # Verificar promedios y materias
    print(f"   -> Estudiante 1 (str): {estudiante1}")
    print(f"   -> Materias de Ana: {estudiante1.materias}")
    print(f"   -> ¿Promedio correcto? (Debe ser 19.0): {estudiante1.obtener_promedio()}")
    
    # Probar la intersección de conjuntos (materias en común)
    compartidas = estudiante1.materias_en_comun(estudiante2)
    print(f"   -> Materias en común entre Ana y Luis: {compartidas} (Debe ser {{'Programación'}})")
    print()


    # =================================================================
    # 3. PRUEBA DE COMPATIBILIDAD CON JSON (Evitar errores con sets)
    # =================================================================
    print("[3] Probando Compatibilidad con JSON:")
    
    diccionario_estudiante = estudiante1.a_diccionario()
    # Verificamos si las materias dejaron de ser un 'set' y pasaron a ser una lista
    tipo_materias_dicc = type(diccionario_estudiante["materias"])
    print(f"   -> En el diccionario, las materias son de tipo: {tipo_materias_dicc.__name__} (Evita error de JSON)")
    
    # Volvemos a cargarlo para ver si se transforma de nuevo en un 'set' original
    estudiante_recuperado = Estudiante.desde_diccionario(diccionario_estudiante)
    tipo_materias_recup = type(estudiante_recuperado.materias)
    print(f"   -> Al recuperarlo, las materias vuelven a ser tipo: {tipo_materias_recup.__name__}")

    print("\n--- ¡Todas las funciones y métodos pasaron la prueba con éxito! ---")
