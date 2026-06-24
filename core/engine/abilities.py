HABILIDADES_DEFENSIVAS = {
    "levitate": {"ground": 0},
    "flash-fire": {"fire": 0},
    "water-absorb": {"water": 0},
    "volt-absorb": {"electric": 0},
    "sap-sipper": {"grass": 0},
    "storm-drain": {"water": 0},
    "dry-skin": {"water": 0},
    "motor-drive": {"electric": 0},
    "lightning-rod": {"electric": 0},
}


def habilidades_pokemon(pokemon):
    return [a["ability"]["name"] for a in pokemon["abilities"]]
    habilidades = habilidades_pokemon(defensor)

    for hab in habilidades:
        if hab in HABILIDADES_DEFENSIVAS:
            if tipo in HABILIDADES_DEFENSIVAS[hab]:
                mult = HABILIDADES_DEFENSIVAS[hab][tipo]

    return mult 
