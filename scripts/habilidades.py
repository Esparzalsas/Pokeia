import requests

pokemon = input("Escribe el nombre de un Pokémon: ").lower()
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()

    print(f"\nHabilidades de {pokemon.capitalize()}:\n")

    for habilidad in datos["abilities"]:
        nombre = habilidad["ability"]["name"]
        es_oculta = habilidad["is_hidden"]

        if es_oculta:
            print(f"- {nombre} (Habilidad Oculta)")
        else:
            print(f"- {nombre}")
else:
    print("No se encontró ese Pokémon 😢")
