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

memoria = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]
mostrar_memoria(memoria)

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

p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=4)
p2 = Proceso(pid="P2", tamano_memoria=300, tiempo_cpu=2)

asignar_first_fit(p1, memoria)
asignar_first_fit(p2, memoria)
mostrar_memoria(memoria)

# ==============================================================================
# BLOQUE 3: COALESCENCIA Y LIBERACIÓN DE MEMORIA
# ==============================================================================

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

print("\n--- LIBERANDO P1 ---")
liberar_memoria("P1", memoria)
mostrar_memoria(memoria)

print("\n--- LIBERANDO P2 (AQUÍ OCURRE LA COALESCENCIA) ---")
liberar_memoria("P2", memoria)
mostrar_memoria(memoria)

# ==============================================================================
# BLOQUE 4: SIMULACIÓN WORST-FIT (PEOR AJUSTE)
# ==============================================================================

def asignar_worst_fit(proceso, lista_memoria):
    # Recorre todos los huecos y elige el MÁS GRANDE
    peor_i      = -1
    peor_tamano = -1

    for i, bloque in enumerate(lista_memoria):
        if bloque.libre and bloque.tamano >= proceso.tamano_memoria:
            if bloque.tamano > peor_tamano:
                peor_tamano = bloque.tamano
                peor_i      = i

    if peor_i == -1:
        print(f"[ESPERA] No hay memoria para {proceso.pid}. Pasa a Esperando Memoria.")
        proceso.estado = "ESPERANDO_MEMORIA"
        return False

    bloque   = lista_memoria[peor_i]
    sobrante = bloque.tamano - proceso.tamano_memoria

    bloque.libre  = False
    bloque.pid    = proceso.pid
    bloque.tamano = proceso.tamano_memoria

    if sobrante > 0:
        lista_memoria.insert(peor_i + 1, BloqueMemoria(
            inicio=bloque.inicio + proceso.tamano_memoria,
            tamano=sobrante, libre=True, pid=None
        ))

    proceso.estado = "LISTO"
    print(f"[OK] {proceso.pid} ({proceso.tamano_memoria} KB) → entró en hueco de {peor_tamano} KB")
    return True

memoria_wf = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]

print("\n=== TICK 0: Memoria inicial ===")
mostrar_memoria(memoria_wf)

print("=== TICK 1: llega P1 (200 KB) ===")
wf_p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=5)
asignar_worst_fit(wf_p1, memoria_wf)
mostrar_memoria(memoria_wf)

print("=== TICK 2: llega P2 (300 KB) ===")
wf_p2 = Proceso(pid="P2", tamano_memoria=300, tiempo_cpu=3)
asignar_worst_fit(wf_p2, memoria_wf)
mostrar_memoria(memoria_wf)

print("=== TICK 3: llega P3 (100 KB) ===")
wf_p3 = Proceso(pid="P3", tamano_memoria=100, tiempo_cpu=1)
asignar_worst_fit(wf_p3, memoria_wf)
mostrar_memoria(memoria_wf)

print("=== TICK 4: terminan P1 y P3 ===")
liberar_memoria("P1", memoria_wf)
liberar_memoria("P3", memoria_wf)
mostrar_memoria(memoria_wf)

print("=== TICK 5: llega P4 (190 KB) ===")
wf_p4 = Proceso(pid="P4", tamano_memoria=190, tiempo_cpu=2)
asignar_worst_fit(wf_p4, memoria_wf)
mostrar_memoria(memoria_wf)

print("=== TICK 6: termina P2 ===")
liberar_memoria("P2", memoria_wf)
mostrar_memoria(memoria_wf)

print("=== TICK 7: llega P5 (300 KB) ===")
wf_p5 = Proceso(pid="P5", tamano_memoria=300, tiempo_cpu=4)
asignar_worst_fit(wf_p5, memoria_wf)
mostrar_memoria(memoria_wf)

# ==============================================================================
# BLOQUE 4: SIMULACIÓN FIRST-FIT TICK A TICK
# ==============================================================================

memoria_ff = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]

print("\n=== INICIAL: Memoria limpia ===")
mostrar_memoria(memoria_ff)

# TIC 1: llega P1 (200 KB)
print("=== TIC 1: llega P1 (200 KB) ===")
ff_p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=4)
asignar_first_fit(ff_p1, memoria_ff)
mostrar_memoria(memoria_ff)

# TIC 2: llega P2 (300 KB)
print("=== TIC 2: llega P2 (300 KB) ===")
ff_p2 = Proceso(pid="P2", tamano_memoria=300, tiempo_cpu=2)
asignar_first_fit(ff_p2, memoria_ff)
mostrar_memoria(memoria_ff)

# TIC 3: llega P3 (100 KB)
print("=== TIC 3: llega P3 (100 KB) ===")
ff_p3 = Proceso(pid="P3", tamano_memoria=100, tiempo_cpu=1)
asignar_first_fit(ff_p3, memoria_ff)
mostrar_memoria(memoria_ff)

# TIC 4: estado con P1, P2 y P3 cargados (ya mostrado arriba)
# ---> es el mismo estado que el resultado del TIC 3

# TIC 5: termina P1 → hueco de 200 KB al inicio, P2 y P3 siguen en el medio
print("=== TIC 5: termina P1 ===")
liberar_memoria("P1", memoria_ff)
mostrar_memoria(memoria_ff)

# TIC 6: termina P3 → su hueco (100 KB) queda pegado a la cola (421 KB)
# coalescencia los fusiona en un único hueco de 521 KB
print("=== TIC 6: termina P3 (coalescencia con la cola) ===")
liberar_memoria("P3", memoria_ff)
mostrar_memoria(memoria_ff)

# TIC 7: termina P2 → su hueco (300 KB) queda entre dos huecos libres
# coalescencia fusiona los tres: 200 + 300 + 521 = 1024 KB libre
print("=== TIC 7 / TIC 8: termina P2 (coalescencia total) ===")
liberar_memoria("P2", memoria_ff)
mostrar_memoria(memoria_ff)