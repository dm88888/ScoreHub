from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime, date
from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    avatar = Column(String, nullable=True)
    score = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    join_date = Column(Date, default=date.today)
    status = Column(String, default="offline")
    last_daily = Column(Date, nullable=True)
    hero_class = Column(String, default="Warrior")
    hp = Column(Integer, default=100)
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)
    mana = Column(Integer, default=30)
    hero1 = Column(String, default=None)
    hero2 = Column(String, default=None)


