from setup_db import setup_database
from app import create_app

# Inizializza o aggiorna il database prima di avviare l'app
setup_database()

# Crea l'istanza dell'app Flask
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)