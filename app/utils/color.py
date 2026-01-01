import hashlib

# Tavolozza di colori predefinita. L'indice viene determinato tramite hash dello username, così lo stesso username avrà sempre lo stesso colore.
COLORS = [
    "#E53935",  # rosso
    "#D81B60",  # rosa
    "#8E24AA",  # viola
    "#5E35B1",  # viola scruro
    "#3949AB",  # indaco
    "#1E88E5",  # blu
    "#039BE5",  # azzurro
    "#00ACC1",  # ciano
    "#00897B",  # verde smeraldo
    "#43A047",  # verde
    "#7CB342",  # verde chiaro
    "#C0CA33",  # limetta / lima / giallo verde
    "#FDD835",  # giallo
    "#FFB300",  # ambra
    "#FB8C00",  # arancione
    "#F4511E",  # arancione scuro
    "#6D4C41",  # marrone
    "#757575",  # grigio
    "#546E7A",  # blu grigio
]

def get_user_initial(username: str) -> str: # Restituisce l’iniziale maiuscola dello username. Se lo username è vuoto o non valido, ritorna "?".

    if not isinstance(username, str) or not username:
        return "?"
    return username[0].upper()


def get_user_color(username: str) -> str: # Associa uno username a un colore in modo deterministico:

    # - Stesso username --> stesso colore.
    # - Username vuoto --> primo colore della lista.
    # - Normalizzazione: spazi e maiuscole non influenzano il risultato.

    if not username: # Caso limite: nessuno username --> colore di default
        return COLORS[0]

    normalized = username.strip().lower() # Normalizza lo username per garantire stabilità dell'hash
    hash_value = int(hashlib.md5(normalized.encode()).hexdigest(), 16) # Calcola hash MD5 --> converte in intero --> riduce modulo numero colori
    return COLORS[hash_value % len(COLORS)] # Seleziona un colore in modo deterministico