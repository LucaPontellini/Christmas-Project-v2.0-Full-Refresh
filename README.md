# 🎄 Christmas Project – v2.0 Full Refresh

Web application sviluppata con **Flask** come progetto di Natale del 2025. Il progetto rappresenta una **ricostruzione completa** della versione realizzata l’anno precedente, con l’obiettivo di applicare correttamente le architetture e le buone pratiche studiate durante il corso.

Repository del progetto originale: https://github.com/LucaPontellini/Christmas-project.git

---

## 📌 Descrizione del progetto

L’applicazione nasce come una **homepage tematica stile “casino”**, con:

- layout cinematografico
- animazioni progressive
- musica di sottofondo
- gestione ordinata delle risorse statiche

Questa homepage rappresenta il **punto di ingresso** dell’applicazione
e costituisce la base visiva su cui verranno sviluppate le funzionalità backend.

Il progetto è pensato come **scalabile**, con successive estensioni dedicate a:
- autenticazione utenti
- gestione dei dati
- funzionalità applicative complete

---

## 🧠 Obiettivi didattici

L’obiettivo principale è realizzare una **web application Flask strutturata professionalmente**, focalizzandosi su:

- Application Factory (`create_app`)
- uso dei **Blueprint**
- separazione tra:
  - logica applicativa
  - template HTML
  - file statici
- accesso ai dati tramite **Repository Pattern**
- **Autenticazione utenti** (Registrazione / Login)
- **CRUD completo** di un’entità principale

---

## 🗂️ Struttura del progetto

La struttura del progetto segue il modello analizzato in classe ed è organizzata per moduli.

Per una descrizione dettagliata delle cartelle, dei file e delle scelte architetturali, fare riferimento al file: [**PROJECT_GUIDE.md**](PROJECT_GUIDE.md)

---

## ⚙️ Tecnologie utilizzate

- Python
- Flask
- Jinja2
- HTML / CSS / JavaScript
- SQLite (fase successiva del progetto)

---

## 📈 Livelli di complessità

Il progetto è progettato per crescere secondo i livelli di complessità richiesti:

- **Livello 1 (Base)**  
  Autenticazione utenti + CRUD completo di un’entità principale

- **Livello 2 (Intermedio)**  
  Gestione relazioni 1-a-N e filtri di ricerca / ordinamento

- **Livello 3 (Avanzato)**  
  Funzionalità social o integrazione di API esterne

- **Livello Pro (Eccellenza)**  
  Upload file o dashboard con statistiche SQL avanzate

---

## 🧭 Utilizzo dell’applicazione (passo passo):

## 📥 Clonare il repository

Per copiare il progetto in locale:

```bash
git clone https://github.com/LucaPontellini/Christmas-Project-v2.0-Full-Refresh.git
cd Christmas-Project-v2.0-Full-Refresh
```

## ▶️ Avvio dell’applicazione

### 1️⃣ Creare e attivare un ambiente virtuale

```bash
python -m venv .venv      # Windows
source .venv/bin/activate # macOS / Linux
```

### 2️⃣ Installare le dipendenze

```bash
pip install -r requirements.txt
```

### 3️⃣ Avviare l’applicazione

```bash
python run.py
```

L’applicazione sarà accessibile all’indirizzo:
`http://localhost:5001`

---

## 📄 Note finali

#### Il progetto verrà aggiornato progressivamente durante lo sviluppo, sia a livello di funzionalità che di documentazione.