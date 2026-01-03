-- database: ../../instance/database.db
/* TABELLA UTENTI

Questa tabella contiene tutte le informazioni principali sugli utenti registrati nel sistema. Ogni utente ha:

- un ID univoco
- un username unico
- una password (hashata)
- un avatar opzionale
- un ruolo (user/admin)
- un saldo (balance)
- un sistema di soft delete */

CREATE TABLE IF NOT EXISTS Users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificatore univoco dell’utente, generato automaticamente.
    Username TEXT NOT NULL UNIQUE, -- Nome utente scelto dall’utente. UNIQUE garantisce che non possano esistere due utenti con lo stesso username.
    Password TEXT NOT NULL, -- Password dell’utente (in realtà verrà salvata hashata, non in chiaro).
    Avatar TEXT, -- Percorso dell’immagine profilo dell’utente (opzionale).
    Role TEXT NOT NULL DEFAULT 'user', -- Ruolo dell’utente: "user" o "admin". DEFAULT 'user' assegna automaticamente il ruolo base.
    Balance INTEGER NOT NULL DEFAULT 0, -- Saldo del conto del giocatore. Utile per gestire depositi, prelievi e vincite.
    Is_deleted BOOLEAN NOT NULL DEFAULT 0, -- Soft delete: 0 = attivo, 1 = eliminato. L’utente non viene rimosso fisicamente dal DB (questa è semi-fittizia).
    Created_at DATETIME DEFAULT (datetime('now', 'localtime')), -- Data e ora di registrazione dell’utente in formato locale.
    Deleted_at DATETIME -- Data e ora in cui l’utente è stato soft-deleted.
);



/* TABELLA PASSWORD_RESET
   
Gestisce i PIN temporanei per il reset della password. Ogni PIN:

- appartiene a un utente
- ha una scadenza
- viene eliminato automaticamente se l’utente viene cancellato */

CREATE TABLE IF NOT EXISTS Password_reset_pins (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- Utente che ha richiesto il reset della password.
    Pin TEXT NOT NULL, -- Codice PIN temporaneo generato dal sistema.
    Expires_at DATETIME NOT NULL, -- Data e ora di scadenza del PIN. Dopo questa data il PIN non è più valido.
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Quando è stato generato il PIN.
    FOREIGN KEY (user_id) REFERENCES Users(Id) ON DELETE CASCADE -- Se l’utente viene eliminato, tutti i suoi PIN vengono eliminati automaticamente.
);



/* TABELLA CHIP_COLORS

Contiene la definizione dei colori delle fiches. Ogni colore ha:

- un nome
- un valore economico
- un colore esadecimale
- un ordine di visualizzazione */

CREATE TABLE IF NOT EXISTS Chip_colors (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT UNIQUE NOT NULL, -- Nome del colore (es. "red", "green", "burgundy"). UNIQUE evita duplicati.
    Value INTEGER NOT NULL, -- Valore economico della fiche di quel colore.
    Color_hex TEXT NOT NULL, -- Colore in formato esadecimale (es. #FF0000 = rosso).
    Display_order INTEGER DEFAULT 0 -- Ordine con cui mostrare le fiches nell’interfaccia grafica.
);



/* TABELLA USER_CHIPS

Rappresenta quante fiches di ogni colore possiede un utente. È una tabella di relazione N:N tra utenti e colori. */

CREATE TABLE IF NOT EXISTS User_chips (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- Utente proprietario delle fiches.
    Color_id INTEGER NOT NULL, -- Colore della fiche (collegato a chip_colors).
    Amount INTEGER NOT NULL DEFAULT 0, -- Quantità di fiches di quel colore possedute dall’utente.
    FOREIGN KEY (user_id) REFERENCES Users(Id) ON DELETE CASCADE,-- Se l’utente viene eliminato, anche le sue fiches vengono eliminate.
    FOREIGN KEY (Color_id) REFERENCES Chip_colors(Id) ON DELETE CASCADE, -- Se un colore viene eliminato, anche le righe collegate spariscono.
    UNIQUE(user_id, Color_id) -- Un utente può avere una sola riga per ogni colore.
);



/* TABELLA TRANSACTIONS

Registra ogni movimento economico associato a un utente. 

Tipologie supportate:
- deposito: aggiunta di saldo
- prelievo: rimozione di saldo
- vincita: incremento dovuto a una vincita di gioco
- perdita: decremento dovuto a una sconfitta
- bonus: accredito di un bonus
- manual_adj: aggiustamento manuale effettuato da un amministratore */

DROP TABLE IF EXISTS Transactions;
CREATE TABLE Transactions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificatore univoco della transazione.
    user_id INTEGER NOT NULL, -- Utente a cui appartiene la transazione.
    type TEXT NOT NULL,-- Tipo di transazione. Può essere: deposito, prelievo, vincita, perdita, bonus, manual_adj.
    Amount INTEGER NOT NULL, -- Importo della transazione (positivo o negativo a seconda del tipo).
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data e ora della registrazione della transazione.
    FOREIGN KEY (user_id) REFERENCES Users(Id) ON DELETE CASCADE -- Se l’utente viene eliminato, anche le sue transazioni vengono eliminate.
);



/* TABELLA BONUSES

Contiene i bonus disponibili nel sistema. Ogni bonus ha:

- un tipo (es. registration)
- un metodo (classic, spid)
- un importo */

