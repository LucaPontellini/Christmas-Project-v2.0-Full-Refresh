import random
from datetime import datetime, timedelta

def generate_pin():
    # Genera un PIN numerico a 6 cifre
    return str(random.randint(100000, 999999))

def pin_expiration():
    # Imposta la scadenza del PIN a 5 minuti da ora (UTC)
    return datetime.utcnow() + timedelta(minutes=5)