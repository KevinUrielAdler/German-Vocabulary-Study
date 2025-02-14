# %% Pruebas fórmula de peso
import math

from tabulate import tabulate


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


def calc_peso_ajustado_v2(aciertos, veces_presentado):
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


def calc_peso_ajustado_v4(aciertos, veces_presentado, dias_sin_practicar, lambda_factor=0.1):
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
    # factor_olvido = 1 + (1 - math.exp(-lambda_factor * dias_sin_practicar)) # 1 + (1 - e^(-0.1 * 7))
    # peso = (
    #     (peso * factor_olvido)  # min: 0, max: 2
    #     /
    #     2
    # )
    peso = (
        (
            veces_presentado**2 * (veces_presentado - aciertos) +
            aciertos
        )
        /
        (veces_presentado**2 * (1 + veces_presentado))
    )
    factor_olvido = 2 - math.exp(-lambda_factor * dias_sin_practicar)
    peso = peso * factor_olvido / 2

    if round(peso, 3) > 0 and round(peso, 3) < 1:
        return round(peso, 3)
    elif round(peso, 6) > 0 and round(peso, 6) < 1:
        return round(peso, 6)
    elif round(peso, 9) > 0 and round(peso, 9) < 1:
        return round(peso, 9)
    else:
        return peso


def cotejarFormulas(funciones_params: dict[str, tuple[int, list]]):
    datos = [
        [0, 0],
        [0, 1], [1, 1],
        [0, 2], [1, 2], [2, 2],
        [0, 3], [1, 3], [2, 3], [3, 3],
        [0, 4], [1, 4], [2, 4], [3, 4], [4, 4],
        [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
        [0, 20], [2, 20], [4, 20], [8, 20], [10, 20], [16, 20], [20, 20],

        [0, 100], [5, 100], [10, 100],
        [30, 100], [50, 100], [70, 100], [100, 100],

        [0, 1_000], [50, 1_000], [100, 1_000],
        [300, 1_000], [500, 1_000], [700, 1_000], [1_000, 1_000],

        [0, 10_000], [500, 10_000], [1_000, 10_000],
        [3_000, 10_000], [5_000, 10_000], [7_000, 10_000], [10_000, 10_000],

        [0, 100_000], [5_000, 100_000], [10_000, 100_000],
        [30_000, 100_000], [50_000, 100_000], [
            70_000, 100_000], [100_000, 100_000]
    ]
    resultados = {
        "__Datos": datos
    }

    for nombre_func, (func_calc_peso, params) in funciones_params.items():
        resultados[nombre_func] = []

        for dato in datos:
            parametros = [*dato, *params]
            resultados[nombre_func].append(func_calc_peso(*parametros))

    resultados["Datos__"] = datos

    print(tabulate(resultados, headers="keys", tablefmt="fancy_grid"))


funciones = {
    # "Sencillo": (calc_peso_sencillo,[]),
    # "Lineal": (calc_peso_lineal,[]),
    # "Exponencial": (calc_peso_exponencial,[]),
    # "Ajustado": (calc_peso_ajustado,[]),
    # "Ajustado Exponencial": (calc_peso_ajustado_exponencial,[]),
    # "Ajustado v2": (calc_peso_ajustado_v2,[]),
    "Ajustado v3": (calc_peso_ajustado_v3, []),
    "Ajustado v4 (1d)": (calc_peso_ajustado_v4, [1]),
    "Ajustado v4 (3d)": (calc_peso_ajustado_v4, [3]),
    "Ajustado v4 (7d)": (calc_peso_ajustado_v4, [7]),
    "Ajustado v4 (14d)": (calc_peso_ajustado_v4, [14]),
    "Ajustado v4 (30d)": (calc_peso_ajustado_v4, [30]),
    "Ajustado v4 (365d)": (calc_peso_ajustado_v4, [365]),
}
cotejarFormulas(funciones)

exit()
# %% Tmp


def func1(**kwargs):
    func2(**kwargs)  # Desempaquetamos kwargs


def func2(**kwargs):
    print(kwargs)  # kwargs será {'días': 2}


func1(días=2)

# %% Guardar fecha de hoy en formato DD-MM-YY
from datetime import datetime

hoy = datetime.now()
print(hoy)  # 2025-02-11 15:31:51.000000
fecha_hoy_str = hoy.strftime("%d-%m-%y")
print(fecha_hoy_str)  # (11-02-25)
# pasar de string "DD-MM-YY" a datetime
fecha_obtenida = datetime.strptime("11-02-24", "%d-%m-%y")
print(fecha_obtenida)  # 2025-02-11 00:00:00
# fecha menos la fecha obtenida del string
diferencia = hoy - fecha_obtenida
print(diferencia.days)  # 0
