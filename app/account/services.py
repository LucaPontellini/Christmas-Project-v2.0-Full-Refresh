from app.account.repository import delete_pins_for_user, save_reset_pin
from app.utils.security import generate_pin, pin_expiration

def create_reset_pin(user_id: int) -> str:
    # Rimuove eventuali PIN di reset precedenti per garantire unicità
    delete_pins_for_user(user_id)

    # Genera un nuovo PIN sicuro
    pin = generate_pin()

    # Calcola la scadenza del PIN
    expires_at = pin_expiration()

    # Registra il nuovo PIN nel sistema con la relativa scadenza
    save_reset_pin(user_id, pin, expires_at)

    # Restituisce il PIN per l’invio all’utente
    return pin