CREATE TABLE IF NOT EXISTS Bonuses (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Type TEXT NOT NULL, -- Tipo di bonus (es. "registration").
    Method TEXT NOT NULL, -- Metodo con cui si ottiene il bonus (classic/spid).
    Amount INTEGER NOT NULL, -- Importo del bonus.
    Is_active BOOLEAN NOT NULL DEFAULT 1, -- Se il bonus è attivo o disattivato.
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data di creazione del bonus.
    UNIQUE(Type, Method) -- Evita duplicati: non possono esistere due bonus identici.
);



/* TABELLA USER_BONUSES

Rappresenta i bonus assegnati agli utenti. Ogni riga indica:

- quale bonus ha ricevuto l’utente
- se è stato attivato
- quando è stato attivato */

CREATE TABLE IF NOT EXISTS User_bonuses (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- Utente che ha ricevuto il bonus.
    Bonus_id INTEGER NOT NULL, -- Bonus assegnato.
    Is_activated BOOLEAN NOT NULL DEFAULT 0,
    -- 0 = bonus assegnato ma non attivato.
    -- 1 = bonus attivato.

    Activated_at DATETIME, -- Data di attivazione del bonus.
    Claimed_method TEXT, -- Metodo con cui l’utente ha richiesto il bonus (opzionale).
    FOREIGN KEY (user_id) REFERENCES Users(Id) ON DELETE CASCADE,
    FOREIGN KEY (Bonus_id) REFERENCES Bonuses(Id) ON DELETE CASCADE,
    UNIQUE(user_id, Bonus_id) -- Un utente non può ricevere due volte lo stesso bonus.
);



/* SEED BONUS

Inserisce i bonus iniziali nel sistema.

- classic: bonus standard
- spid: bonus più alto perché verificato */

INSERT OR IGNORE INTO Bonuses (Type, Method, Amount)
VALUES
    ('registration', 'classic', 50),
    ('registration', 'spid', 100);



/* POPOLAMENTO CHIP COLORS

Inserisce i colori delle fiches con valori realistici. Note sui colori:

- burgundy: rosso scuro elegante
- light_blue: azzurro chiaro
- yellow_high: giallo brillante
- pink: rosa acceso
- gray: grigio metallico
- orange_high: arancione intenso
- black_high: nero per fiches di valore molto alto */

INSERT OR IGNORE INTO Chip_colors (Name, Value, Color_hex, Display_order) VALUES
    ('white',       1,      '#FFFFFF',  1),
    ('red',         5,      '#FF0000',  2),
    ('orange',      10,     '#FFA500',  3),
    ('yellow',      20,     '#FFFF00',  4),
    ('green',       25,     '#008000',  5),
    ('black',       100,    '#000000',  6),
    ('purple',      500,    '#800080',  7),
    ('burgundy',    1000,   '#800000',  8),
    ('light_blue',  2000,   '#ADD8E6',  9),
    ('yellow_high', 5000,   '#FFD700', 10),
    ('pink',        10000,  '#FF69B4', 11),
    ('gray',        25000,  '#C0C0C0', 12),
    ('orange_high', 50000,  '#FF4500', 13),
    ('black_high',  100000, '#000000', 14);



/* TABELLA ACCESS_LOGS

Registra ogni accesso e disconnessione degli utenti.
Serve per:

- tracciare login e logout
- monitorare attività sospette
- conservare lo storico degli accessi */

CREATE TABLE IF NOT EXISTS Access_logs (
    Id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificatore univoco del log.
    user_id INTEGER, -- Utente che ha effettuato l’azione. Può essere NULL se l’utente viene eliminato (ON DELETE SET NULL).
    Action TEXT NOT NULL, -- Tipo di azione registrata: "login" o "logout".
    Ip_address TEXT, -- Indirizzo IP da cui è avvenuto l’accesso o la disconnessione.
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data e ora in cui è stato registrato l’evento.
    FOREIGN KEY (user_id) REFERENCES Users(Id) ON DELETE SET NULL -- Se l’utente viene eliminato, il campo user_id diventa NULL per mantenere comunque lo storico degli accessi.
);



/* TABELLA ADMIN_LOGS

Registra tutte le azioni amministrative effettuate nel sistema. Ogni log contiene:

- quale admin ha eseguito l’azione
- quale utente è stato coinvolto
- il tipo di azione (soft_delete, restore, hard_delete)
- il timestamp dell’operazione */

DROP TABLE IF EXISTS Admin_logs;

CREATE TABLE Admin_logs (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificatore univoco del log
    Admin_id INTEGER, -- Admin che ha eseguito l’azione. Può diventare NULL se l’admin viene eliminato.
    Target_user_id INTEGER, -- Utente coinvolto nell’azione. Può diventare NULL se l’utente viene eliminato.
    Action TEXT NOT NULL, -- Tipo di azione: soft_delete, restore, hard_delete.
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Timestamp automatico dell’azione.
    FOREIGN KEY (Admin_id) REFERENCES Users(Id) ON DELETE SET NULL, -- Mantiene il log anche se l’admin viene eliminato.
    FOREIGN KEY (Target_user_id) REFERENCES Users(Id) ON DELETE SET NULL -- Mantiene il log anche se l’utente viene eliminato.
);