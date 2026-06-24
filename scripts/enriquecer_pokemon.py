import json
import os

BASE = "pokemon/base"
DESTINO = "pokemon/enriquecidos"

os.makedirs(DESTINO, exist_ok=True)

for archivo in os.listdir(BASE):
    with open(f"{BASE}/{archivo}", encoding="utf-8") as f:
        datos = json.load(f)

    pokemon = {
        "id": datos["id"],
        "nombre": datos["name"],
        "tipos": [t["type"]["name"] for t in datos["types"]],
        "stats_base": {s["stat"]["name"]: s["base_stat"] for s in datos["stats"]},
        "habilidades": {
            "normales": [],
            "oculta": None
        },
        "movimientos": [],
        "peso": datos["weight"],
        "altura": datos["height"]
    }

    for h in datos["abilities"]:
        if h["is_hidden"]:
            pokemon["habilidades"]["oculta"] = h["ability"]["name"]
        else:
            pokemon["habilidades"]["normales"].append(h["ability"]["name"])

    for m in datos["moves"]:
        pokemon["movimientos"].append(m["move"]["name"])

    with open(
        f"{DESTINO}/{datos['name']}.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(pokemon, f, indent=4, ensure_ascii=False)

    print(f"✔ {datos['name']}")

print("✅ Pokémon enriquecidos")
