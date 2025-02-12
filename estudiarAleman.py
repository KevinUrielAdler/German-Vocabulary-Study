import os
import csv
import random

from colorama import Fore

from config import OPENAI_API_KEY

RUTA_VOCABULARIO = "Vocabulario/"
GENEROS = {
    "e": "die ",
    "r": "der ",
    "s": "das ",
    "-": "",
}
COLORES = {
    "die ": Fore.MAGENTA,
    "der ": Fore.CYAN,
    "das ": Fore.WHITE,
}
RESET = Fore.RESET
ACIERTO = Fore.GREEN
ERROR = Fore.RED


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def colorear(strings, colores):
    if isinstance(strings, str):
        return f"{colores}{strings}{RESET}"

    strings_res = []

    for string, color in zip(strings, colores):
        strings_res.append(f"{color}{string}{RESET}")

    return strings_res


def esIgual(elemento1, elemento2):
    if elemento1["Beschreibung"] != elemento2["Beschreibung"]:
        return False

    significados1 = [s.strip() for s in elemento1["Übersetzung"].split("/")]
    significados2 = [s.strip() for s in elemento2["Übersetzung"].split("/")]

    for s1 in significados1:
        for s2 in significados2:
            if s1 == s2:
                return True

    return False


def calcular_peso(aciertos, veces_presentado):
    if veces_presentado == 0:
        return 1

    peso = (
        (
            veces_presentado**2 * (veces_presentado - aciertos) +
            aciertos
        )
        /
        (veces_presentado**2 * (1 + veces_presentado))
    )

    return peso


def elegirOpcion(archivo, columna_conteo):
    datos = []

    with open(RUTA_VOCABULARIO + archivo, mode='r', encoding="utf-8") as archivo:
        lector_csv = csv.DictReader(archivo)
        datos = list(lector_csv)

    opciones = []
    pesos = []

    for i, dato in enumerate(datos):
        conteo = dato[columna_conteo].split("/")
        opciones.append(i)
        pesos.append(calcular_peso(int(conteo[0]), int(conteo[1])))

    indice = random.choices(opciones, weights=pesos)[0]

    return indice, datos, lector_csv.fieldnames


def explicarRespuestaIncorrecta(asistente, mensajes, prompt_asistente, mensaje_asistente, mensaje_usuario):
    explicacion = input(
        "¿Desea una explicación detallada de por qué su respuesta es incorrecta? (s/n): "
    )

    if explicacion == "s":
        mensajes[0].content = prompt_asistente
        mensajes[1].content = mensaje_asistente
        mensajes[2].content = mensaje_usuario
        print()
        respuesta = asistente.stream_chat(mensajes)

        for r in respuesta:
            print(r.delta, end="")

        print()


def guardarDatos(datos, nombre_archivo, fieldnames):
    with open(RUTA_VOCABULARIO + nombre_archivo, mode='w', encoding="utf-8", newline='') as archivo:
        escritor_csv = csv.DictWriter(
            archivo,
            fieldnames=fieldnames
        )
        escritor_csv.writeheader()

        for fila in datos:
            escritor_csv.writerow(fila)


