#ACTIVIDAD EN EQUIPO (En Google Colab o Editor Python):

#1. Crear una memoria limpia de 1024 KB.
#2. Cargar con First-Fit estos tres procesos:
   #- P1: 200 KB
   #- P2: 300 KB
   #- P3: 150 KB
#3. Mostrar la memoria (debe haber 3 ocupados y 1 libre).
#4. Liberar solo el proceso P2 (el del medio) y mostrar la memoria.
#5. Liberar P1 y P3. Mostrar la memoria final.
   #> Verificación: El resultado final DEBE ser 1 único bloque de 1024 KB libre.


# ==============================================================================
# BLOQUE 1: ESTRUCTURAS BÁSICAS Y MEMORIA INICIAL
# ==============================================================================

class Proceso:
    def __init__(self, pid, tamano_memoria, tiempo_cpu):
        self.pid = pid
        self.tamano_memoria = tamano_memoria
        self.tiempo_cpu = tiempo_cpu
        self.estado = "NUEVO"

class BloqueMemoria:
    def __init__(self, inicio, tamano, libre=True, pid=None):
        self.inicio = inicio
        self.tamano = tamano
        self.libre = libre
        self.pid = pid

def mostrar_memoria(lista_memoria):
    print("\n--- ESTADO DE LA MEMORIA (1024 KB) ---")
    for b in lista_memoria:
        fin = b.inicio + b.tamano - 1          # fin real del bloque
        if b.libre:
            print(f"[{b.inicio} KB a {fin} KB] -> Tamaño: {b.tamano} KB | ESTADO: LIBRE")
        else:
            print(f"[{b.inicio} KB a {fin} KB] -> Tamaño: {b.tamano} KB | ESTADO: OCUPADO por {b.pid}")
    print("---------------------------------------\n")

def asignar_first_fit(proceso, lista_memoria):
    for i, bloque in enumerate(lista_memoria):
        if bloque.libre and bloque.tamano >= proceso.tamano_memoria:
            if bloque.tamano > proceso.tamano_memoria:
                sobrante = bloque.tamano - proceso.tamano_memoria
                nuevo_libre = BloqueMemoria(
                    inicio=bloque.inicio + proceso.tamano_memoria,
                    tamano=sobrante,
                    libre=True,
                    pid=None
                )
                bloque.tamano = proceso.tamano_memoria
                bloque.libre = False
                bloque.pid = proceso.pid
                lista_memoria.insert(i + 1, nuevo_libre)
            else:
                bloque.libre = False
                bloque.pid = proceso.pid
            proceso.estado = "LISTO"
            print(f"[OK] Se asignaron {proceso.tamano_memoria} KB al proceso {proceso.pid}")
            return True
    print(f"[ESPERA] No hay memoria para {proceso.pid}. Pasa a Esperando Memoria.")
    proceso.estado = "ESPERANDO_MEMORIA"
    return False

def coalescencia(lista_memoria):
    i = 0
    while i < len(lista_memoria) - 1:
        actual = lista_memoria[i]
        siguiente = lista_memoria[i + 1]
        if actual.libre and siguiente.libre:
            actual.tamano += siguiente.tamano
            lista_memoria.pop(i + 1)
        else:
            i += 1

def liberar_memoria(pid, lista_memoria):
    for bloque in lista_memoria:
        if bloque.pid == pid:
            bloque.libre = True
            bloque.pid = None
            print(f"[LIBERACIÓN] Se liberó la memoria del proceso {pid}")
            coalescencia(lista_memoria)
            return True
    print(f"No se encontró el proceso {pid} en memoria.")
    return False

# ==============================================================================
# ACTIVIDAD: FIRST-FIT + COALESCENCIA
# ==============================================================================

# 1. Memoria limpia de 1024 KB
memoria = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]

# 2. Cargar los tres procesos con First-Fit
p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=4)
p2 = Proceso(pid="P2", tamano_memoria=300, tiempo_cpu=2)
p3 = Proceso(pid="P3", tamano_memoria=150, tiempo_cpu=3)

asignar_first_fit(p1, memoria)
asignar_first_fit(p2, memoria)
asignar_first_fit(p3, memoria)

# 3. Mostrar: 3 ocupados y 1 libre
print("\n=== PASO 3: P1, P2 y P3 cargados ===")
mostrar_memoria(memoria)

# 4. Liberar solo P2 (el del medio)
# P1 y P3 siguen ocupados a sus lados, así que el hueco queda aislado
print("=== PASO 4: liberando P2 ===")
liberar_memoria("P2", memoria)
mostrar_memoria(memoria)

# 5. Liberar P1 y P3
# Al liberar P1: su hueco toca el de P2 → coalescencia los junta
# Al liberar P3: el bloque resultante toca la cola → segunda fusión
# Resultado esperado: 1 único bloque de 1024 KB libre
print("=== PASO 5: liberando P1 y P3 ===")
liberar_memoria("P1", memoria)
liberar_memoria("P3", memoria)
mostrar_memoria(memoria)

# Verificación final
assert len(memoria) == 1 and memoria[0].libre and memoria[0].tamano == 1024
print("VERIFICACIÓN OK: queda 1 único bloque de 1024 KB libre.")