from flask import Flask, jsonify, request
from flask_cors import CORS
from database import Base, engine, SessionLocal
from models import Player
import random
from datetime import date, datetime


# HEROES – card-battle system


HEROES = {
    "Warrior": {
        "hp": 120,
        "atk": 15,
        "def": 6,
        "special": 30  # Power Slash
    },
    "Mage": {
        "hp": 75,
        "atk": 8,
        "def": 3,
        "special": 45  # Fireball
    },
    "Rogue": {
        "hp": 90,
        "atk": 12,
        "def": 4,
        "special": 20  # Critical Strike
    },
    "Paladin": {
        "hp": 110,
        "atk": 10,
        "def": 10,
        "special": 25  # Holy Smite
    },
    "Hunter": {
        "hp": 100,
        "atk": 14,
        "def": 5,
        "special": 18  # Poison Arrow
    }
}

# TEMP battle states stored in RAM
BATTLES = {}



app = Flask(__name__)
CORS(app)


# --------------------------------------------------------
# PLAYER XP LEVEL SYSTEM
# --------------------------------------------------------
def update_level(player):
    while player.xp >= player.level * 100:
        player.level += 1



# DATABASE INIT

Base.metadata.create_all(bind=engine)



# HOME

@app.get("/")
def home():
    return jsonify({
        "status": "running",
        "routes": [
            "/players",
            "/players/<id>",
            "/players/<id>/heroes",
            "/battle/start/<id>",
            "/battle/play/<id>",
            "/heroes",
            "/players/<id>/play",
        ]
    })



# HERO ENDPOINTS

@app.get("/heroes")
def get_heroes():
    return jsonify(HEROES)


@app.post("/players/<int:pid>/heroes")
def select_heroes(pid):
    db = SessionLocal()
    player = db.query(Player).filter(Player.id == pid).first()

    if not player:
        db.close()
        return jsonify({"error": "Player not found"}), 404

    data = request.json
    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    if hero1 not in HEROES or hero2 not in HEROES:
        return jsonify({"error": "Invalid hero"}), 400

    if hero1 == hero2:
        return jsonify({"error": "Choose 2 different heroes"}), 400

    player.hero1 = hero1
    player.hero2 = hero2

    db.commit()
    db.close()

    return jsonify({
        "status": "heroes selected",
        "hero1": hero1,
        "hero2": hero2
    })



# GET ALL PLAYERS

@app.get("/players")
def get_players():
    db = SessionLocal()
    players = db.query(Player).all()
    db.close()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "score": p.score,
            "xp": p.xp,
            "level": p.level,
            "hero1": p.hero1,
            "hero2": p.hero2
        }
        for p in players
    ])



# GET ONE PLAYER

@app.get("/players/<int:pid>")
def get_player(pid):
    db = SessionLocal()
    player = db.query(Player).filter(Player.id == pid).first()
    db.close()

    if not player:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "id": player.id,
        "name": player.name,
        "email": player.email,
        "avatar": player.avatar,
        "score": player.score,
        "xp": player.xp,
        "level": player.level,
        "join_date": str(player.join_date),
        "last_daily": str(player.last_daily),
        "hero1": player.hero1,
        "hero2": player.hero2
    })



# ADD PLAYER

@app.post("/players")
def add_player():
    data = request.json
    db = SessionLocal()

    player = Player(
        name=data["name"],
        email=data.get("email"),
        avatar=data.get("avatar"),
        score=0,
        xp=0,
        level=1,
        status="offline"
    )

    db.add(player)
    db.commit()
    db.refresh(player)
    db.close()

    return jsonify({"status": "ok", "id": player.id})



# EDIT SCORE

@app.put("/players/<int:pid>/score")
def edit_score(pid):
    data = request.json
    db = SessionLocal()
    player = db.query(Player).filter(Player.id == pid).first()

    if not player:
        db.close()
        return jsonify({"error": "Player not found"}), 404

    player.score = data.get("score", player.score)
    db.commit()
    db.close()

    return jsonify({"status": "score updated"})


# --------------------------------------------------------
# DELETE PLAYER
# --------------------------------------------------------
@app.delete("/players/<int:pid>")
def delete_player(pid):
    db = SessionLocal()
    player = db.query(Player).filter(Player.id == pid).first()

    if not player:
        db.close()
        return jsonify({"error": "not found"}), 404

    db.delete(player)
    db.commit()
    db.close()

    return jsonify({"status": "deleted"})


# --------------------------------------------------------
# DAILY REWARD
# --------------------------------------------------------
@app.post("/players/<int:pid>/daily")
def daily_reward(pid):
    db = SessionLocal()
    player = db.query(Player).filter(Player.id == pid).first()

    if not player:
        db.close()
        return jsonify({"error": "not found"}), 404

    today = date.today()

    if player.last_daily == today:
        return jsonify({"error": "Already claimed today"}), 400

    player.last_daily = today
    player.score += 5
    player.xp += 10

    update_level(player)

    db.commit()
    db.close()

    return jsonify({"status": "daily reward claimed"})


