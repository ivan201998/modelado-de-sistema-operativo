# FIRST-FIT CON LISTA DE BLOQUES
# Cada bloque tiene:
# [inicio, tamaño, estado, PID]

memoria = [
    [0, 1024, "Libre", "Ninguno"]
]


def mostrar_memoria():
    print("\n--- ESTADO DE LA MEMORIA ---")
    print("Inicio | Fin | Tamaño | Estado | PID")

    for bloque in memoria:
        inicio = bloque[0]
        tamano = bloque[1]
        estado = bloque[2]
        pid = bloque[3]

        fin = inicio + tamano - 1

        print(inicio, "|", fin, "|", tamano, "KB |", estado, "|", pid)


def agregar_first_fit(pid, tamano):

    for i in range(len(memoria)):
        bloque = memoria[i]

        inicio = bloque[0]
        tamano_bloque = bloque[1]
        estado = bloque[2]

        # First-Fit usa el primer hueco donde entra.
        if estado == "Libre" and tamano_bloque >= tamano:

            memoria[i] = [inicio, tamano, "Ocupado", pid]

            sobrante = tamano_bloque - tamano

            if sobrante > 0:
                memoria.insert(
                    i + 1,
                    [inicio + tamano, sobrante, "Libre", "Ninguno"]
                )

            print(f"{pid} ingresó usando First-Fit")
            return

    print(f"No hay espacio para {pid}")


def liberar_proceso(pid):

    for bloque in memoria:
        if bloque[3] == pid:
            bloque[2] = "Libre"
            bloque[3] = "Ninguno"
            break

    # Unir huecos libres contiguos.
    i = 0

    while i < len(memoria) - 1:

        actual = memoria[i]
        siguiente = memoria[i + 1]

        if actual[2] == "Libre" and siguiente[2] == "Libre":
            actual[1] += siguiente[1]
            memoria.pop(i + 1)
        else:
            i += 1

    print(f"{pid} terminó y liberó memoria")


# EJEMPLO
agregar_first_fit("P1", 200)
agregar_first_fit("P2", 300)
agregar_first_fit("P3", 100)
mostrar_memoria()

liberar_proceso("P1")
mostrar_memoria()