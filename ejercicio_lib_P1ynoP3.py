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
        fin = b.inicio + b.tamano - 1
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
# BLOQUE 4: COMPACTACIÓN
# ==============================================================================

def compactar(lista_memoria):
    # Junta todos los procesos ocupados al inicio, uno detrás del otro,
    # y deja un único hueco libre al final con todo lo que sobra
    ocupados   = [b for b in lista_memoria if not b.libre]
    total_libre = sum(b.tamano for b in lista_memoria if b.libre)

    cursor = 0
    for b in ocupados:
        b.inicio = cursor
        cursor  += b.tamano

    lista_memoria.clear()
    lista_memoria.extend(ocupados)

    if total_libre > 0:
        lista_memoria.append(BloqueMemoria(inicio=cursor, tamano=total_libre))

    print("[COMPACTACIÓN] Procesos corridos al inicio, hueco único al final.")

# ==============================================================================
# ACTIVIDAD
# ==============================================================================

# 1. Memoria limpia de 1024 KB
memoria = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]

# 2. Cargar P1, P2 y P3
p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=4)
p2 = Proceso(pid="P2", tamano_memoria=300, tiempo_cpu=2)
p3 = Proceso(pid="P3", tamano_memoria=150, tiempo_cpu=3)

asignar_first_fit(p1, memoria)
asignar_first_fit(p2, memoria)
asignar_first_fit(p3, memoria)

print("\n=== PASO 3: P1, P2 y P3 cargados ===")
mostrar_memoria(memoria)

# 4. Liberar P2 (el del medio) → queda aislado entre P1 y P3
print("=== PASO 4: liberando P2 ===")
liberar_memoria("P2", memoria)
mostrar_memoria(memoria)

# 5. Liberar solo P1
# Su hueco (0-199) queda pegado al hueco de P2 (200-499) → coalescencia los fusiona
# P3 sigue ocupado, así que el hueco grande (0-499) queda separado de la cola (650-1023)
print("=== PASO 5: liberando P1 ===")
liberar_memoria("P1", memoria)
mostrar_memoria(memoria)

# 6. Compactar
# P3 se corre al inicio (0-149), el hueco de 874 KB queda todo junto al final
print("=== PASO 6: compactando ===")
compactar(memoria)
mostrar_memoria(memoria)