def estudiarConjVerbos(*_, infinitas_veces=True):
    resp_correcta = True
    ejecuciones = 0
    fieldnames = []
    indice = 0

    while infinitas_veces or ejecuciones == 0:
        print("Conjugación de verbos en alemán\n")

        if resp_correcta:
            indice, verbos, fieldnames = elegirOpcion(
                archivo="Verbos.csv",
                columna_conteo="Treffer Konjugations"
            )

        conteo = verbos[indice]["Treffer Konjugations"].split("/")
        conteo = [int(c) for c in conteo]
        verbo = verbos[indice]
        infinitivo = verbo["Infinitiv"]
        respuesta_presente = input(
            f"Conjuga el verbo en presente para '{infinitivo}': ").strip()
        respuesta_participio = input(
            f"Indica el Partizip II para '{infinitivo}': ").strip()
        respuesta_preterito = input(
            f"Indica el Präteritum para '{infinitivo}': ").strip()
        respuesta_konjunktiv = input(
            f"Indica el Konjunktiv II para '{infinitivo}': ").strip()
        resp_correcta = (
            respuesta_presente == verbo["Präsens"] and
            respuesta_participio == verbo["Partizip II"] and
            respuesta_preterito == verbo["Präteritum"] and
            respuesta_konjunktiv == verbo["Konjunktiv II"]
        )

        if resp_correcta:
            conteo[0] += 1
            ejecuciones += 1
            print(f"\n{colorear('¡Correcto!', ACIERTO)}\n")

        else:
            print(f"\n{colorear('Incorrecto.', ERROR)} Respuesta correcta:")
            print(f"Presente: {verbo['Präsens']}")
            print(f"Partizip II: {verbo['Partizip II']}")
            print(f"Präteritum: {verbo['Präteritum']}")
            print(f"Konjunktiv II: {verbo['Konjunktiv II']}\n")

        print(
            f"- Traducción: {verbo['Übersetzung']}\n" +
            (
                f"- Descripción: {verbo['Beschreibung']}\n"
                if verbo["Beschreibung"] != "-" else ""
            )
        )

        conteo[1] += 1
        verbos[indice]["Treffer Konjugations"] = f"{conteo[0]}/{conteo[1]}"
        guardarDatos(verbos, "Verbos.csv", fieldnames)
        salir = input("¿Salir? (s/n): ")

        if salir.lower() == 's':
            print("¡Hasta luego!")
            exit(0)

        os.system("cls")


def estudiarVerbosEspanol(asistente, mensajes, infinitas_veces=True):
    prompt_asistente = """
Eres un asistente de estudio de verbos en alemán.
La traducción siempre será incorrecta.
Tu función es aclarar la razón por la que la traducción de un verbo del alemán al español es incorrecta.
Por favor, explica brevemente por qué la respuesta incorrecta es incorrecta y por qué la respuesta correcta es correcta.
"""
    resp_correcta = True
    ejecuciones = 0
    fieldnames = []
    indice = 0

    while infinitas_veces or ejecuciones == 0:
        print("Traducción de verbos al español\n")

        if resp_correcta:
            indice, verbos, fieldnames = elegirOpcion(
                archivo="Verbos.csv",
                columna_conteo="Treffer Spanisch"
            )

        conteo = verbos[indice]["Treffer Spanisch"].split("/")
        conteo = [int(c) for c in conteo]
        verbo = verbos[indice]
        respuestas = [v.strip() for v in verbo["Übersetzung"].split("/")]

        for respuesta in respuestas:
            if '(' in respuesta:
                respuestas.remove(respuesta)
                respuestas.append(respuesta.replace("(", "").replace(")", ""))

        instruccion = f"Traduce '{verbo['Infinitiv']}' al español: "
        respuesta = input(instruccion).strip()
        resp_correcta = respuesta in respuestas

        if resp_correcta:
            conteo[0] += 1
            ejecuciones += 1
            print(
                f"\n{colorear('¡Correcto!', ACIERTO)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n" +
                (
                    f"- Descripción: ({verbo['Beschreibung']})\n"
                    if verbo["Beschreibung"] != "-" else ""
                )
            )

        else:
            msg_asistente = f"Verbo original en alemán: \
'{verbo['Infinitiv']}'."
            msg_usuario = f"Respuesta incorrecta: {respuesta}. "

            if len(respuestas) == 1:
                msg_correcta = f"Respuesta correcta: {respuestas[0]}"
            else:
                msg_correcta = f"Respuestas válidas: {', '.join(respuestas)}"

            msg_usuario += msg_correcta
            print(
                f"\n{colorear('Incorrecto.', ERROR)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n" +
                (
                    f"- Descripción: ({verbo['Beschreibung']})\n"
                    if verbo["Beschreibung"] != "-" else ""
                )
            )

            if asistente:
                explicarRespuestaIncorrecta(
                    asistente, mensajes, prompt_asistente,
                    msg_asistente, msg_usuario
                )

        conteo[1] += 1
        verbos[indice]["Treffer Spanisch"] = f"{conteo[0]}/{conteo[1]}"
        guardarDatos(verbos, "Verbos.csv", fieldnames)
        salir = input("¿Salir? (s/n): ")

        if salir.lower() == 's':
            print("¡Hasta luego!")
            exit(0)

        os.system("cls")


