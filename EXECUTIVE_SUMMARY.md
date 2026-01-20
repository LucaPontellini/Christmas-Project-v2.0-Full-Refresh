# Executive Summary

## Christmas Project – v2.0 Full Refresh

**Christmas Project – v2.0 Full Refresh** è una web application sviluppata in **Flask** come progetto di Natale 2025, nata con l’obiettivo di ricostruire e migliorare integralmente una versione precedente realizzata l’[anno prima](https://github.com/LucaPontellini/Christmas-project.git). Il progetto rappresenta un esercizio completo di progettazione, sviluppo e documentazione di un’applicazione web strutturata secondo buone pratiche professionali.

L’applicazione si presenta come una **piattaforma tematica stile casinò**, con una forte attenzione all’impatto visivo, all’esperienza utente e alla separazione chiara delle responsabilità tra frontend, backend e livello dati.

---

## Finalità del progetto

L’obiettivo principale del progetto non è la simulazione realistica di un casinò online, ma la **costruzione di una web application scalabile e ben organizzata**, capace di dimostrare:

- comprensione delle architetture Flask
- gestione completa del ciclo di vita degli utenti (CRUD completo)
- integrazione tra interfaccia grafica, logica applicativa e database
- capacità di progettare un sistema estendibile nel tempo

Il progetto è pensato come **base evolutiva**, su cui poter innestare in futuro funzionalità più complesse (giochi, transazioni avanzate, API esterne, ecc.).

---

## Panoramica funzionale

L’applicazione è composta da due macro-aree principali:

### Area pubblica
- Landing page iniziale con animazioni, musica e layout cinematografico
- Homepage del casinò (lobby) accessibile anche senza autenticazione
- Navigazione completa dell’interfaccia con contenuti dimostrativi
- Giochi, bonus e sezioni presenti come **placeholder** per sviluppi futuri

### Area utenti autenticati
- Registrazione account con validazione dei dati
- Login e gestione sessione
- Recupero password tramite PIN di sicurezza
- Logout e eliminazione account tramite **soft delete**
- Personalizzazione dinamica della lobby dopo l’autenticazione

### Area amministrativa
- Dashboard riservata agli utenti con ruolo **admin**
- Monitoraggio utenti e stato degli account
- Gestione dei saldi e delle operazioni critiche
- Tracciamento completo delle attività tramite log amministrativi
- Pannello concepito come centro di controllo del sistema

---

## Approccio architetturale

Il progetto adotta un’architettura modulare e ordinata, basata su:

- **Application Factory** per l’inizializzazione dell’app Flask
- utilizzo dei **Blueprint** per separare le aree funzionali
- distinzione chiara tra:
  - logica applicativa (Python e Jinja)
  - template HTML
  - file statici (CSS, JS, immagini, audio)
- accesso ai dati tramite pattern dedicati
- database **SQLite3** inizializzato automaticamente all’avvio

Queste scelte consentono al progetto di rimanere leggibile, manutenibile ed estendibile, anche con l’aumento della complessità.

---

## Stato attuale del progetto

Alla versione attuale:

- il sistema di **autenticazione utenti** è pienamente funzionante
- la **dashboard admin** è operativa e integrata con il database
- le principali operazioni sono tracciate tramite log
- giochi e sistema di cassa sono volutamente non implementati

Gli elementi non ancora attivi sono presenti come **predisposizione strutturale**, per dimostrare una progettazione orientata allo sviluppo futuro.

---

## Valore didattico

Christmas Project – v2.0 Full Refresh rappresenta un progetto completo che dimostra:

- capacità di analisi e pianificazione
- attenzione alla documentazione tecnica e operativa
- applicazione concreta delle best practice studiate
- consapevolezza della differenza tra prototipo funzionale e prodotto finale

Il progetto non si limita a “funzionare”, ma è costruito per essere **letto, capito e mantenuto**, rendendolo adatto come progetto di studio, portfolio personale o base per sviluppi successivi.

---

## Documentazione di riferimento

Per approfondimenti specifici:

- **[`README.md`](README.md)** → panoramica generale e istruzioni rapide
- **[`PROJECT_GUIDE.md`](PROJECT_GUIDE.md)** → descrizione architetturale e strutturale
- **[`PROJECT_OPERATION.md`](PROJECT_OPERATION.md)** → guida operativa dettagliata all’utilizzo dell’applicazione

---

**Christmas Project – v2.0 Full Refresh** non è solo un esercizio tecnico, ma una dimostrazione concreta di crescita progettuale e maturità nello sviluppo di applicazioni web.

---

## Percorso evolutivo del progetto

Il progetto si inserisce all’interno di un percorso di sviluppo progressivo, documentato attraverso diverse iterazioni nel tempo:

- **[End of Year Project for Computer Science - Poker](https://github.com/LucaPontellini/End-of-Year-Project-for-Computer-Science-Poker.git)**

- **[Christmas Project *(prima versione)*](https://github.com/LucaPontellini/Christmas-project.git)**

- **[Texas Hold’em Poker](https://github.com/LucaPontellini/Texas-Hold-em-poker.git)**

- **[Christmas Project – v2.0 Full Refresh *(versione attuale)*](https://github.com/LucaPontellini/Christmas-Project-v2.0-Full-Refresh.git)**