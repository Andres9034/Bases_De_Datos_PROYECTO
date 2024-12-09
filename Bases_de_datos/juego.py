import mysql.connector
import json

conexion = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="pilk12345",
    database="MundoMultijugador"
)
cursor = conexion.cursor()


cursor.execute("SELECT * FROM jugadores")
for jugador in cursor.fetchall():
    print(jugador)

def crear_jugador(nombre_usuario, nivel, puntuacion, equipo, inventario):
    query = """
    INSERT INTO jugadores (nombre_usuario, nivel, puntuacion, equipo, inventario)
    VALUES (%s, %s, %s, %s, %s)
    """
    datos = (nombre_usuario, nivel, puntuacion, equipo, json.dumps(inventario))
    cursor.execute(query, datos)
    conexion.commit()1
    print(f"Jugador '{nombre_usuario}' creado con éxito.")


def consultar_jugadores():
    cursor.execute("SELECT * FROM jugadores")
    for jugador in cursor.fetchall():
        print(jugador)


def actualizar_jugador(id_jugador, nivel):
    query = "UPDATE jugadores SET nivel = %s WHERE id = %s"
    cursor.execute(query, (nivel, id_jugador))
    conexion.commit()


def eliminar_jugador(id_jugador):
    query = "DELETE FROM jugadores WHERE id = %s"
    cursor.execute(query, (id_jugador,))
    conexion.commit()
    

class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_ubicacion(self, ubicacion):
        if ubicacion not in self.nodos:
            self.nodos[ubicacion] = []

    def agregar_ruta(self, desde, hacia, peso):
        self.nodos[desde].append((hacia, peso))

def guardar_grafo_en_db(grafo, nombre_mundo):
    grafo_json = json.dumps(grafo.nodos)
    query = "INSERT INTO mundos (grafo_serializado) VALUES (%s)"
    cursor.execute(query, (grafo_json,))
    conexion.commit()
    

class Nodo:
    def __init__(self, fecha, resultado):
        self.fecha = fecha
        self.resultado = resultado
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, nodo):
        if not self.raiz:
            self.raiz = nodo
        else:
            self._insertar_recursivo(self.raiz, nodo)

    def _insertar_recursivo(self, actual, nodo):
        if nodo.fecha < actual.fecha:
            if actual.izquierda is None:
                actual.izquierda = nodo
            else:
                self._insertar_recursivo(actual.izquierda, nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nodo
            else:
                self._insertar_recursivo(actual.derecha, nodo)

def agregar_item_inventario(id_jugador, item, descripcion):
    cursor.execute("SELECT inventario FROM jugadores WHERE id = %s", (id_jugador,))
    inventario = json.loads(cursor.fetchone()[0]) if cursor.fetchone()[0] else {}
    inventario[item] = descripcion
    query = "UPDATE jugadores SET inventario = %s WHERE id = %s"
    cursor.execute(query, (json.dumps(inventario), id_jugador))
    conexion.commit()
    
cursor.execute("CALL actualizar_ranking()")
conexion.commit()
    
equipos = {
    "equipo1": {"jugadores": [], "promedio_puntuacion": 0},
    "equipo2": {"jugadores": [], "promedio_puntuacion": 0},
}

def menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar un jugador")
        print("2. Consultar jugadores")
        print("3. Crear un mundo virtual")
        print("4. Jugar una partida")
        print("5. Consultar ranking")
        print("6. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            registrar_jugador()
        elif opcion == "2":
            consultar_jugadores()
        elif opcion == "3":
            crear_mundo_virtual()
        elif opcion == "4":
            jugar_partida()
        elif opcion == "5":
            consultar_ranking()
        elif opcion == "6":
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

def registrar_jugador():
    nombre_usuario = input("Nombre del jugador: ")
    nivel = int(input("Nivel inicial: "))
    puntuacion = int(input("Puntuación inicial: "))
    equipo = input("Equipo: ")
    inventario = {} 
    
    query = "INSERT INTO jugadores (nombre_usuario, nivel, puntuacion, equipo, inventario) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nombre_usuario, nivel, puntuacion, equipo, json.dumps(inventario)))
    conexion.commit()
    
    crear_jugador(nombre_usuario, nivel, puntuacion, equipo, inventario)
    print(f"Jugador '{nombre_usuario}' registrado con éxito.")
    
def consultar_jugadores():
    print("\n--- Lista de jugadores ---")
    cursor.execute("SELECT * FROM jugadores")
    for jugador in cursor.fetchall():
        print(jugador)

def crear_mundo_virtual():
    print("\n--- Creación de mundo virtual ---")
    nombre_mundo = input("Nombre del mundo: ")
    grafo = Grafo()
    
    
    while True:
        ubicacion = input("Agregar ubicación (deja vacío para terminar): ")
        if not ubicacion:
            break
        grafo.agregar_ubicacion(ubicacion)
    
    
    while True:
        desde = input("Desde (deja vacío para terminar): ")
        if not desde:
            break
        hacia = input("Hacia: ")
        peso = int(input("Peso: "))
        grafo.agregar_ruta(desde, hacia, peso)
    
    guardar_grafo_en_db(grafo, nombre_mundo)
    print(f"Mundo '{nombre_mundo}' creado con éxito.")

def jugar_partida():
    print("\n--- Iniciar una partida ---")
    equipo1 = input("Nombre del Equipo 1: ")
    equipo2 = input("Nombre del Equipo 2: ")
    resultado = input("Resultado (e.g., 'Equipo1 ganó'): ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    
    
    nodo = Nodo(fecha, resultado)
    arbol.insertar(nodo)
    
   
    query = "INSERT INTO partidas (fecha, equipo1, equipo2, resultado) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (fecha, equipo1, equipo2, resultado))
    conexion.commit()
    
    print("Partida registrada con éxito.")

def consultar_ranking():
    print("\n--- Ranking Global ---")
    cursor.execute("SELECT * FROM ranking ORDER BY posicion ASC")
    for jugador in cursor.fetchall():
        print(jugador)

if __name__ == "__main__":
    menu()
    