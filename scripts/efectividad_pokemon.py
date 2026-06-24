import json

with open("tabla_tipos.json", encoding="utf-8") as f:
    TABLA = json.load(f)

def debilidades(tipos):
    resultado = {}

    for ataque in TABLA:
        mult = 1.0
        for t in tipos:
            if ataque in TABLA[t]["doble"]:
                mult *= 2
            elif ataque in TABLA[t]["mitad"]:
                mult *= 0.5
            elif ataque in TABLA[t]["inmune"]:
                mult *= 0

        if mult != 1:
            resultado[ataque] = mult

    return resultado

# prueba
print(debilidades(["ghost", "steel"]))
