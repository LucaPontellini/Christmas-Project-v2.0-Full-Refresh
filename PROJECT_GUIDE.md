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

```
Christmas-Project-v2.0-Full-Refresh/
│
├── app/
│ ├── init.py # create_app()
│ │
│ ├── main/
│ │ ├── init.py
│ │ └── routes.py # homepage
│ │
│ ├── templates/
│ │ └── main/
│ │   └── index.html
│ │
│ └── static/
│   ├── css/
│   │ └── index.css
│   │
│   ├── js/
│   │ └── index.js
│   │
│   ├── images/
│   │ ├── casino_photos.jpg
│   │ ├── monopoly_man.png
│   │ ├── instagram.jpeg
│   │ ├── youtube.jpeg
│   │ ├── github.jpeg
│   │ └── favicon.ico
│   │
│   └── music/
│     └── Invisible_Cities.mp3
│
├── run.py
│
├── .gitignore
│
├── LICENSE
│
├── requirements.txt
│
├── README.md
└── PROJECT_GUIDE.md
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

Ogni funzionalità verrà aggiunta in modo incrementale, mantenendo la coerenza strutturale dell’applicazione.

---

## 📄 Note finali

Il file **PROJECT_GUIDE.md** verrà aggiornato progressivamente per documentare le nuove funzionalità, le scelte progettuali e l’evoluzione architetturale del progetto.