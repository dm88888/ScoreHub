##  ScoreHub — navodila za celoten projekt
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-Desktop-FF6F00?logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Web-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?logo=javascript&logoColor=black)
![MIT](https://img.shields.io/badge/License-MIT-2ea44f)

**ScoreHub** je večdelna aplikacija, sestavljena iz:

- **Backend** (Flask API)
- **Desktop Client** (Tkinter Card Battle igra)
- **Web Client** (HTML nadzorna plošča za pregled igralcev)

Projekt omogoča:

- vodenje igralcev,
- XP in level sistem,
- dnevne nagrade,
- izbiro herojev,
- real-time Card Battle igro (desktop),
- spletni pregled igralcev in statistike (web).

---

##  1. Namestitev projekta

##  Zahteve

- Python 3.10+
- pip
- Windows / macOS / Linux

##  Prenos projekta

V terminalu zaženi:

```bash
git clone <tvoj-repo-url>
cd ScoreHub
```

##  2. Backend — namestitev in zagon
 Namestitev virtualnega okolja:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```
##  Namestitev paketov
```bash
pip install -r requirements.txt
```

##  Zagon backenda
```bash
python app.py
```

Backend teče na naslovu:

http://127.0.0.1:5001

##  3. Desktop Client — namestitev in zagon

Namizni odjemalec nudi Card Battle igro, kjer igralec izbere dva heroja in se bori proti AI.

 Namestitev:
```bash
cd desktop_client
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
 Zagon aplikacije
python client.py

 Funkcije:

- dodaj igralca,

- izberi heroje,

- začni bitko,

- napad / obramba / special,

- XP in score nagrade.

##  4. Web Client — zagon

Web client služi kot pregledovalnik igralcev, leaderboarda in grafov.

Odpri datoteko:
```text
web_client/index.html
```

Za delovanje ni potreben poseben strežnik – gre za čisto frontend aplikacijo.

Web client omogoča:

- dodajanje igralcev,

- ogled vseh igralcev,

- leaderboard,

- grafični prikaz score statistike.

 Deluje samo, ko backend teče.

##  5. Kako komponente sodelujejo
| Komponenta       | Odvisnost | Namen |
|------------------|-----------|-------|
| Backend          | —         | Glavna logika, baza, API |
| Desktop client   | Backend   | Igra s kartami |
| Web client       | Backend   | Pregled igralcev in statistik |
##  6. Struktura projekta
```text
project/
│── backend/
│   ├── app.py
│   ├── models.py
│   ├── database.py
│   └── README.md
│
│── desktop_client/
│   ├── client.py
│   └── README.md
│
│── web_client/
│   ├── index.html
│   ├── script.js
│   └── README.md
│
└── README.md   (glavna navodila)
```
##  7. Glavne funkcionalnosti
## Upravljanje igralcev

- dodajanje, brisanje in posodabljanje score,

- XP in nivojski sistem,

- dnevne nagrade.

## Hero sistem

- 5 različnih herojev,

- igralec izbere 2 heroja in s tem ustvari ekipo.

## Card Battle gameplay

- real-time potezna bitka,

- napad / obramba / special ability,

AI nasprotnik s svojimi statistikami.

## Statistike in grafi

- leaderboard,

- graf prikaza score,

- na voljo samo v web clientu.
