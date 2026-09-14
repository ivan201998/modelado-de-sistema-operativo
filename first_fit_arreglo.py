# FIRST-FIT CON ARREGLO
# Cada posición representa 1 KB de memoria.

TAMANO_MEMORIA = 1024
memoria = [None] * TAMANO_MEMORIA


def agregar_first_fit(pid, tamano):
    libres = 0

    for i in range(TAMANO_MEMORIA):

        if memoria[i] is None:
            libres += 1
        else:
            libres = 0

        if libres == tamano:
            inicio = i - tamano + 1

            for j in range(inicio, inicio + tamano):
                memoria[j] = pid

            print(f"{pid} ingresó usando First-Fit")
            return

    print(f"No hay espacio para {pid}")


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


# EJEMPLO
agregar_first_fit("P1", 200)
agregar_first_fit("P2", 300)
agregar_first_fit("P3", 100)
mostrar_memoria()

liberar_proceso("P1")
mostrar_memoria()