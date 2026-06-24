import json
import os

BASE = "movimientos/base"
DESTINO = "movimientos/enriquecidos"

os.makedirs(DESTINO, exist_ok=True)

def texto_es(lista, clave="name"):
    for item in lista:
        if item["language"]["name"] == "es":
            return item.get(clave)
    return None

for archivo in os.listdir(BASE):
    ruta = os.path.join(BASE, archivo)

    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)

    movimiento = {
        "id": datos["id"],
        "nombre_en": datos["name"],
        "nombre_es": texto_es(datos["names"]),
        "tipo": datos["type"]["name"],
        "categoria": datos["damage_class"]["name"],
        "potencia": datos["power"],
        "precision": datos["accuracy"],
        "pp": datos["pp"],
        "prioridad": datos["priority"],
        "generacion": datos["generation"]["name"],
        "efecto": None,
        "pokemon_que_lo_aprenden": []
    }

    # Efecto en español
    for efecto in datos["effect_entries"]:
        if efecto["language"]["name"] == "es":
            movimiento["efecto"] = efecto["effect"]
            break

    # Pokémon que lo aprenden
    for p in datos["learned_by_pokemon"]:
        movimiento["pokemon_que_lo_aprenden"].append(p["name"])

    with open(
        os.path.join(DESTINO, f"{datos['name']}.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(movimiento, f, indent=4, ensure_ascii=False)

    print(f"✔ {datos['name']}")

print("✅ Movimientos enriquecidos correctamente")
