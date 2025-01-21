# %% Importar librerías
from tabulate import tabulate


# %% Pruebas fórmula de peso
def calc_peso_sencillo(aciertos, veces_presentado, epsilon=0.1):
    if veces_presentado == 0:
        return 1

    rendimiento = aciertos / veces_presentado
    peso = 1 - rendimiento + epsilon

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def calc_peso_lineal(aciertos, veces_presentado, epsilon=1):
    if veces_presentado == 0:
        return 1

    rendimiento = aciertos / veces_presentado
    peso = (1 - rendimiento + epsilon) / (1 + veces_presentado)

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def calc_peso_exponencial(aciertos, veces_presentado, epsilon=1):
    if veces_presentado == 0:
        return 1

    rendimiento = aciertos / veces_presentado
    peso = (1 - rendimiento + epsilon) / (1 + veces_presentado**2)

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def calc_peso_ajustado(aciertos, veces_presentado, epsilon=0.1):
    if veces_presentado == 0:
        return 1

    rendimiento = aciertos / veces_presentado
    peso = (
        veces_presentado * (1 - rendimiento + epsilon) /
        (1 + veces_presentado)
    )

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def calc_peso_ajustado_exponencial(aciertos, veces_presentado, epsilon=0.1):
    if veces_presentado == 0:
        return 1

    rendimiento = aciertos / veces_presentado
    peso = (
        (1 - rendimiento + epsilon) * veces_presentado /
        (1 + veces_presentado**2)
    )

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def calc_peso_ajustado_v2(aciertos, veces_presentado, epsilon=0.1):
    if veces_presentado == 0:
        return 1

    rendimiento = aciertos / veces_presentado
    peso = (
        veces_presentado * (1 - rendimiento) /
        (1 + veces_presentado)
    )

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def calc_peso_ajustado_v3(aciertos, veces_presentado):
    if veces_presentado == 0:
        return 1

    # rendimiento = aciertos / veces_presentado
    # peso = (
    #     (
    #         veces_presentado * (1 - rendimiento) +
    #         (rendimiento / veces_presentado)
    #     )
    #     /
    #     (1 + veces_presentado)
    # )
    peso = (
        (
            veces_presentado**2 * (veces_presentado - aciertos) +
            aciertos
        )
        /
        (veces_presentado**2 * (1 + veces_presentado))
    )

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def cotejarFormulas(funciones):
    datos = [
        [0, 0],
        [0, 1], [1, 1],
        [0, 2], [1, 2], [2, 2],
        [0, 3], [1, 3], [2, 3], [3, 3],
        [0, 4], [1, 4], [2, 4], [3, 4], [4, 4],
        [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
        [0, 20], [2, 20], [4, 20], [8, 20], [16, 20], [20, 20],
        [0, 100], [5, 100], [10, 100], [30, 100], [70, 100], [100, 100],

        [0, 1_000], [50, 1_000], [100, 1_000],
        [300, 1_000], [700, 1_000], [1_000, 1_000],

        [0, 10_000], [500, 10_000], [1_000, 10_000],
        [3_000, 10_000], [7_000, 10_000], [10_000, 10_000],

        [0, 100_000], [5_000, 100_000], [10_000, 100_000],
        [30_000, 100_000], [70_000, 100_000], [100_000, 100_000]
    ]
    resultados = {
        "__Datos": datos
    }

    for nombre_func, func_calc_peso in funciones.items():
        resultados[nombre_func] = []

        for dato in datos:
            resultados[nombre_func].append(func_calc_peso(*dato))

    resultados["Datos__"] = datos

    print(tabulate(resultados, headers="keys", tablefmt="fancy_grid"))


funciones = {
    "Sencillo": calc_peso_sencillo,
    "Lineal": calc_peso_lineal,
    "Exponencial": calc_peso_exponencial,
    "Ajustado": calc_peso_ajustado,
    "Ajustado Exponencial": calc_peso_ajustado_exponencial,
    "Ajustado v2": calc_peso_ajustado_v2,
    "Ajustado v3": calc_peso_ajustado_v3
}
cotejarFormulas(funciones)

# %%
