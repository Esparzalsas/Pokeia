import json
import os
import requests
import time

HABILIDADES_DIR = "habilidades"

for archivo in os.listdir(HABILIDADES_DIR):
    if not archivo.endswith(".json"):
        continue

    nombre_habilidad = archivo.replace(".json", "")
    ruta = os.path.join(HABILIDADES_DIR, archivo)

    with open(ruta, "r", encoding="utf-8") as f:
        datos_locales = json.load(f)

    url = f"https://pokeapi.co/api/v2/ability/{nombre_habilidad}"
    respuesta = requests.get(url)

    if respuesta.status_code != 200:
        print(f"No se pudo obtener {nombre_habilidad}")
        continue

    datos_api = respuesta.json()

    # Nombre en español
    nombre_es = next(
        (n["name"] for n in datos_api["names"] if n["language"]["name"] == "es"),
        nombre_habilidad
    )

    # Descripción en español
    descripcion = None
    for entry in datos_api["flavor_text_entries"]:
        if entry["language"]["name"] == "es":
            descripcion = entry["flavor_text"].replace("\n", " ")
            break

    # Generación de introducción
    generacion = datos_api["generation"]["name"]

    datos_locales["nombre_es"] = nombre_es
    datos_locales["descripcion"] = descripcion
    datos_locales["generacion_introduccion"] = generacion

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos_locales, f, indent=4, ensure_ascii=False)

    print(f"Enriquecida: {nombre_habilidad}")

    time.sleep(0.1)

print("\nEnriquecimiento completo ✅")

