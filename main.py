print("PokéIA iniciando...")

from core.engine.typing import (
        multiplicador_real,
        explicar_inmunidad,
        defensas_pokemon,
        debilidades_pokemon,
        defensas_tipo_puro,
    )
from core.engine.abilities import habilidades_pokemon
from data.loaders.cargar_datos import cargar_todo 
from core.razonamiento import amenazas_por_movimientos
from core.Data.coberturas import COBERTURAS_COMUNES
from colorama import init, Fore, Style
init(autoreset=True)

    # =========================
    # CARGA DE DATOS
    # =========================
datos = cargar_todo()   
pokedex = datos["pokemon"]

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

TIPOS_EQUIVALENTES = {
        "normal": "normal",
        "fire": "fire", "fuego": "fire",
        "water": "water", "agua": "water",
        "grass": "grass", "planta": "grass",
        "electric": "electric", "eléctrico": "electric", "electrico": "electric",
        "ice": "ice", "hielo": "ice",
        "fighting": "fighting", "lucha": "fighting",
        "poison": "poison", "veneno": "poison",
        "ground": "ground", "tierra": "ground",
        "flying": "flying", "volador": "flying",
        "psychic": "psychic", "psiquico": "psychic",
        "bug": "bug", "bicho": "bug",
        "rock": "rock", "roca": "rock",
        "ghost": "ghost", "fantasma": "ghost",
        "dragon": "dragon", "dragón": "dragon",
        "dark": "dark", "siniestro": "dark",
        "steel": "steel", "acero": "steel",
        "fairy": "fairy", "hada": "fairy"
    }

print("PokéIA lista.")
print("Escribe 'ayuda' para ver los comandos disponibles.")
class C:
        RESET = "\033[0m"
        ROJO = "\033[91m"
        VERDE = "\033[92m"
        AMARILLO = "\033[93m"
        AZUL = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
        GRIS = "\033[90m"
COLORES_TIPO = {
        "fire": C.ROJO,
        "water": C.AZUL,
        "grass": C.VERDE,
        "electric": C.AMARILLO,
        "ice": C.CYAN,
        "steel": C.GRIS,
        "rock": C.GRIS,
        "ground": C.AMARILLO,
        "flying": C.CYAN,
        "psychic": C.MAGENTA,
        "dark": C.GRIS,
        "fairy": C.MAGENTA,
        "ghost": C.MAGENTA,
        "dragon": C.ROJO,
        "fighting": C.ROJO,
        "poison": C.MAGENTA,
        "bug": C.VERDE,
        "normal": C.RESET,
    }
MOVIMIENTOS_COMUNES = {
        "normal": [
            ("Body Slam", 85, 100),
            ("Return", 102, 100),
        ],
        "fire": [
            ("Flamethrower", 90, 100),
            ("Fire Blast", 110, 85),
        ],
        "water": [
            ("Surf", 90, 100),
            ("Hydro Pump", 110, 80),
        ],
        "electric": [
            ("Thunderbolt", 90, 100),
            ("Thunder", 110, 70),
        ],
        "grass": [
            ("Energy Ball", 90, 100),
            ("Leaf Storm", 130, 90),
        ],
        "ice": [
            ("Ice Beam", 90, 100),
            ("Icicle Crash", 85, 90),
        ],
        "fighting": [
            ("Close Combat", 120, 100),
            ("Drain Punch", 75, 100),
        ],
        "poison": [
            ("Sludge Bomb", 90, 100),
            ("Gunk Shot", 120, 80),
        ],
        "ground": [
            ("Earthquake", 100, 100),
            ("High Horsepower", 95, 95),
        ],
        "flying": [
            ("Brave Bird", 120, 100),
            ("Hurricane", 110, 70),
        ],
        "psychic": [
            ("Psychic", 90, 100),
            ("Psyshock", 80, 100),
        ],
        "bug": [
            ("U-turn", 70, 100),
            ("X-Scissor", 80, 100),
        ],
        "rock": [
            ("Stone Edge", 100, 80),
            ("Rock Slide", 75, 90),
        ],
        "ghost": [
            ("Shadow Ball", 80, 100),
            ("Poltergeist", 110, 90),
        ],
        "dragon": [
            ("Dragon Claw", 80, 100),
            ("Outrage", 120, 100),
            ("Draco Meteor", 130, 90),
        ],
        "dark": [
            ("Dark Pulse", 80, 100),
            ("Knock Off", 65, 100),
        ],
        "steel": [
            ("Iron Head", 80, 100),
            ("Flash Cannon", 80, 100),
        ],
        "fairy": [
            ("Moonblast", 95, 100),
            ("Play Rough", 90, 90),
        ],
    }


    # funciones
