## Slika 1: Arhitektura projekta ScoreHub
```mermaid
flowchart LR
    A["Desktop Client (Tkinter Game)"] --> C["Flask API"]
    B["Web Client (HTML + JS Dashboard)"] --> C["Flask API"]

    C --> D["SQLite Database"]

    subgraph Backend
        C
        D
    end
```

ScoreHub je sestavljen iz treh glavnih komponent, ki delujejo preko skupnega Flask REST API-ja.
```text
ScoreHub/
 ├── backend/         ← Flask API + poslovna logika + podatkovna baza
 ├── desktop_client/  ← Tkinter namizni odjemalec (dejanska igra)
 └── web_client/      ← Spletni dashboard (pregled podatkov)
```
## 1. Backend (Flask)

Backend je jedro projekta in vsebuje:

- REST API za upravljanje igralcev

- XP / Level / Score sistem

- Hero sistem (5 herojev s statistikami)

- Bitke (turn-based card combat)

- Dnevne nagrade

- SQLite baza podatkov

# Ključne značilnosti:

API je centralni vir podatkov za desktop + web odjemalca.

Vse operacije na igralcih gredo preko API-ja.

Stanja bitk so shranjena začasno v RAM-u (BATTLES{}).

## 2. Desktop Client (Tkinter)

Namizna aplikacija, kjer se dejansko igra.

# Funkcije:

Pregled in upravljanje igralcev

Izbira dveh herojev

Kartna bitka (napad / obramba / special)

Živi dnevnik boja

Modern UI (neonski gumbi, temna tema)

# Namen:

Igralec igra igro na računalniku, podatki pa se sinhronizirajo v backend.

## 3. Web Client (HTML + JS)

Spletna aplikacija služi kot dashboard:

- Pregled igralcev

- Dodajanje igralcev

- Lestvica najboljših

- Graf prikaza rezultatov

Ni igre — prikazuje podatke iz backend API-ja.

Namen:

Administracija in pregled statistike.

Podatkovni model (Tabela players)
```pgsql
players
players
 ├── id          INTEGER (PK)
 ├── name        TEXT
 ├── email       TEXT
 ├── avatar      TEXT
 ├── score       INTEGER
 ├── xp          INTEGER
 ├── level       INTEGER
 ├── hero1       TEXT
 ├── hero2       TEXT
 ├── join_date   TEXT   (ISO date)
 └── last_daily  TEXT   (ISO date)
```
## Slika 2: Podatkovni model za tabelo players v SQLite.
```mermaid
erDiagram
    PLAYER {
        int id PK
        string name
        string email
        string avatar
        int score
        int xp
        int level
        string hero1
        string hero2
        date join_date
        date last_daily
    }
```

Arhitektura bitk

1. Desktop odjemalec izbere heroe.

2. Pošlje zahtevo /battle/start/<id>

3. Backend ustvari stanje bitke:
```bash
BATTLES[player_id] = {
   p_hp, p_atk, p_def, p_spec,
   ai_hp, ai_atk, ai_def, ai_spec,
   log: []
}
```

4. Za vsako potezo frontend pošlje:
POST /battle/play/<id>

5. Backend izvede premike, posodobi stanje in vrne rezultat:

- continue

- win (+ XP + Score)

- lose

Po koncu se stanje bitke izbriše.
## Slika 3: Sekvenčni diagram poteka bitke (Battle Flow).
```mermaid
sequenceDiagram
    participant Player
    participant DesktopApp
    participant FlaskAPI
    participant BattleRAM as Battle State (RAM)

    Player->>DesktopApp: Izbere heroja 1 & 2
    DesktopApp->>FlaskAPI: POST /battle/start/<id>
    FlaskAPI->>BattleRAM: Ustvari bitko in shrani stanje
    FlaskAPI-->>DesktopApp: Vrne začetne HP statistike

    loop vsaka poteza
        Player->>DesktopApp: Izbere: Attack / Defend / Special
        DesktopApp->>FlaskAPI: POST /battle/play/<id>
        FlaskAPI->>BattleRAM: Izračuna potezo
        FlaskAPI-->>DesktopApp: Vrne HP + log + rezultat
    end

    alt zmaga
        FlaskAPI->>DesktopApp: result = win (+XP, +Score)
    else poraz
        FlaskAPI->>DesktopApp: result = lose
    end
```
