# 🎄 Christmas Project – v2.0 Full Refresh
## 📘 PROJECT GUIDE

---

## 📌 Project Overview

Questo progetto è una **web application Flask** sviluppata come progetto di Natale. Rappresenta una **ricostruzione completa** della versione precedente, con un focus specifico su:

- organizzazione modulare del progetto
- separazione delle responsabilità
- esperienza utente (UX)
- uso corretto di Flask (Blueprint, static, templates)

Repository del progetto originale: https://github.com/LucaPontellini/Christmas-project.git

---

## 🧠 Obiettivo del progetto

L’obiettivo iniziale è la realizzazione di una **homepage tematica stile “casino”**, caratterizzata da:

- layout cinematografico
- animazioni progressive
- musica di sottofondo
- struttura Flask pulita e scalabile

Questa homepage rappresenta il **punto di ingresso** dell’applicazione e costituisce la base visiva su cui verranno sviluppate le funzionalità backend.

Il progetto è pensato come base per una futura estensione:
- login
- giochi
- database
- funzionalità applicative complete

---

## 🗂️ Struttura del progetto

La struttura del progetto segue il modello modulare visto in classe, basato su **Application Factory** e **Blueprint**.

  
# DA CORREGGERE... LO SCHEMA E' DA TERMINARE...

```text
Christmas-Project-v2.0-Full-Refresh/
│
├── app/                            # Cuore pulsante dell'applicazione Flask
│   ├── __init__.py                 # Application Factory: create_app()
│   │
│   ├── account/                    # Blueprint Gestione Utenti
│   │   ├── repository.py           # Gestione Query SQL (CRUD, Soft/Hard Delete, PIN, Balance)
│   │   ├── routes.py               # Gestione Endpoints (Login, Register, Logout, Reset Password)
│   │   └── services.py             # Logica di supporto (Generazione e scadenza PIN di reset)
│   │
│   ├── admin/                      # Blueprint Pannello Amministratore
│   │   ├── repository.py           # Logica Dati: Statistiche dashboard (GGR, Chips, Users), Liste transazioni/accessi e azioni su utenti.
│   │   └── routes.py               # Endpoints: Dashboard (/admin/dashboard), Gestione Bilancio, Soft/Hard Delete e Restore utenti con protezione admin_required.
│   │
│   ├── bonus/                      # Blueprint Sistema Bonus
│   │   ├── repository.py           # Query atomiche: Riscatto bonus, aggiornamento balance e inserimento automatico in transactions.
│   │   ├── routes.py               # API Endpoint (/bonus/claim): Gestione risposte JSON per chiamate asincrone (Fetch API).
│   │   └── services.py             # Business Logic: Validazione univocità del bonus e distinzione tra metodi 'classic' e 'spid'.
│   │
│   ├── casino/                     # Blueprint Core Casino
│   │   ├── __init__.py             # Inizializzazione Blueprint
│   │   └── routes.py               # Punto centrale: Gestione Lobby, Logica Bonus visivi e placeholder per Giochi/Cassiere.
│   │
│   ├── database/                   # Infrastruttura Dati
│   │   ├── db.py                   # Gestione connessione SQLite: Factory, RowFactory e wrapper per query (one, all, execute, many).
│   │   └── schema.sql              # Definizione tabelle: Utenti, Bonus, Transazioni, Fiches e Log con logica di cancellazione a cascata.
│   │
│   ├── main/                       # Blueprint Landing Page
│   │   ├── __init__.py             # Inizializzazione Blueprint
│   │   └── routes.py               # Punto di ingresso: Gestione della rotta principale (/) e rendering della Landing Page (index.html).
│   │
│   ├── static/                     # Risorse Statiche Frontend
│   │   ├── css/                    # Fogli di stile modulari
│   │   │   ├── base.css            # Reset, sidebar e layout comune
│   │   │   ├── bonus.css           # Hero section e promo cards
│   │   │   ├── casino.css          # Grid dei giochi e UI lobby
│   │   │   ├── index.css           # Stile cinematografico landing page
│   │   │   └── modal.css           # Design universale finestre modali
│   │   │   
```