def tipo_color(nombre):
        color = COLORES_TIPO.get(nombre, C.RESET)
        return f"{color}{nombre}{C.RESET}"

def obtener_generacion(pokemon):
        poke_id = pokemon.get("id")

        if not poke_id:
            url = pokemon.get("species", {}).get("url", "")
            if url:
                try:
                    poke_id = int(url.rstrip("/").split("/")[-1])
                except ValueError:
                    poke_id = None

        if not poke_id:
            return "Desconocida"

        # 4️⃣ Determinar generación por ID real
        if poke_id <= 151:
            return "I"
        elif poke_id <= 251:
            return "II"
        elif poke_id <= 386:
            return "III"
        elif poke_id <= 493:
            return "IV"
        elif poke_id <= 649:
            return "V"
        elif poke_id <= 721:
            return "VI"
        elif poke_id <= 809:
            return "VII"
        elif poke_id <= 905:
            return "VIII"
        else:
            return "IX"

def tipos_de_movimientos(pokemon, datos_movimientos):
        tipos = set()

        for m in pokemon["moves"]:
            nombre = m["move"]["name"]
            mov = datos_movimientos.get(nombre)
            if mov: 
                tipos.add(mov["type"]["name"])

        return tipos
def normalizar_nombre(texto):
        return texto.lower().strip().replace(" ", "-")
def buscar_pokemon(nombre, pokedex):
        nombre = normalizar_nombre(nombre)

        # 1️⃣ match exacto
        if nombre in pokedex:
            return pokedex[nombre]

        # 2️⃣ match por prefijo (formas)
        for key in pokedex:
            if key.startswith(nombre + "-"):
                return pokedex[key]

        # 3️⃣ match parcial (último recurso)
        for key in pokedex:
            if nombre in key:
                return pokedex[key]

        return None
def sugerir_movimientos(tipos, max_movs=3):
        sugerencias = []

        for tipo in tipos:
            if tipo in MOVIMIENTOS_COMUNES:
                for mov in MOVIMIENTOS_COMUNES[tipo]:
                    sugerencias.append((tipo, mov))
        sugerencias.sort(
            key=lambda x: x[1][1] * (x[1][2] / 100),
            reverse=True
        )

        return sugerencias[:max_movs]

def movimientos_reales_peligrosos(pokemon_atacante, defensor, datos):
        debilidades = debilidades_pokemon(defensor, datos["tipos"])
        peligrosos = {}

        for m in pokemon_atacante["moves"]:
            nombre_mov = m["move"]["name"].lower().strip()

            mov = datos["movimientos"].get(nombre_mov)

            if not mov:
                continue

            tipo = mov["type"]["name"]
            poder = mov.get("power")
            precision = mov.get("accuracy")

            if poder is None:
                continue

            if precision is None:
                precision = 100

            if poder is None:
                continue
            mult = multiplicador_real(tipo, defensor, datos)
            tipos_atacante = [t["type"]["name"] for t in pokemon_atacante["types"]]

            if mult == 0:
                if tipo in tipos_atacante:
                    print(
                        f"🛡 {pokemon_atacante['name'].capitalize()} "
                        f"({tipo_color(tipo)}) es inmune a STAB "
                        f"{tipo_color(tipo)} contra {defensor['name'].capitalize()}"
                    )
                else:
                    print(
                        f"🛡 {defensor['name'].capitalize()} es inmune a "
                        f"{tipo_color(tipo)} de {pokemon_atacante['name'].capitalize()}"
                    )
                continue

            
            habilidades = habilidades_pokemon(defensor)
    
            
            for hab in habilidades:
                if hab in HABILIDADES_DEFENSIVAS:
                    if tipo in HABILIDADES_DEFENSIVAS[hab]:
                        mult = HABILIDADES_DEFENSIVAS[hab][tipo]

            hab = explicar_inmunidad(tipo, defensor, datos)
            if hab:
                continue

            score = poder * (precision / 100) * mult

            if nombre_mov not in peligrosos or score > peligrosos[nombre_mov][0]:
                peligrosos[nombre_mov] = (
                    score,
                    nombre_mov,
                    tipo,
                    poder,
                    precision,
                    mult
                )

        resultado = list(peligrosos.values())
        resultado.sort(key=lambda x: x[0], reverse=True)
        resultado = [x[1:] for x in resultado]
        
        return resultado[:3]




