import random
from datetime import datetime, timedelta

def generate_pin():
    return str(random.randint(100000, 999999)) # Genera un PIN numerico a 6 cifre

def pin_expiration():
    return datetime.utcnow() + timedelta(minutes=5) # Imposta la scadenza del PIN a 5 minuti da ora (UTC)