> **Nota di Refactoring (separazione logica):**
> - NOTA: Qui vanno estratti tutti i blocchi <style> dai file HTML

```text
│   │   │
│   │   ├── js/                     # Logica Client-Side
│   │   │   ├── auth_ui.js          # Gestione login/register e modali
│   │   │   ├── bonus.js            # Chiamate asincrone (Fetch) per bonus
│   │   │   ├── index.js            # Animazioni progressive landing
│   │   │   ├── music.js            # Controller audio (play/pause/volume)
│   │   │   └── ui_toast.js         # Sistema notifiche popup globale
```

> **Nota di Refactoring (separazione logica):**
> - NOTA: Qui vanno estratti tutti i blocchi <script> dai file HTML
> - da finire di commentare i css, html e js di tutto...

```text
│   │   │
│   │   ├── images/                 # Repository Grafico
│   │   │   ├── games/              # Cover Giochi
│   │   │   │   ├── american_roulette.jpg
│   │   │   │   ├── baccarat.jpg
│   │   │   │   ├── big_six_wheel.png
│   │   │   │   ├── blackjack.jpg
│   │   │   │   ├── caribbean_stud_poker.jpg
│   │   │   │   ├── classic_slot.jpg
│   │   │   │   ├── craps.jpg
│   │   │   │   ├── deuces_wild.jpg
│   │   │   │   ├── dream_catcher.jpg
│   │   │   │   ├── e_sports.jpg
│   │   │   │   ├── european_roulette.jpg
│   │   │   │   ├── fantasy_sports.jpg
│   │   │   │   ├── french_roulette.jpg
│   │   │   │   ├── greyhound_racing.jpg
│   │   │   │   ├── horse_racing.jpg
│   │   │   │   ├── jacks_or_better.jpg
│   │   │   │   ├── joker_poker.jpg
│   │   │   │   ├── keno.jpg
│   │   │   │   ├── let_it_ride.jpg
│   │   │   │   ├── mini_baccarat.jpg
│   │   │   │   ├── pai_gow_poker.jpg
│   │   │   │   ├── poker_texas_holdem.jpg
│   │   │   │   ├── progressive_slot.jpg
│   │   │   │   ├── punto_banco.jpg
│   │   │   │   ├── red_dog.jpg
│   │   │   │   ├── sic_bo.png
│   │   │   │   ├── three_card_poker.jpg
│   │   │   │   ├── video_poker.jpg
│   │   │   │   ├── video_slot.jpg
│   │   │   │   ├── virtual_sports.jpg
│   │   │   │   └── war.jpg
│   │   │   │
│   │   │   ├── payments/           # Metodi di Pagamento
│   │   │   │   ├── apple-pay.png
│   │   │   │   ├── bitcoin.png
│   │   │   │   ├── maestro.png
│   │   │   │   ├── mastercard.png
│   │   │   │   ├── paypal.png
│   │   │   │   ├── skrill.png
│   │   │   │   ├── visa.png
│   │   │   │   └── western-union.png
│   │   │   │
│   │   │   ├── 18-plus.png         # Icone di Sistema e Social
│   │   │   ├── ADM.png
│   │   │   ├── cashier.webp
│   │   │   ├── casino_photos.jpg
│   │   │   ├── favicon.ico
│   │   │   ├── github.jpeg
│   │   │   ├── instagram.jpeg
│   │   │   ├── monopoly_man.png
│   │   │   ├── play_icon.png
│   │   │   ├── roulette_icon.png
│   │   │   ├── SPID.png
│   │   │   ├── user_icon.png
│   │   │   └── youtube.jpeg
│   │   │
│   │   └── music/                  # Playlist Audio (Atmosfera Casino)
│   │       ├── Invisible_Cities.mp3 # Traccia dedicata alla Landing Page (index.html)
│   │       └── Jazzy_Smile.mp3      # Traccia per Lobby e aree interne (Casino, Admin, etc.)
│   │
│   ├── templates/                  # Motore Jinja2 (HTML)
│   │   ├── casino/                 # Template lobby e componenti dei giochi
│   │   ├── main/                   # Landing page (index.html)
│   │   ├── base.html               # Skeleton principale: definisce <head>, <body> e caricamento asset
│   │   ├── layout.html             # Struttura intermedia: include Sidebar + Main Content
│   │   └── modals.html             # Frammenti HTML per le finestre di Login/Register
│   │
```

