# 🧠 PokéIA

PokéIA es un asistente en consola hecho en Python que permite analizar Pokémon, tipos y enfrentamientos usando lógica simple de combate basada en tipos, habilidades, STAB y cobertura de movimientos.

---

## ⚠️ Estado del proyecto

Proyecto personal en desarrollo. La lógica puede cambiar con el tiempo. No he probado todas las combinaciones así que no puedo garantizar que no tenga ningún error, si encuentras alguno por favor informa.


## ▶️ Ejecución

Abre una terminal dentro de la carpeta del proyecto y ejecuta:

```bash
python main.py
```

o

```bash
py main.py
```

Una vez iniciado, escribe `ayuda` para ver los comandos disponibles.

## QUÉ HACE❓❓

Analiza efectividad de tipos, maneja la tabla de efectividades y analiza enfrentamientos entre dos Pokémon teniendo en cuenta habilidades, STAB, tipos y coberturas.

### Ejemplo

![Ejemplo de análisis](https://github.com/user-attachments/assets/3da0d8f9-8856-441b-ad0b-fec221cd1545)


## ❌ Limitaciones actuales

Los análisis de enfrentamientos no consideran:

- EVs
- IVs
- Naturalezas
- Objetos equipados
- Clima
- Cambios de estadísticas
- Potenciadores de habilidad (Solar Power, Huge Power, etc.)
- Valores reales de Ataque, Defensa, Ataque Especial, Defensa Especial y Velocidad
    
## 🚀 Requisitos

- Python 3.10+
- Dependencias:
```bash
pip install colorama
