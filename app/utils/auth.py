from functools import wraps
from flask import session, redirect, url_for, abort

# Se non c'è un 'user_id' nella sessione, l'utente viene reindirizzato alla pagina di login.
def login_required(f):
    @wraps(f)  # Mantiene nome e metadata della funzione originale
    def decorated(*args, **kwargs): # Controlla se l'utente è loggato
        
        if "user_id" not in session:
            return redirect(url_for("casino.lobby", open="login")) # Reindirizza alla lobby del casino con popup di login
        
        return f(*args, **kwargs) # Se l'utente è autenticato, esegue la funzione originale
    return decorated

# Controlla che nella sessione sia presente il ruolo 'admin'.
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        if session.get("role") != "admin": # Verifica che il ruolo dell'utente sia 'admin'
            abort(403) # Se non è admin, restituisce errore HTTP 403 (Accesso negato)
        
        return f(*args, **kwargs) # Se è admin, esegue la funzione originale
    return decorated



# ------------------------------------------------------------------------------------------------------------------------------------------
# Cosa sono i " @wraps(f) " --> spiegazione sottostante e breve (sono decoratori)

# Un decoratore in Python è una funzione che "avvolge" un'altra funzione per modificarne il comportamento senza cambiarne il codice interno.

# Esempio di sintassi con decoratori:
#   @decoratore
#   def funzione():
#       ...

# La funzione viene passata attraverso il decoratore, che può eseguire codice PRIMA e/o DOPO la funzione originale.

# Questo è utilissimo per:
#   - evitare codice duplicato
#   - aggiungere controlli (login, permessi, logging…)
#   - mantenere le route pulite e leggibili

# In questo caso, i decoratori servono per proteggere le route controllando autenticazione e permessi.

# Link consultati:

# - https://www.geeksforgeeks.org/python/python-decorators-a-complete-guide
# - https://realpython.com/primer-on-python-decorators
# - https://www.freecodecamp.org/news/decorators-in-python-tutorial
# - https://www.programiz.com/python-programming/decorator
# ------------------------------------------------------------------------------------------------------------------------------------------