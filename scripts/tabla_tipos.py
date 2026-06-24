import json
import os

TIPOS_DIR = "tipos"

efectividad = {}

for archivo in os.listdir(TIPOS_DIR):
    with open(os.path.join(TIPOS_DIR, archivo), encoding="utf-8") as f:
        datos = json.load(f)

    tipo = datos["name"]

    efectividad[tipo] = {
        "doble": [t["name"] for t in datos["damage_relations"]["double_damage_to"]],
        "mitad": [t["name"] for t in datos["damage_relations"]["half_damage_to"]],
        "inmune": [t["name"] for t in datos["damage_relations"]["no_damage_to"]]
    }

with open("tabla_tipos.json", "w", encoding="utf-8") as f:
    json.dump(efectividad, f, indent=4, ensure_ascii=False)

print("✅ Tabla de tipos creada")