# --------------------------------------------------------
# QUEST (kept for compatibility)
# --------------------------------------------------------
QUESTS = {
    "combat": [
        ("Porazi goblina", "Igralec se spopade z goblinom v gozdu."),
        ("Premagaj volka", "Divji volk napade iz sence!")
    ],
    "explore": [
        ("Razišči tempelj", "Temni hodniki skrivajo skrivnosti."),
        ("Sledi svetlobi", "Svetleči simboli vodijo globlje.")
    ]
}


@app.post("/players/<int:pid>/play")
def play_game(pid):
    db = SessionLocal()
    player = db.query(Player).filter(Player.id == pid).first()

    if not player:
        return jsonify({"error": "not found"}), 404

    category = random.choice(list(QUESTS.keys()))
    quest, description = random.choice(QUESTS[category])

    xp_gain = random.randint(5, 20)
    score_gain = random.randint(2, 8)

    player.xp += xp_gain
    player.score += score_gain

    update_level(player)
    db.commit()
    db.close()

    return jsonify({
        "quest": quest,
        "description": description,
        "xp": xp_gain,
        "score": score_gain
    })


# --------------------------------------------------------
# BATTLE SYSTEM
# --------------------------------------------------------
@app.post("/battle/start/<int:pid>")
def battle_start(pid):
    data = request.json
    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    if hero1 not in HEROES or hero2 not in HEROES:
        return jsonify({"error": "Invalid hero"}), 400

    # Player stats
    p_hp = HEROES[hero1]["hp"] + HEROES[hero2]["hp"]
    p_atk = HEROES[hero1]["atk"] + HEROES[hero2]["atk"]
    p_def = HEROES[hero1]["def"] + HEROES[hero2]["def"]
    p_spec = HEROES[hero1]["special"] + HEROES[hero2]["special"]

    # AI picks team
    ai1, ai2 = random.sample(list(HEROES.keys()), 2)
    ai_hp = HEROES[ai1]["hp"] + HEROES[ai2]["hp"]
    ai_atk = HEROES[ai1]["atk"] + HEROES[ai2]["atk"]
    ai_def = HEROES[ai1]["def"] + HEROES[ai2]["def"]
    ai_spec = HEROES[ai1]["special"] + HEROES[ai2]["special"]

    BATTLES[pid] = {
        "p_hp": p_hp, "p_atk": p_atk, "p_def": p_def, "p_spec": p_spec,
        "ai_hp": ai_hp, "ai_atk": ai_atk, "ai_def": ai_def, "ai_spec": ai_spec,
        "log": []
    }

    return jsonify({
        "status": "battle started",
        "player_hp": p_hp,
        "enemy_hp": ai_hp,
        "enemy_team": [ai1, ai2]
    })


@app.post("/battle/play/<int:pid>")
def battle_play(pid):
    data = request.json
    move = data.get("move")

    if pid not in BATTLES:
        return jsonify({"error": "No active battle"}), 400

    battle = BATTLES[pid]

    # AI chooses move
    ai_move = random.choice(["attack", "defend", "special"])

    # Player damage
    if move == "attack":
        dmg = battle["p_atk"]
    elif move == "defend":
        dmg = max(battle["p_def"] - battle["ai_atk"], 0)
    elif move == "special":
        dmg = battle["p_spec"]
    else:
        dmg = 0

    battle["ai_hp"] -= dmg

    # AI damage
    if ai_move == "attack":
        ai_dmg = battle["ai_atk"]
    elif ai_move == "defend":
        ai_dmg = max(battle["ai_def"] - battle["p_atk"], 0)
    elif ai_move == "special":
        ai_dmg = battle["ai_spec"]
    else:
        ai_dmg = 0

    battle["p_hp"] -= ai_dmg

    # Log
    battle["log"].append(f"You used {move}, enemy used {ai_move}")

    # Check win
    if battle["ai_hp"] <= 0:
        del BATTLES[pid]

        db = SessionLocal()
        player = db.query(Player).filter(Player.id == pid).first()
        player.score += 15
        player.xp += 20
        update_level(player)
        db.commit()
        db.close()

        return jsonify({"result": "win", "xp": 20, "score": 15})

    # Check lose
    if battle["p_hp"] <= 0:
        del BATTLES[pid]
        return jsonify({"result": "lose"})

    return jsonify({
        "result": "continue",
        "player_hp": battle["p_hp"],
        "enemy_hp": battle["ai_hp"],
        "log": battle["log"][-1]
    })


# --------------------------------------------------------
# RUN SERVER
# --------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
