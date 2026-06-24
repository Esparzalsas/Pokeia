import json
import os

POKEMON_DIR = "pokemon/enriquecidos"

def pokemon_con_habilidad(nombre_habilidad):
    resultados = []

    for archivo in os.listdir(POKEMON_DIR):
        with open(os.path.join(POKEMON_DIR, archivo), encoding="utf-8") as f:
            p = json.load(f)

        if (
            nombre_habilidad == p["habilidades"]["oculta"]
            or nombre_habilidad in p["habilidades"]["normales"]
        ):
            resultados.append(p["nombre"])

    return resultados


habilidad = input("Escribe una habilidad (en inglés, por ahora): ").lower()

usuarios = pokemon_con_habilidad(habilidad)

print(f"\nPokémon con la habilidad '{habilidad}':\n")
for p in usuarios:
    print("-", p)