> **Nota di Refactoring**
> - Rimuovere tutti i tag `<style>` e `<script>` inline  
> - Spostare il design in `static/css/`  
> - Spostare l’interattività in `static/js/`

```text
│   └── utils/                      # Funzioni Helper
│       ├── __init__.py             # Inizializzazione Blueprint
│       ├── auth.py                 # Decoratori: Protezione rotte (@login_required, @admin_required)
│       ├── color.py                # UI UX: Generazione deterministica di avatar (Colore + Iniziale)
│       └── security.py             # Security: Generazione PIN e calcolo scadenze temporali
│
├── instance/                       # Cartella dati locali esclusa dal file .gitignore assieme a database.db (Runtime)
│   └── database.db                 # Database SQLite reale (Generato dallo schema.sql)
│
├── run.py                          # Entry point: Avvio del server Flask
│                                   # 1. Chiama setup_database() per garantire che le tabelle esistano (DDL).
│                                   # 2. Crea l'app tramite l'Application Factory (create_app).
│                                   # 3. Lancia il server in modalità Debug (Hot Reload attivo).
│
├── setup_db.py                     # Script di setup: Bootstrap del database
│                                   # 1. Crea la cartella /instance se mancante.
│                                   # 2. Esegue schema.sql per generare le tabelle (solo al primo avvio).
│                                   # 3. Crea l'account 'admin' (password: admin123) se non esiste già.
│                                   # 4. Usa generate_password_hash per garantire la sicurezza sin dall'inizio.
│
├── requirements.txt                # Gestione Dipendenze
│                                   # - Flask: Il framework core per il web serving e il routing.
│                                   # - Werkzeug: Gestisce la sicurezza (password hashing) e il WSGI.
│                                   
├── LICENSE                         # Licenza MIT: Uso libero, obbligo di citazione
│                                   # - Garantisce il mio copyright.
│                                   # - Permette a chiunque di usare, copiare e modificare il codice.
│                                   # - Esclude la responsabilità (Disclaimer "AS IS").
│
├── .gitignore                      # Sicurezza e Pulizia: Esclusione file runtime
│                                   # - Protegge i dati sensibili (instance/, .env).
│                                   # - Esclude file di sistema inutili (__pycache__, .vscode).
│                                   # - Mantiene il repository leggero e professionale.
│
├── PROJECT_GUIDE.md                # Manuale tecnico: descrive il progetto in grandi linee, standard SoC e regole refactoring
│
└── README.md                       # Il file che hai appena scritto (Presentazione)
```

---

## 🧱 Architettura dell’applicazione

### 🔹 Application Factory

L’applicazione Flask viene creata tramite una **Application Factory** (`create_app()`), che consente:

- migliore organizzazione del codice
- separazione delle configurazioni
- maggiore scalabilità
- facilità di test ed estensione

Il file `app/__init__.py` ha il compito di:
- inizializzare Flask
- registrare i Blueprint
- configurare l’applicazione

---

### 🔹 Blueprint

La logica dell’applicazione è suddivisa in **Blueprint** per evitare un’app monolitica.

Attualmente è presente:
- `main` → gestione della homepage
- `casino` → gestione della lobby principale e navigazione interna

