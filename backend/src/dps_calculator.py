from sqlalchemy.orm import Session
from database import Weapon, redis_client


def calculate_dps(weapon_name: str, fire_rate: float, damage: float) -> float:
    """
    Computes DPS dynamically based on input stats.
    DPS = Damage * Fire Rate
    """
    return damage * fire_rate


def compute_efficiency(weapon: Weapon) -> dict:
    """
    Evaluates weapon efficiency based on power draw, heat generation, and meta rating.
    Returns a structured dictionary with optimization insights.
    """
    efficiency_score = (weapon.damage * weapon.fire_rate) / (weapon.power_draw + weapon.heat_generation)

    return {
        "weapon": weapon.name,
        "DPS": weapon.dps,
        "Efficiency Score": round(efficiency_score, 2),
        "Meta Rating": weapon.meta_rating if weapon.meta_rating else "Not yet rated"
    }


def get_weapon_data(db: Session, weapon_name: str):
    """
    Fetches weapon stats from the database and caches results for faster access.
    """
    cached_data = redis_client.get(f"weapon:{weapon_name}")
    if cached_data:
        return eval(cached_data)  # Use cached data if available

    weapon = db.query(Weapon).filter(Weapon.name == weapon_name).first()
    if not weapon:
        return {"error": f"Weapon '{weapon_name}' not found in the database."}

    weapon_data = compute_efficiency(weapon)

    # Store result in Redis cache for future quick lookups
    redis_client.set(f"weapon:{weapon_name}", str(weapon_data))

    return weapon_data