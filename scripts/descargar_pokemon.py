import requests
import json
import os
import time

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
CARPETA = "pokemon/base"

os.makedirs(CARPETA, exist_ok=True)

total = requests.get(BASE_URL).json()["count"]
print(f"Descargando {total} Pokémon...")

for i in range(1, total + 1):
    url = f"{BASE_URL}{i}/"
    r = requests.get(url)

    if r.status_code == 200:
        datos = r.json()
        nombre = datos["name"]

        with open(f"{CARPETA}/{nombre}.json", "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        print(f"✔ {nombre}")

    time.sleep(0.1)

print("✅ Descarga completa")