In futuro verranno aggiunti Blueprint dedicati a:
- autenticazione (`auth`)
- gestione delle entità
- funzionalità avanzate

---

## 🎨 Gestione dei template

I template HTML sono organizzati nella cartella `templates/` e suddivisi per Blueprint.

- `templates/main/index.html`  
  Contiene la struttura HTML della homepage.

I template utilizzano **Jinja2**, permettendo:
- separazione tra logica e presentazione
- riutilizzo dei layout
- estensioni future (base layout, partial, ecc.)

---

## 🗃️ Gestione dei file statici

Tutte le risorse statiche sono centralizzate nella cartella `static/`, suddivise per tipologia:

- `css/` → stile dell’applicazione
- `js/` → logica frontend (animazioni, audio, interazioni)
- `images/` → immagini dell’interfaccia
- `music/` → musica di sottofondo

Questa organizzazione segue le best practice Flask e migliora la leggibilità e manutenzione del progetto.

---

## 🎨 UI / UX & Responsive Design

Una parte centrale del progetto riguarda la **cura dell’esperienza utente (UX)** e dell’interfaccia grafica (UI).

La lobby del casino è stata progettata con particolare attenzione a:

- gerarchia visiva chiara
- call-to-action evidenti (Welcome Bonus, Play, Activate)
- coerenza cromatica (nero/oro stile casino)
- animazioni leggere e progressive

### 📱 Responsive Design

L’interfaccia è **completamente responsive**, con adattamenti specifici per dispositivi mobili:

- layout flessibile basato su Flexbox e Grid
- ridimensionamento di card, testi e pulsanti su smartphone
- gestione dedicata della sezione *Welcome Bonus* su mobile
- pulsanti full-width e spaziature maggiorate per touch

Le regole responsive sono gestite tramite **media queries** all’interno di `casino.css`, mantenendo separata la logica desktop da quella mobile.

---

## 📈 Evoluzione futura del progetto

Il progetto è progettato per crescere secondo i livelli di complessità richiesti.

### Livello 1 – Base
- Autenticazione utenti (registrazione / login)
- CRUD completo di un’entità principale
- separazione tra logica, dati e presentazione

### Livello 2 – Intermedio
- Relazioni 1-a-N (categorie, tag, ecc.)
- filtri di ricerca e ordinamento

### Livello 3 – Avanzato
- funzionalità social (commenti, like, preferiti)
- integrazione di API esterne

### Livello Pro – Eccellenza
- caricamento e gestione file
- dashboard con statistiche
- query SQL avanzate (GROUP BY, COUNT, AVG)

---

## 🧭 Filosofia del progetto

Il progetto non è pensato come un semplice esercizio, ma come una **base applicativa reale**, sviluppata seguendo:

- buone pratiche di sviluppo
- architettura modulare
- codice leggibile e manutenibile
- attenzione alla resa grafica e all’usabilità su dispositivi reali

Ogni funzionalità verrà aggiunta in modo incrementale, mantenendo la coerenza strutturale dell’applicazione.

---

## 📄 Note finali

Il file **PROJECT_GUIDE.md** verrà aggiornato progressivamente per documentare le nuove funzionalità, le scelte progettuali e l’evoluzione architetturale del progetto.


# TO DO:
- Ho dovuto ricostruire quasi tutto il progetto da zero per problemi strutturali e concettuali che rendevano impossibile proseguire.
- I commit precedenti erano basati sulla struttura iniziale del progetto di quest’anno, ma poi ho cambiato completamente approccio.
- Finché il progetto non funzionava non ho voluto fare altri commit, per evitare di salvare versioni inutili o sbagliate.
- Ora che la nuova versione è stabile, posso finalmente committare.
- Questa versione integra tutto ciò che volevo realizzare, riprendendo anche le idee del progetto di Natale scorso adattate ai requisiti di quest’anno.