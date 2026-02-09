#  Backend – ScoreHub

Flask API, ki upravlja igralce, XP/level sistem, dnevne nagrade ter hero/battle mehaniko za Card Battle igro (za desktop client).

---

##  Zagon backend strežnika
V terminalu:
```bash
cd backend
python app.py
```
Backend teče na:
http://127.0.0.1:5001

##  Glavne funkcije API-ja
- **/players** – pridobi vse igralce  
- **POST /players** – dodaj novega igralca  
- **PUT /players/<id>/score** – spremeni rezultat  
- **POST /players/<id>/daily** – dnevna nagrada  
- **POST /players/<id>/heroes** – izbira 2 herojev  
- **POST /battle/start/<id>** – začne bitko  
- **POST /battle/play/<id>** – izvede potezo v bitki  
- **/heroes** – seznam vseh herojev  

---

##  Struktura
```text
backend/
│── app.py
│── models.py
│── database.py
└── README.md
```
##  Uporabljene tehnologije
- Python 3 + Flask  
- SQLAlchemy ORM  
- SQLite baza  
- CORS za dostop iz web clienta  


##  Opombe
- Bitke se hranijo v RAM-u (BATTLES dict).  
- Desktop client uporablja celoten battle sistem.  
- Web client uporablja samo `/players` podatke (brez bitk).
