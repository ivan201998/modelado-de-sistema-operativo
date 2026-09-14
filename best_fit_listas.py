# BEST-FIT CON LISTA DE BLOQUES
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


def agregar_best_fit(pid, tamano):

    mejor_posicion = -1
    mejor_tamano = None

    for i in range(len(memoria)):

        bloque = memoria[i]

        tamano_bloque = bloque[1]
        estado = bloque[2]

        if estado == "Libre" and tamano_bloque >= tamano:

            if mejor_tamano is None:
                mejor_posicion = i
                mejor_tamano = tamano_bloque

            elif tamano_bloque < mejor_tamano:
                mejor_posicion = i
                mejor_tamano = tamano_bloque

    if mejor_posicion == -1:
        print(f"No hay espacio para {pid}")
        return

    bloque = memoria[mejor_posicion]

    inicio = bloque[0]
    tamano_original = bloque[1]

    memoria[mejor_posicion] = [
        inicio,
        tamano,
        "Ocupado",
        pid
    ]

    sobrante = tamano_original - tamano

    if sobrante > 0:
        memoria.insert(
            mejor_posicion + 1,
            [inicio + tamano, sobrante, "Libre", "Ninguno"]
        )

    print(f"{pid} ingresó usando Best-Fit")


def liberar_proceso(pid):

    for bloque in memoria:
        if bloque[3] == pid:
            bloque[2] = "Libre"
            bloque[3] = "Ninguno"
            break

    # Coalescencia: unir huecos libres contiguos.
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


# EJEMPLO BASADO EN TU PLANILLA
agregar_best_fit("P1", 200)
agregar_best_fit("P2", 300)
agregar_best_fit("P3", 100)

liberar_proceso("P1")
agregar_best_fit("P4", 180)

liberar_proceso("P2")
agregar_best_fit("P5", 250)

mostrar_memoria()