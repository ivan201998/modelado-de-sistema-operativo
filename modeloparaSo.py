
# BLOQUE 1: ESTRUCTURAS BÁSICAS Y MEMORIA INICIAL
# ==============================================================================

# Ficha del Proceso: guarda los datos mínimos que pide la consigna
class Proceso:
    def __init__(self, pid, tamano_memoria, tiempo_cpu):
        self.pid = pid                          # Identificador único (ej: "P1")
        self.tamano_memoria = tamano_memoria    # Memoria en KB
        self.tiempo_cpu = tiempo_cpu            # Ticks necesarios de CPU
        self.estado = "NUEVO"                   # Arranca en estado Nuevo

# Ficha del Bloque de Memoria: representa un casillero físico de la RAM
class BloqueMemoria:
    def __init__(self, inicio, tamano, libre=True, pid=None):
        self.inicio = inicio                    # Dirección en KB donde empieza
        self.tamano = tamano                    # Tamaño en KB del bloque
        self.libre = libre                      # True si está vacío, False si está ocupado
        self.pid = pid                          # PID del proceso que lo ocupa (o None si está libre)

# Función para imprimir la memoria en pantalla como si fuera el Excel
def mostrar_memoria(lista_memoria):
    print("\n--- ESTADO DE LA MEMORIA (1024 KB) ---")
    for b in lista_memoria:
        fin = b.inicio + b.tamano
        if b.libre:
            print(f"[{b.inicio} KB a {fin} KB] -> Tamaño: {b.tamano} KB | ESTADO: LIBRE")
        else:
            print(f"[{b.inicio} KB a {fin} KB] -> Tamaño: {b.tamano} KB | ESTADO: OCUPADO por {b.pid}")
    print("---------------------------------------\n")

# Creamos la memoria inicial: 1 solo bloque de 1024 KB totalmente libre
memoria = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]

# Mostramos cómo arranca la memoria vacía
mostrar_memoria(memoria)

# ==============================================================================
# BLOQUE 2: ALGORITMO FIRST-FIT (PRIMER AJUSTE)
# ==============================================================================

def asignar_first_fit(proceso, lista_memoria):
    # Recorremos bloque por bloque desde el inicio
    for i, bloque in enumerate(lista_memoria):
        # Si el bloque está libre y tiene tamaño suficiente
        if bloque.libre and bloque.tamano >= proceso.tamano_memoria:

            # Caso 1: El hueco es más grande que lo pedido -> Partimos el bloque
            if bloque.tamano > proceso.tamano_memoria:
                sobrante = bloque.tamano - proceso.tamano_memoria

                # Creamos el nuevo bloque libre con el pedazo que sobró
                nuevo_libre = BloqueMemoria(
                    inicio=bloque.inicio + proceso.tamano_memoria,
                    tamano=sobrante,
                    libre=True,
                    pid=None
                )

                # El bloque actual se ajusta al proceso y se marca ocupado
                bloque.tamano = proceso.tamano_memoria
                bloque.libre = False
                bloque.pid = proceso.pid

                # Insertamos el pedazo libre justo después
                lista_memoria.insert(i + 1, nuevo_libre)

            # Caso 2: El hueco mide exactamente lo mismo que pide el proceso
            else:
                bloque.libre = False
                bloque.pid = proceso.pid

            proceso.estado = "LISTO"
            print(f"[OK] Se asignaron {proceso.tamano_memoria} KB al proceso {proceso.pid}")
            return True

    # Si recorrió todo y no encontró lugar suficiente
    print(f"[ESPERA] No hay memoria para {proceso.pid}. Pasa a Esperando Memoria.")
    proceso.estado = "ESPERANDO_MEMORIA"
    return False

# PROBAMOS ASIGNAR DOS PROCESOS
p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=4)
p2 = Proceso(pid="P2", tamano_memoria=300, tiempo_cpu=2)

asignar_first_fit(p1, memoria)
asignar_first_fit(p2, memoria)

