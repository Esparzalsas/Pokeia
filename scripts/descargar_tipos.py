import requests
import json
import os

BASE_URL = "https://pokeapi.co/api/v2/type/"
CARPETA = "tipos"

os.makedirs(CARPETA, exist_ok=True)

total = requests.get(BASE_URL).json()["count"]

for i in range(1, total + 1):
    datos = requests.get(f"{BASE_URL}{i}/").json()
    nombre = datos["name"]

    with open(f"{CARPETA}/{nombre}.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f"✔ {nombre}")

print("✅ Tipos descargados")