def estudiarVerbosAleman(asistente, mensajes, infinitas_veces=True):
    prompt_asistente = """
Eres un asistente de estudio de verbos en alemán.
La traducción siempre será incorrecta.
Tu función es aclarar la razón por la que la traducción de un verbo al alemán es incorrecta.
Por favor, explica brevemente por qué la respuesta incorrecta es incorrecta y por qué la respuesta correcta es correcta.
"""
    resp_correcta = True
    ejecuciones = 0
    fieldnames = []
    indice = 0

    while infinitas_veces or ejecuciones == 0:
        print("Traducción de verbos al alemán\n")

        if resp_correcta:
            indice, verbos, fieldnames = elegirOpcion(
                archivo="Verbos.csv",
                columna_conteo="Treffer Deutsch"
            )

        conteo = verbos[indice]["Treffer Deutsch"].split("/")
        conteo = [int(c) for c in conteo]
        verbo = verbos[indice]
        instruccion = f"Traduce '{verbo['Übersetzung']}' "
        instruccion += f"\
({verbo['Beschreibung']}) " if verbo["Beschreibung"] != "-" else ""
        instruccion += "al alemán: "
        respuesta = input(instruccion).strip()
        respuestas = []

        for v in verbos:
            if esIgual(v, verbo):
                if '(' not in v["Infinitiv"]:
                    respuestas.append(v["Infinitiv"])
                else:
                    respuestas.append(
                        v["Infinitiv"].replace("(", "").replace(")", "")
                    )

        resp_correcta = respuesta in respuestas

        if resp_correcta:
            conteo[0] += 1
            ejecuciones += 1
            print(
                f"\n{colorear('¡Correcto!', ACIERTO)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n"
            )

        else:
            msg_asistente = f"Verbo original en alemán: \
    '{verbo['Übersetzung']}'."
            msg_asistente += f" descripción: \
    {verbo['Beschreibung']}." if verbo["Beschreibung"] != "-" else ""
            msg_usuario = f"Respuesta incorrecta: {respuesta}. "

            if len(respuestas) == 1:
                msg_correcta = f"Respuesta correcta: {respuestas[0]}"
            else:
                msg_correcta = f"Respuestas válidas: {', '.join(respuestas)}"

            msg_usuario += msg_correcta
            print(
                f"\n{colorear('Incorrecto.', ERROR)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n"
            )

            if asistente:
                explicarRespuestaIncorrecta(
                    asistente, mensajes, prompt_asistente,
                    msg_asistente, msg_usuario
                )

        conteo[1] += 1
        verbos[indice]["Treffer Deutsch"] = f"{conteo[0]}/{conteo[1]}"
        guardarDatos(verbos, "Verbos.csv", fieldnames)
        salir = input("¿Salir? (s/n): ")

        if salir.lower() == 's':
            print("¡Hasta luego!")
            exit(0)

        os.system("cls")