def barra_stat(valor, maximo=255, ancho=25):
        proporcion = valor / maximo
        relleno = int(proporcion * ancho)
        vacio = ancho - relleno
        return "█" * relleno + "░" * vacio


def mostrar_stats(pokemon):
        nombres = {
            "hp": "PS",
            "attack": "Ataque",
            "defense": "Defensa",
            "special-attack": "At. esp",
            "special-defense": "Def. esp",
            "speed": "Velocidad",
        }

        print(f"\n📊 Stats base de {pokemon['name'].title()}:\n")

        total = 0

        for s in pokemon["stats"]:
            nombre = s["stat"]["name"]
            valor = s["base_stat"]
            total += valor

            etiqueta = nombres.get(nombre, nombre)
            barra = barra_stat(valor)

            print(f"{etiqueta:10} {valor:3} |{barra}|")

        print(f"\nTotal: {total}")
def nombre_legible(texto):
        return texto.replace("-", " ").title()


DEBUG = False
def debug(*args):
        if DEBUG:
            print("[DEBUG]", *args)

def inmunidades_pokemon(pokemon, datos_tipos):
    defs = defensas_pokemon(pokemon, datos_tipos)
    inmunidades = {t: m for t, m in defs.items() if m == 0}
    return inmunidades

def amenaza_basica(atacante, defensor, datos):
    score = 0
    tiene_movs_con_poder = False

    tipos_atacante = [t["type"]["name"] for t in atacante["types"]]

    for mov in atacante["moves"]:
        nombre = mov["move"]["name"].lower().strip()
        datos_mov = datos["movimientos"].get(nombre)
        if not datos_mov:
            continue

        poder = datos_mov.get("power")
        if not poder:
            continue

        tiene_movs_con_poder = True
        tipo = datos_mov["type"]["name"]
        precision = datos_mov.get("accuracy") or 100
        mult = multiplicador_real(tipo, defensor, datos)

        if mult == 0:
            continue  # inmunidad real, no suma

        stab = 1.5 if tipo in tipos_atacante else 1
        score += poder * (precision / 100) * mult * stab

    # ⬇️ Fallback: si no hay movimientos cargados, usar STAB implícito
    if not tiene_movs_con_poder:
        for tipo in tipos_atacante:
            mult = multiplicador_real(tipo, defensor, datos)
        if mult > 0:
            score += 80 * mult * 1.5

    return score
TIPOS = datos["tipos"]
MOVIMIENTOS = datos["movimientos"]
POKEMON = datos["pokemon"]
    # =========================
    # LOOP PRINCIPAL
    # =========================
