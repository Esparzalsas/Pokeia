from core.Data.movimientos import tipos_de_movimientos
def debilidades_pokemon(pokemon, tipos_data):
    debilidades = {}

    for t in pokemon["types"]:
        tipo_nombre = t["type"]["name"]
        tipo_info = tipos_data.get(tipo_nombre)

        if not tipo_info:
            continue

        relaciones = tipo_info["damage_relations"]

        for d in relaciones["double_damage_from"]:
            nombre = d["name"]
            debilidades[nombre] = debilidades.get(nombre, 1) * 2

        for d in relaciones["half_damage_from"]:
            nombre = d["name"]
            debilidades[nombre] = debilidades.get(nombre, 1) * 0.5

        for d in relaciones["no_damage_from"]:
            nombre = d["name"]
            debilidades[nombre] = 0

    # 👉 solo devolvemos debilidades reales
    return {k: v for k, v in debilidades.items() if v > 1}
def defensas_pokemon(pokemon, tipos_data):
    defensas = {}

    for t in pokemon["types"]:
        tipo_nombre = t["type"]["name"]
        tipo_info = tipos_data.get(tipo_nombre)

        if not tipo_info:
            continue

        relaciones = tipo_info["damage_relations"]

        # Resistencias
        for d in relaciones["half_damage_from"]:
            nombre = d["name"]
            defensas[nombre] = defensas.get(nombre, 1) * 0.5

        # Inmunidades
        for d in relaciones["no_damage_from"]:
            nombre = d["name"]
            defensas[nombre] = 0

        # Debilidades (para compensar mezclas de tipos)
        for d in relaciones["double_damage_from"]:
            nombre = d["name"]
            defensas[nombre] = defensas.get(nombre, 1) * 2

    return defensas
def defensas_tipo_puro(tipo, tipos_data):
    defensas = {}

    tipo_info = tipos_data.get(tipo)
    if not tipo_info:
        return defensas

    relaciones = tipo_info["damage_relations"]

    # Debilidades
    for d in relaciones["double_damage_from"]:
        nombre = d["name"]
        defensas[nombre] = defensas.get(nombre, 1) * 2

    # Resistencias
    for d in relaciones["half_damage_from"]:
        nombre = d["name"]
        defensas[nombre] = defensas.get(nombre, 1) * 0.5

    # Inmunidades
    for d in relaciones["no_damage_from"]:
        nombre = d["name"]
        defensas[nombre] = 0

    return defensas
def amenazas_por_movimientos(defensor, atacante, datos_tipos, datos_movimientos):
    """
    Retorna lista de amenazas reales basadas en movimientos que el atacante
    puede aprender y que son super efectivos contra el defensor.
    """
    amenazas = []

    tipos_def = [t["type"]["name"] for t in defensor["types"]]
    tipos_mov = tipos_de_movimientos(atacante, datos_movimientos)

    for tipo_mov in tipos_mov:
        for tipo_def in tipos_def:
            rel = datos_tipos[tipo_def]["damage_relations"]

            if tipo_mov in [t["name"] for t in rel["double_damage_from"]]:
                amenazas.append((tipo_mov, "x2"))
            elif tipo_mov in [t["name"] for t in rel["half_damage_from"]]:
                pass
            elif tipo_mov in [t["name"] for t in rel["no_damage_from"]]:
                pass

    return list(set(amenazas))