def estudiarSustantivosEspanol(asistente, mensajes, infinitas_veces=True):
    prompt_asistente = """
Eres un asistente de estudio de sustantivos en alemán.
La traducción siempre será incorrecta.
Tu función es aclarar la razón por la que la traducción de un sustantivo del alemán al español es incorrecta.
Por favor, explica brevemente por qué la respuesta incorrecta es incorrecta y por qué la respuesta correcta es correcta.
"""
    resp_correcta = True
    ejecuciones = 0
    fieldnames = []
    indice = 0
    genero_s = "der "

    while infinitas_veces or ejecuciones == 0:
        print("Traducción de sustantivos al español\n")

        if resp_correcta:
            indice, sustantivos, fieldnames = elegirOpcion(
                archivo="Sustantivos.csv",
                columna_conteo="Treffer Spanisch"
            )
            genero_s = random.choice(["der ", "die "])

        conteo = sustantivos[indice]["Treffer Spanisch"].split("/")
        conteo = [int(c) for c in conteo]
        sustantivo = sustantivos[indice]
        genero = GENEROS[sustantivo["Genus"]]
        respuestas = [s.strip() for s in sustantivo["Übersetzung"].split("/")]

        if genero:
            sustantivo_aleman = f"{genero}{sustantivo['Wort']}"
        else:
            genero = genero_s

            if genero_s == "der ":
                sustantivo_aleman = f"{genero_s}{sustantivo['Wort']}"
            else:
                sustantivo_aleman = f"{genero_s}{sustantivo['Femeninum']}"

            for resp in respuestas:
                if "(a)" in resp:
                    resp_base = resp.replace("(a)", "").strip()
                    respuestas.remove(resp)

                    if genero_s == "der ":
                        respuestas.append(resp_base)
                    else:
                        if resp_base[-1] == "o" or resp_base[-1] == "e":
                            respuestas.append(resp_base[:-1] + "a")
                        else:
                            respuestas.append(resp_base + "a")

        instruccion = f"Traduce '{
            colorear(sustantivo_aleman, COLORES[genero])
        }' al español: "
        respuesta = input(instruccion).strip()
        resp_correcta = respuesta in respuestas

        if resp_correcta:
            conteo[0] += 1
            ejecuciones += 1
            print(
                f"\n{colorear('¡Correcto!', ACIERTO)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n" +
                (
                    f"- Descripción: ({sustantivo['Beschreibung']})\n"
                    if sustantivo["Beschreibung"] != "-" else ""
                )
            )

        else:
            msg_asistente = f"Sustantivo original en alemán: \
'{sustantivo['Wort']}'."
            msg_usuario = f"Respuesta incorrecta: {respuesta}. "

            if len(respuestas) == 1:
                msg_correcta = f"Respuesta correcta: {respuestas[0]}"
            else:
                msg_correcta = f"Respuestas válidas: {', '.join(respuestas)}"

            msg_usuario += msg_correcta
            print(
                f"\n{colorear('Incorrecto.', ERROR)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n" +
                (
                    f"- Descripción: ({sustantivo['Beschreibung']})\n"
                    if sustantivo["Beschreibung"] != "-" else ""
                )
            )

            if asistente:
                explicarRespuestaIncorrecta(
                    asistente, mensajes, prompt_asistente,
                    msg_asistente, msg_usuario
                )

        conteo[1] += 1
        sustantivos[indice]["Treffer Spanisch"] = f"{conteo[0]}/{conteo[1]}"
        guardarDatos(sustantivos, "Sustantivos.csv", fieldnames)
        salir = input("¿Salir? (s/n): ")

        if salir.lower() == 's':
            print("¡Hasta luego!")
            exit(0)

        os.system("cls")


