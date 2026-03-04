from dotenv import load_dotenv
from setup_db import setup_database
from app import create_app

# Carica le variabili dal file .env
load_dotenv()

# Inizializza o aggiorna il database prima di avviare l'app
setup_database()

# Crea l'istanza dell'app Flask
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)