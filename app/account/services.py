from app.account.repository import delete_pins_for_user, save_reset_pin
from app.utils.security import generate_pin, pin_expiration

def create_reset_pin(user_id: int) -> str:
    delete_pins_for_user(user_id)
    pin = generate_pin()
    expires_at = pin_expiration()
    save_reset_pin(user_id, pin, expires_at)
    return pin