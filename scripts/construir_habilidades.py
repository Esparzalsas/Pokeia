import json
import os

POKEMON_DIR = "pokemon"
HABILIDADES_DIR = "habilidades"

# Crear carpeta de habilidades
os.makedirs(HABILIDADES_DIR, exist_ok=True)

habilidades = {}

for archivo in os.listdir(POKEMON_DIR):
    if not archivo.endswith(".json"):
        continue

    ruta = os.path.join(POKEMON_DIR, archivo)

    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    nombre_pokemon = datos["name"]

    for habilidad in datos["abilities"]:
        nombre_habilidad = habilidad["ability"]["name"]
        es_oculta = habilidad["is_hidden"]

        if nombre_habilidad not in habilidades:
            habilidades[nombre_habilidad] = {
                "pokemon": []
            }

        habilidades[nombre_habilidad]["pokemon"].append({
            "nombre": nombre_pokemon,
            "oculta": es_oculta
        })

# Guardar cada habilidad en su propio archivo
for nombre, info in habilidades.items():
    ruta = os.path.join(HABILIDADES_DIR, f"{nombre}.json")

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4, ensure_ascii=False)

print(f"Se generaron {len(habilidades)} habilidades ✅")
