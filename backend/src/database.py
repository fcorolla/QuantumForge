from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
import os

# PostgreSQL Database URL
DATABASE_URL = "postgresql://user:password@localhost/quantumforge"

# Initialize PostgreSQL Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define Tables
class Weapon(Base):
    __tablename__ = "weapons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    damage = Column(Float, nullable=False)
    fire_rate = Column(Float, nullable=False)
    power_draw = Column(Float, nullable=False)
    heat_generation = Column(Float, nullable=False)
    dps = Column(Float, nullable=False)
    meta_rating = Column(Float, default=None)

class Ship(Base):
    __tablename__ = "ships"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    size = Column(String(50), nullable=False)
    class_ = Column(String(50), nullable=False)
    max_shields = Column(Float, nullable=False)
    max_weapons = Column(Integer, nullable=False)
    ai_recommended_loadout = Column(JSON, default={})

# Create Tables
Base.metadata.create_all(bind=engine)

# Initialize Redis Cache
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def setup_database():
    """Ensures database is initialized."""
    try:
        session = SessionLocal()
        print("PostgreSQL Database Connected Successfully")
        return session
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None

def cache_weapon_data(weapon_id, weapon_info):
    """Stores weapon data in Redis for quick lookup."""
    redis_client.set(f"weapon:{weapon_id}", str(weapon_info))

def fetch_cached_weapon(weapon_id):
    """Retrieves weapon data from Redis cache."""
    data = redis_client.get(f"weapon:{weapon_id}")
    return eval(data) if data else None