def conversar(pokedex, type_chart):
    while True:
        q = input("> ")
        if q == "salir":
            break

        if "debil" in q:
            nombre = q.split()[-1]
            pokemon = pokedex.get(nombre)
            if pokemon:
                from core.razonamiento import explicar_defensas
                print(explicar_defensas(pokemon, type_chart))
            else:
                print("No conozco ese Pokémon.")
