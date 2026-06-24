import os
import json

def cargar_todo():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    POKEMON_PATH = os.path.join(BASE_DIR, "data", "raw", "pokemon")
    HABILIDADES_PATH = os.path.join(BASE_DIR, "data", "raw", "habilidades")
    MOVIMIENTOS_PATH = os.path.join(BASE_DIR, "data", "raw", "movimientos")
    TIPOS_PATH = os.path.join(BASE_DIR, "data", "raw", "tipos")

    return {
        "pokemon": cargar_carpeta(POKEMON_PATH),
        "habilidades": cargar_carpeta(HABILIDADES_PATH),
        "movimientos": cargar_carpeta(MOVIMIENTOS_PATH),
        "tipos": cargar_carpeta(TIPOS_PATH),
    }


def cargar_carpeta(ruta):
    data = {}

    for archivo in os.listdir(ruta):
        if archivo.endswith(".json"):
            with open(os.path.join(ruta, archivo), encoding="utf-8") as f:
                obj = json.load(f)

                if "name" not in obj:
                    continue

                data[obj["name"]] = obj

    return data
