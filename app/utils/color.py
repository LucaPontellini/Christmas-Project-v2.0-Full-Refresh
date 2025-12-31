import hashlib

# Tavolozza di colori predefinita: indice determinato dall'hash dello username
COLORS = [
    "#E53935",  # red
    "#D81B60",  # pink
    "#8E24AA",  # purple
    "#5E35B1",  # deep purple
    "#3949AB",  # indigo
    "#1E88E5",  # blue
    "#039BE5",  # light blue
    "#00ACC1",  # cyan
    "#00897B",  # teal
    "#43A047",  # green
    "#7CB342",  # light green
    "#C0CA33",  # lime
    "#FDD835",  # yellow
    "#FFB300",  # amber
    "#FB8C00",  # orange
    "#F4511E",  # deep orange
    "#6D4C41",  # brown
    "#757575",  # grey
    "#546E7A",  # blue grey
]

def get_user_initial(username: str) -> str: # Restituisce l’iniziale maiuscola, oppure "?" se lo username è vuoto
    if not isinstance(username, str) or not username:
        return "?"
    return username[0].upper()

def get_user_color(username: str) -> str: # Associa uno username a un colore in modo stabile: stesso username → stesso colore.
    if not username:
        # Caso limite: nessuno username → primo colore della lista
        return COLORS[0]

    # Normalizzazione per garantire stabilità (spazi e maiuscole irrilevanti)
    normalized = username.strip().lower()

    # Hash MD5 → numero intero → modulo lunghezza lista colori
    hash_value = int(hashlib.md5(normalized.encode()).hexdigest(), 16)

    # Selezione deterministica del colore
    return COLORS[hash_value % len(COLORS)]