while True:
        entrada = input("> ").strip()
        pregunta = entrada.lower()
        
        nombre_norm = normalizar_nombre(pregunta)
        
        debug("entrada =", nombre_norm)


        if pregunta == "salir":
            print("Hasta luego 👋")
            break
        elif pregunta == "ayuda":
            print("""
        📖 Comandos disponibles

        🔎 Información de Pokémon
            Pikachu
            Charizard
            Garchomp

        📊 Estadísticas
            stats Pikachu
            stats Charizard

        ⚔️ Debilidades y resistencias
            debilidades Charizard
            resistencias Ferrothorn

        🧬 Tipos
            debilidades tipo fuego
            debilidades tipo electric

        🤝 Matchups
            match garchomp vs tyranitar
            match heatran vs ferrothorn

        🚪 Salir
            salir
            """)
            continue
            # =========================
            # MOSTRAR ESTADÍSTICAS
            # =========================
        elif pregunta.startswith("stats"):
                nombre = pregunta.replace("stats", "")
                nombre = nombre.replace("base", "")
                nombre = nombre.replace("de", "")
                nombre = nombre.strip()

                p = buscar_pokemon(nombre, pokedex)

                if not p:
                    print("No conozco ese Pokémon.")
                    continue

                mostrar_stats(p)
                continue 
            
            
            # =========================
            # DEBILIDADES DE TIPO
            # =========================
        elif pregunta.startswith("debilidades tipo "):
            tipo_input = pregunta.replace("debilidades tipo ", "").strip()

            if tipo_input not in TIPOS_EQUIVALENTES:
                print("No conozco ese tipo.")  
                continue
                
            tipo = TIPOS_EQUIVALENTES[tipo_input]
            defs = defensas_tipo_puro(tipo, datos["tipos"])

            for t, m in defs.items():
                    print(f"{t}: x{m}")
            # =========================
            # DEBILIDADES DE POKÉMON
            # =========================
        elif pregunta.startswith("debilidades "):
            nombre = normalizar_nombre( 
            pregunta.replace("debilidades ", "").strip()
            )
            p = buscar_pokemon(nombre, pokedex)

            if not p:
                print("No conozco ese Pokémon.")
                continue
            deb = debilidades_pokemon(p, datos["tipos"])

            if not deb:
                    print("No se encontraron debilidades.")
                    continue

            for t, mult in deb.items():
                    print(f"{t}: x{mult}")
        elif pregunta.startswith("resistencias "):
            nombre = normalizar_nombre( 
                pregunta.replace("resistencias ", "").strip()
            )
            p = buscar_pokemon(nombre, pokedex)

            if not p:
                print("No conozco ese Pokémon.")
                continue

            defs = defensas_pokemon(p, datos["tipos"])

            resistencias = {t: m for t, m in defs.items() if 0 < m < 1}

            if not resistencias: 
                print("No tiene resistencias relevantes.")
                continue

            print(f"Resistencias de {nombre.title()}:")
            for t, m in resistencias.items():
                print(f"  {t}: x{m}")

            # =========================
            # MATCHUP
            # =========================

        elif pregunta.startswith("match "):

            mensajes_inmunidad = []
            mensajes_cobertura = []

            texto = pregunta.replace("match ", "").strip()

            if " vs " not in texto:
                print("Usa: match pokemon1 vs pokemon2")
                continue

            a, b = texto.split(" vs ")
            a, b = a.strip(), b.strip()

            print(" a =", a, "| b =", b)

            p1 = buscar_pokemon(a, pokedex)
            p2 = buscar_pokemon(b, pokedex)

            if not p1 or not p2:
                print("No conozco uno de esos Pokémon.")
                continue

            print(f"\nAnálisis: {a.title()} vs {b.title()}")

            tipos1 = [t["type"]["name"] for t in p1["types"]]
            tipos2 = [t["type"]["name"] for t in p2["types"]]

            # =====================
            # INMUNIDADES STAB (simétrico)
            # =====================

            for tipo in tipos1:
                mult = multiplicador_real(tipo, p2, datos)
                hab = explicar_inmunidad(tipo, p2, datos)

                if mult == 0:
                    razon = f"por {hab}" if hab else "por su tipo"
                    mensajes_inmunidad.append(
                        f"🛡 {b.title()} es inmune a STAB {tipo_color(tipo)} "
                        f"de {a.title()} {razon}"
                    )

            for tipo in tipos2:
                mult = multiplicador_real(tipo, p1, datos)
                hab = explicar_inmunidad(tipo, p1, datos)

                if mult == 0:
                    razon = f"por {hab}" if hab else "por su tipo"
                    mensajes_inmunidad.append(
                        f"🛡 {a.title()} es inmune a STAB {tipo_color(tipo)} "
                        f"de {b.title()} {razon}"
                    )
            
            score_a = amenaza_basica(p1, p2, datos)
            score_b = amenaza_basica(p2, p1, datos)

            max_score = max(score_a, score_b)

            # Reemplaza el cálculo de UMBRAL_AMENAZA
            if score_a == 0 and score_b == 0:
                UMBRAL_AMENAZA = 9999
            else:
                UMBRAL_AMENAZA = 0.4 * max(score_a, score_b)  # más permisivo

            amenaza_a = score_a >= UMBRAL_AMENAZA
            amenaza_b = score_b >= UMBRAL_AMENAZA
            # =====================
            # COBERTURAS
            # =====================

            # Tipos de movimientos reales de p1
            tipos_movs_reales_p1 = set()
            for m in p1["moves"]:
                nombre_m = m["move"]["name"].lower().strip()
                mov_data = datos["movimientos"].get(nombre_m)
                if mov_data and mov_data.get("power"):
                    tipos_movs_reales_p1.add(mov_data["type"]["name"])

            for tipo_atacante in tipos1:
                for tipo_cobertura in COBERTURAS_COMUNES.get(tipo_atacante, []):
                    if tipo_cobertura not in tipos_movs_reales_p1:
                        continue
                    mult = multiplicador_real(tipo_cobertura, p2, datos)
                    if mult > 1:
                        mensajes_cobertura.append(
                            f"⚠️ {b.title()} podría estar en peligro por cobertura "
                            f"{tipo_color(tipo_cobertura)} de {a.title()} (x{mult})"
                        )  

            # =====================
            # MOVIMIENTOS REALES
            # =====================

            movs_a = movimientos_reales_peligrosos(p1, p2, datos)
            movs_b = movimientos_reales_peligrosos(p2, p1, datos)

            # =====================
            # IMPRESIÓN ORDENADA
            # =====================

            print(f"\n- {a.title()} tipos: {', '.join(tipos1)}")
            print(f"- {b.title()} tipos: {', '.join(tipos2)}")

            if mensajes_inmunidad:
                print("\n🛡 Inmunidades relevantes:")
                for m in mensajes_inmunidad:
                    print(m)

            if mensajes_cobertura:
                print("\n🎯 Coberturas a tener en cuenta:")
                for m in mensajes_cobertura:
                    print(m)

            if movs_a:
                print(f"\n⚠️ {a.title()} amenaza a {b.title()} con:")
                for nombre, tipo, poder, precision, mult in movs_a:
                    print(f" - {nombre} ({tipo_color(tipo)}) x{mult}")

            if movs_b:
                print(f"\n⚠️ {b.title()} amenaza a {a.title()} con:")
                for nombre, tipo, poder, precision, mult in movs_b:
                    print(f" - {nombre} ({tipo_color(tipo)}) x{mult}")

            print("\n⚔️ Evaluación de amenaza real:")

            if score_a == 0 and score_b == 0:
                print("❌ Ninguno tiene herramientas ofensivas fiables")
            elif score_a == 0 and score_b > 0:
                print(f"🛡 {b.title()} niega completamente a {a.title()}")
            elif score_b == 0 and score_a > 0:
                print(f"🛡 {a.title()} niega completamente a {b.title()}")
            else:
                if amenaza_b and not amenaza_a:
                    print(f"⚠️ {b.title()} es un hard counter real de {a.title()}")
                elif amenaza_a and not amenaza_b:
                    print(f"⚠️ {a.title()} es un hard counter real de {b.title()}")
                else:
                    print("⚖️ Ambos pueden amenazarse de forma relevante")
            # =====================
            # RESUMEN FINAL
            # =====================
            
            mensajes_cobertura = list(set(mensajes_cobertura))
            print("\n📊 Resumen estratégico:")

            print(
                f"{a.title()} ({', '.join(tipos1)}) vs "
                f"{b.title()} ({', '.join(tipos2)})"
            )

            if mensajes_cobertura:
                print(f"{a.title()} tiene coberturas que pueden amenazar a {b.title()}.")

            for m in mensajes_inmunidad:
                print(m)
        # =========================
        # INFO SIMPLE
        # =========================
        elif pregunta.startswith("inmunidades "):
            nombre = pregunta.replace("inmunidades ", "").strip()
            p = buscar_pokemon(nombre, pokedex)

            if not p:
                print("No conozco ese Pokémon.")
                continue

            inmunidades = inmunidades_pokemon(p, datos["tipos"])

            if not inmunidades:
                print(f"{p['name'].title()} no tiene inmunidades.")
                continue

            print(f"Inmunidades de {p['name'].title()}:")
            print(", ".join([f"{tipo_color(t)} x0" for t in inmunidades]))
            continue
        else:
                p = buscar_pokemon(pregunta, pokedex)

                if p:
                    tipos = [t["type"]["name"] for t in p["types"]]
                print(f"{nombre_norm.title()} es de tipo: {', '.join(tipos)}")

                gen = obtener_generacion(p)
                print(f"Generación de introducción: {gen}")
                
                
                habilidades = habilidades_pokemon(p)
                print("Habilidades:")
                for h in habilidades:
                    print(f" - {h.title()}")
                
                mostrar_stats(p)    
else:
    print("No entiendo el comando o Pokémon.")
