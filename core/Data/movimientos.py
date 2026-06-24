# core/movimientos.py

def tipos_de_movimientos(pokemon, datos_movimientos):
    """
    Retorna un set de tipos de movimientos que el Pokémon puede aprender
    según los datos de movimientos cargados desde JSON.
    """
    tipos = set()

    nombre = pokemon["name"].lower()

    for mov in datos_movimientos.values():
        aprendible = mov.get("learned_by_pokemon", [])
        if nombre in aprendible:
            tipo = mov["type"]["name"]
            tipos.add(tipo)

    return tipos