def estudiarSustantivosAleman(asistente, mensajes, infinitas_veces=True):
    prompt_asistente = """
Eres un asistente de estudio de sustantivos en alemán.
La traducción siempre será incorrecta.
Tu función es aclarar la razón por la que la traducción de un sustantivo al alemán es incorrecta.
Por favor, explica brevemente por qué la respuesta incorrecta es incorrecta y por qué la respuesta correcta es correcta.
"""
    resp_correcta = True
    ejecuciones = 0
    fieldnames = []
    indice = 0

    while infinitas_veces or ejecuciones == 0:
        print("Traducción de sustantivos al alemán\n")

        if resp_correcta:
            indice, sustantivos, fieldnames = elegirOpcion(
                archivo="Sustantivos.csv",
                columna_conteo="Treffer Deutsch"
            )

        conteo = sustantivos[indice]["Treffer Deutsch"].split("/")
        conteo = [int(c) for c in conteo]
        sustantivo = sustantivos[indice]
        instruccion = f"Traduce '{sustantivo['Übersetzung']}' "
        instruccion += f"\
({sustantivo['Beschreibung']}) " if sustantivo["Beschreibung"] != "-" else ""
        instruccion += "al alemán: "
        respuesta = input(instruccion).strip()
        respuestas = []
        colores = []

        for s in sustantivos:
            if esIgual(s, sustantivo):
                if s["Femeninum"] != "-":
                    respuestas.append(f"der {s['Wort']}")
                    respuestas.append(f"die {s['Femeninum']}")
                    colores.append(COLORES["der "])
                    colores.append(COLORES["die "])

                else:
                    genero_s = GENEROS[s['Genus']]
                    respuestas.append(f"{genero_s}{s['Wort']}")
                    colores.append(COLORES[genero_s])

        resp_correcta = respuesta in respuestas

        if resp_correcta:
            conteo[0] += 1
            ejecuciones += 1
            print(
                f"\n{colorear('¡Correcto!', ACIERTO)}\n- Respuestas válidas: " +
                ", ".join(colorear(respuestas, colores)) + "\n"
            )

        else:
            msg_asistente = f"Sustantivo original en español: \
'{sustantivo['Übersetzung']}'."
            msg_asistente += f" descripción: \
{sustantivo['Beschreibung']}." if sustantivo["Beschreibung"] != "-" else ""
            msg_usuario = f"Respuesta incorrecta: {respuesta}. "

            if len(respuestas) == 1:
                msg_correcta = f"Respuesta correcta: {respuestas[0]}"
            else:
                msg_correcta = f"Respuestas válidas: {', '.join(respuestas)}"

            msg_usuario += msg_correcta
            print(
                f"\n{colorear('Incorrecto.', ERROR)}\n- Respuestas válidas: " +
                ", ".join(colorear(respuestas, colores)) + "\n"
            )

            if asistente:
                explicarRespuestaIncorrecta(
                    asistente, mensajes, prompt_asistente,
                    msg_asistente, msg_usuario
                )

        conteo[1] += 1
        sustantivos[indice]["Treffer Deutsch"] = f"{conteo[0]}/{conteo[1]}"
        guardarDatos(sustantivos, "Sustantivos.csv", fieldnames)
        salir = input("¿Salir? (s/n): ")

        if salir.lower() == 's':
            print("¡Hasta luego!")
            exit(0)

        os.system("cls")


