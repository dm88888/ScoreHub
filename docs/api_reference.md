# API Referenca — ScoreHub Backend

Osnovni URL: `http://127.0.0.1:5001`

---

## GET /players  
Vrne seznam vseh igralcev.

### Odgovor:
```json
[
  { "id": 1, "name": "Ime_igralca", "score": 20, "xp": 50, "level": 1,
    "hero1": "Warrior", "hero2": "Mage" }
]
```
## POST /players

Ustvari novega igralca.

Telo:
```json
{ "name": "Ime_igralca" }
```
## GET /players/<id>

Podrobnosti enega igralca.

## PUT /players/<id>/score

Posodobi igralčev rezultat (score).

## DELETE /players/<id>

Izbriše igralca.

## POST /players/<id>/daily

Dnevna nagrada:
+5 score, +10 XP.

## GET /heroes

Vrne seznam razpoložljivih herojev.

## POST /players/<id>/heroes

Igralcu dodeli 2 heroja.

Telo:
```json
{ "hero1": "Warrior", "hero2": "Mage" }
```
## POST /battle/start/<id>

Začne bitko za igralca.

Odgovor:
```json
{
  "status": "battle started",
  "player_hp": 200,
  "enemy_hp": 180,
  "enemy_team": ["Rogue", "Hunter"]
}
```
## POST /battle/play/<id>

Izvede en potezo v bitki.

Telo:
```json
{ "move": "attack" }
```

Možni odgovori: zmaga, poraz ali nadaljevanje.