# Mostramos cómo quedó partida la memoria
mostrar_memoria(memoria)

# ==============================================================================
# BLOQUE 3: COALESCENCIA Y LIBERACIÓN DE MEMORIA
# ==============================================================================

def coalescencia(lista_memoria):
    i = 0
    # Recorremos la lista comparando cada bloque con el que tiene a su derecha
    while i < len(lista_memoria) - 1:
        actual = lista_memoria[i]
        siguiente = lista_memoria[i + 1]

        # Si ambos bloques contiguos están libres, los fusionamos en uno solo
        if actual.libre and siguiente.libre:
            actual.tamano += siguiente.tamano
            lista_memoria.pop(i + 1)  # Eliminamos el bloque repetido
            # NOTA CLAVE: no aumentamos i, porque el bloque actual ahora es más grande
            # y podría tener que unirse también con el que sigue a la derecha
        else:
            i += 1

def liberar_memoria(pid, lista_memoria):
    for bloque in lista_memoria:
        if bloque.pid == pid:
            bloque.libre = True
            bloque.pid = None
            print(f"[LIBERACIÓN] Se liberó la memoria del proceso {pid}")
            # Inmediatamente después de liberar, aplicamos coalescencia automática
            coalescencia(lista_memoria)
            return True

    print(f"No se encontró el proceso {pid} en memoria.")
    return False

# PROBAMOS LIBERAR P1 Y P2
print("\n--- LIBERANDO P1 ---")
liberar_memoria("P1", memoria)
mostrar_memoria(memoria)

print("\n--- LIBERANDO P2 (AQUÍ OCURRE LA COALESCENCIA) ---")
liberar_memoria("P2", memoria)
mostrar_memoria(memoria)

#probar si queremos liberar P3

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
# ACTIVIDAD EN EQUIPO: FIRST-FIT + LIBERACIÓN
# (pegar como celda nueva, después de los bloques 1 a 3)
# ==============================================================================
print("\n analisis de la actividad")

def verificar_suma(lista_memoria, total=1024):
    # Chequeo de seguridad: los bloques siempre tienen que sumar la memoria total
    suma = sum(b.tamano for b in lista_memoria)
    assert suma == total, f"Los bloques suman {suma} KB y no {total} KB"

# 1. Memoria limpia de 1024 KB (se arma de cero, no depende de las pruebas anteriores)
memoria = [BloqueMemoria(inicio=0, tamano=1024, libre=True)]

# 2. Cargar los tres procesos con First-Fit
p1 = Proceso(pid="P1", tamano_memoria=200, tiempo_cpu=4)
p2 = Proceso(pid="P2", tamano_memoria=300, tiempo_cpu=2)
p3 = Proceso(pid="P3", tamano_memoria=150, tiempo_cpu=3)

for p in (p1, p2, p3):
    asignar_first_fit(p, memoria)

# 3. Mostrar la memoria: tiene que haber 3 ocupados y 1 libre
print("\n=== PASO 3: P1, P2 y P3 cargados ===")
mostrar_memoria(memoria)
assert len([b for b in memoria if not b.libre]) == 3
assert len([b for b in memoria if b.libre]) == 1
verificar_suma(memoria)

# 4. Liberar solo P2 (el del medio): sus vecinos siguen ocupados, no hay fusión
print("\n=== PASO 4: se libera P2 (el del medio) ===")
liberar_memoria("P2", memoria)
mostrar_memoria(memoria)
assert len(memoria) == 4
verificar_suma(memoria)

# 5. Liberar P1 y P3: ahora sí se juntan los tres huecos
print("\n=== PASO 5: se liberan P1 y P3 ===")
liberar_memoria("P1", memoria)
liberar_memoria("P3", memoria)
mostrar_memoria(memoria)

# Verificación final: un único bloque de 1024 KB libre
assert len(memoria) == 1 and memoria[0].libre and memoria[0].tamano == 1024
print("VERIFICACIÓN OK: queda 1 único bloque de 1024 KB libre.")