def estudiarAdjetivosAleman(asistente, mensajes, infinitas_veces=True):
    prompt_asistente = """
Eres un asistente de estudio de adjetivos en alemán.
La traducción siempre será incorrecta.
Tu función es aclarar la razón por la que la traducción de un adjetivo al alemán es incorrecta.
Por favor, explica brevemente por qué la respuesta incorrecta es incorrecta y por qué la respuesta correcta es correcta.
"""
    resp_correcta = True
    ejecuciones = 0
    fieldnames = []
    indice = 0

    while infinitas_veces or ejecuciones == 0:
        print("Traducción de adjetivos al alemán\n")

        if resp_correcta:
            indice, adjetivos, fieldnames = elegirOpcion(
                archivo="Adjetivos.csv",
                columna_conteo="Treffer Deutsch"
            )

        conteo = adjetivos[indice]["Treffer Deutsch"].split("/")
        conteo = [int(c) for c in conteo]
        adjetivo = adjetivos[indice]
        instruccion = f"Traduce '{adjetivo['Übersetzung']}' "
        instruccion += f"\
({adjetivo['Beschreibung']}) " if adjetivo["Beschreibung"] != "-" else ""
        instruccion += "al alemán: "
        respuesta = input(instruccion).strip()
        respuestas = []

        for a in adjetivos:
            if esIgual(a, adjetivo):
                respuestas.append(a["Adjektiv"])

        resp_correcta = respuesta in respuestas

        if resp_correcta:
            conteo[0] += 1
            ejecuciones += 1
            print(
                f"\n{colorear('¡Correcto!', ACIERTO)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n"
            )

        else:
            msg_asistente = f"Sustantivo original en español: \
'{adjetivo['Übersetzung']}'."
            msg_asistente += f" descripción: \
{adjetivo['Beschreibung']}." if adjetivo["Beschreibung"] != "-" else ""
            msg_usuario = f"Respuesta incorrecta: {respuesta}. "

            if len(respuestas) == 1:
                msg_correcta = f"Respuesta correcta: {respuestas[0]}"
            else:
                msg_correcta = f"Respuestas válidas: {', '.join(respuestas)}"

            msg_usuario += msg_correcta
            print(
                f"\n{colorear('Incorrecto.', ERROR)}\n- Respuestas válidas: " +
                ", ".join(respuestas) + "\n"
            )

            if asistente:
                explicarRespuestaIncorrecta(
                    asistente, mensajes, prompt_asistente,
                    msg_asistente, msg_usuario
                )

        conteo[1] += 1
        adjetivos[indice]["Treffer Deutsch"] = f"{conteo[0]}/{conteo[1]}"
        guardarDatos(adjetivos, "Adjetivos.csv", fieldnames)
        salir = input("¿Salir? (s/n): ")

        if salir.lower() == 's':
            print("¡Hasta luego!")
            exit(0)

        os.system("cls")


def main():
    try:
        from llama_index.llms.openai import OpenAI
        from llama_index.core.llms import ChatMessage

        asistente = OpenAI(model="gpt-4o-mini", temperature=0.1,
                           max_tokens=128, response_format="text")
        mensajes = [
            ChatMessage(role="system"),
            ChatMessage(role="assistant"),
            ChatMessage(role="user"),
        ]

        asistente = None
    except:
        print("No se puede acceder a GPT\n\n")
        asistente = None

    print("""
¡Bienvenido al programa de estudio de verbos en alemán!
¿Qué deseas hacer?
1. Estudiar las conjugaciones de los verbos en alemán.
2. Estudiar la traducción de verbos al español.
3. Estudiar la traducción de verbos al alemán.
4. Estudiar la traducción de sustantivos al español.
5. Estudiar la traducción de sustantivos al alemán.
6. Estudiar la traducción de adjetivos al alemán.
7. Estudiar selección.
8. Salir.
          """)
    funciones = {
        "1": estudiarConjVerbos,
        "2": estudiarVerbosEspanol,
        "3": estudiarVerbosAleman,
        "4": estudiarSustantivosEspanol,
        "5": estudiarSustantivosAleman,
        "6": estudiarAdjetivosAleman
    }
    pesos_funciones = {
        "1": 0.15,
        "2": 0.5,
        "3": 1,
        "4": 0.5,
        "5": 1,
        "6": 1
    }
    opcion = input("Opción: ")

    if opcion != "7" and opcion != "8":
        os.system("cls")
        funciones[opcion](asistente, mensajes)

    elif opcion == "7":
        opciones = []
        pesos_opciones = []
        opciones_in = input("Ingrese las opciones de práctica: ")
        opciones_in = opciones_in.strip().split()

        for opcion in opciones_in:
            if opcion in funciones.keys():
                opciones.append(funciones[opcion])
                pesos_opciones.append(pesos_funciones[opcion])

        while True:
            os.system("cls")
            funcion = random.choices(opciones, weights=pesos_opciones)[0]
            funcion(asistente, mensajes, infinitas_veces=False)

    elif opcion == "8":
        print("¡Hasta luego!")
        exit(0)

    print("¡Hasta luego!")


if __name__ == "__main__":
    main()
