# core/engine/typing.py
from core.engine.abilities import (
    habilidades_pokemon,
    HABILIDADES_DEFENSIVAS
)


def multiplicador_real(tipo, defensor, datos):
    mult = 1

    # ✅ Consultar inmunidades/resistencias/debilidades por tipo
    for t in defensor["types"]:
        tipo_nombre = t["type"]["name"]
        tipo_info = datos["tipos"].get(tipo_nombre)
        if not tipo_info:
            continue
        relaciones = tipo_info["damage_relations"]

        for d in relaciones["no_damage_from"]:
            if d["name"] == tipo:
                return 0  # inmunidad total, salir ya

        for d in relaciones["half_damage_from"]:
            if d["name"] == tipo:
                mult *= 0.5

        for d in relaciones["double_damage_from"]:
            if d["name"] == tipo:
                mult *= 2

    # Luego aplicar habilidades defensivas (pueden anular lo anterior)
    habilidades = habilidades_pokemon(defensor)
    for hab in habilidades:
        if hab in HABILIDADES_DEFENSIVAS:
            if tipo in HABILIDADES_DEFENSIVAS[hab]:
                mult = HABILIDADES_DEFENSIVAS[hab][tipo]

    return mult

def explicar_inmunidad(tipo, defensor, datos):
    # inmunidad por habilidad
    habilidades = habilidades_pokemon(defensor)

    for hab in habilidades:
        if hab in HABILIDADES_DEFENSIVAS:
            if tipo in HABILIDADES_DEFENSIVAS[hab]:
                return hab.title()

    # inmunidad por tipo
    mult = debilidades_pokemon(defensor, datos["tipos"]).get(tipo, 1)

    if mult == 0:
        return "tipo"

    return None

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

    # ✅ Incluir inmunidades (v == 0) además de debilidades (v > 1)
    return {k: v for k, v in debilidades.items() if v != 1}
    
