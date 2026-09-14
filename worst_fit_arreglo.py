# WORST-FIT CON ARREGLO
# Cada posición representa 1 KB.

TAMANO_MEMORIA = 1024
memoria = [None] * TAMANO_MEMORIA


def agregar_worst_fit(pid, tamano):

    huecos = []
    inicio = 0

    while inicio < TAMANO_MEMORIA:

        if memoria[inicio] is None:
            fin = inicio

            while fin < TAMANO_MEMORIA and memoria[fin] is None:
                fin += 1

            tamano_hueco = fin - inicio

            if tamano_hueco >= tamano:
                huecos.append([inicio, tamano_hueco])

            inicio = fin

        else:
            inicio += 1

    if len(huecos) == 0:
        print(f"No hay espacio para {pid}")
        return

    peor_hueco = huecos[0]

    for hueco in huecos:
        if hueco[1] > peor_hueco[1]:
            peor_hueco = hueco

    posicion = peor_hueco[0]

    for i in range(posicion, posicion + tamano):
        memoria[i] = pid

    print(f"{pid} ingresó usando Worst-Fit")


def liberar_proceso(pid):
    for i in range(TAMANO_MEMORIA):
        if memoria[i] == pid:
            memoria[i] = None

    print(f"{pid} terminó y liberó memoria")


def mostrar_memoria():
    print("\n--- ESTADO DE LA MEMORIA ---")

    inicio = 0
    actual = memoria[0]

    for i in range(1, TAMANO_MEMORIA):
        if memoria[i] != actual:

            nombre = "LIBRE" if actual is None else actual

            print(f"[{inicio} - {i - 1}] ({i - inicio} KB) --> {nombre}")

            inicio = i
            actual = memoria[i]

    nombre = "LIBRE" if actual is None else actual
    print(f"[{inicio} - {TAMANO_MEMORIA - 1}] ({TAMANO_MEMORIA - inicio} KB) --> {nombre}")


# EJEMPLO BASADO EN TU PLANILLA
agregar_worst_fit("P1", 200)
agregar_worst_fit("P2", 300)
agregar_worst_fit("P3", 100)

liberar_proceso("P1")
liberar_proceso("P3")

agregar_worst_fit("P4", 190)

liberar_proceso("P2")

agregar_worst_fit("P5", 300)

mostrar_memoria()