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
        fin = b.inicio + b.tamano
        if b.libre:
            print(f"[{b.inicio} KB a {fin} KB] -> Tamaño: {b.tamano} KB | ESTADO: LIBRE")
        else:
            print(f"[{b.inicio} KB a {fin} KB] -> Tamaño: {b.tamano} KB | ESTADO: OCUPADO por {b.pid}")
    print("---------------------------------------\n")

# ==============================================================================
# BLOQUE 2: ALGORITMO FIRST-FIT (PRIMER AJUSTE)
# ==============================================================================

def asignar_first_fit(proceso, lista_memoria):
    for i, bloque in enumerate(lista_memoria):
        if bloque.libre and bloque.tamano >= proceso.tamano_memoria:
            if bloque.tamano > proceso.tamano_memoria:
                sobrante = bloque.tamano - proceso.tamano_memoria
                nuevo_libre = BloqueMemoria(
                    inicio=bloque.inicio + proceso.tamano_memoria,
                    tamano=sobrante, libre=True, pid=None
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

# ==============================================================================
# BLOQUE 3: COALESCENCIA Y LIBERACIÓN DE MEMORIA
# ==============================================================================

def coalescencia(lista_memoria):
    i = 0
    while i < len(lista_memoria) - 1:
        actual    = lista_memoria[i]
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
            bloque.pid   = None
            print(f"[LIBERACIÓN] Se liberó la memoria del proceso {pid}")
            coalescencia(lista_memoria)
            return True
    print(f"No se encontró el proceso {pid} en memoria.")
    return False

# ==============================================================================
# BLOQUE 4: ACTIVIDAD PRÁCTICA — ROUND ROBIN + FIRST-FIT
# ==============================================================================

QUANTUM_LIMITE = 2

# 1. Crear los tres procesos
p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=4)
p2 = Proceso(pid="P2", tamano_memoria=250, tiempo_cpu=2)
p3 = Proceso(pid="P3", tamano_memoria=100, tiempo_cpu=1)

# 2. Memoria limpia de 1024 KB
memoria = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]

# 3. Asignar memoria con First-Fit e ingresar a cola_listos
print("=== CARGA INICIAL: asignando memoria con First-Fit ===")
cola_listos = []
for p in [p1, p2, p3]:
    asignar_first_fit(p, memoria)
    cola_listos.append(p)

mostrar_memoria(memoria)
print(f"Cola listos: {[p.pid for p in cola_listos]}\n")

# 4. Bucle de ticks Round Robin hasta que los tres procesos terminen
tick           = 0
proceso_actual = None
quantum_actual = 0

print("=== INICIO DE EJECUCIÓN ===\n")

while cola_listos or proceso_actual:

    # Si no hay proceso en CPU, tomar el primero de la cola
    if proceso_actual is None:
        proceso_actual = cola_listos.pop(0)
        quantum_actual = 0
        proceso_actual.estado = "EJECUTANDO"

    tick           += 1
    quantum_actual += 1
    proceso_actual.tiempo_cpu -= 1

    print(f"--- TICK {tick} ---")
    print(f"Ejecutando: {proceso_actual.pid} | CPU restante: {proceso_actual.tiempo_cpu} | Quantum: {quantum_actual}/{QUANTUM_LIMITE}")

    # ¿Terminó?
    if proceso_actual.tiempo_cpu == 0:
        proceso_actual.estado = "TERMINADO"
        print(f"[FIN] {proceso_actual.pid} terminó su trabajo.")
        liberar_memoria(proceso_actual.pid, memoria)
        proceso_actual = None
        quantum_actual = 0

    # ¿Agotó el quantum sin terminar?
    elif quantum_actual >= QUANTUM_LIMITE:
        proceso_actual.estado = "LISTO"
        print(f"[QUANTUM] {proceso_actual.pid} agotó su quantum. Vuelve al final de la cola.")
        cola_listos.append(proceso_actual)
        proceso_actual = None
        quantum_actual = 0

    mostrar_memoria(memoria)
    print(f"Cola listos: {[p.pid for p in cola_listos]}\n")

print("=== TODOS LOS PROCESOS TERMINARON ===")
mostrar_memoria(memoria)