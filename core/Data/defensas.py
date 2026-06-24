def analizar_defensas(pokemon, type_chart):
    tipos = pokemon["types"]
    resultado = {}

    for tipo_ataque, tabla in type_chart.items():
        mult = 1.0
        for tipo_def in tipos:
            mult *= tabla.get(tipo_def, 1.0)

        if mult != 1.0:
            resultado[tipo_ataque] = mult

    return resultado
def defensas_tipo_puro(tipo, tabla_tipos):
    multiplicadores = {}

    for atacante, info in tabla_tipos.items():
        mult = info["efectividades"].get(tipo, 1)
        multiplicadores[atacante] = mult

    return multiplicadores
