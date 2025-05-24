from sqlalchemy.orm import Session
from database import Loadout, Weapon, Ship


def save_custom_build(db: Session, ship_name: str, build_name: str, weapon_list: list):
    """
    Saves a player-customized loadout into the database.
    """
    ship = db.query(Ship).filter(Ship.name == ship_name).first()
    if not ship:
        return {"error": f"Ship '{ship_name}' not found."}

    new_loadout = Loadout(ship_id=ship.id, custom_name=build_name)
    db.add(new_loadout)
    db.commit()

    for weapon_name in weapon_list:
        weapon = db.query(Weapon).filter(Weapon.name == weapon_name).first()
        if weapon:
            db.add(Loadout(ship_id=ship.id, weapon_id=weapon.id, custom_name=build_name))

    db.commit()
    return {"message": f"Custom build '{build_name}' saved successfully!"}


def fetch_custom_builds(db: Session, ship_name: str):
    """
    Retrieves all stored player-customized builds for a given ship.
    """
    ship = db.query(Ship).filter(Ship.name == ship_name).first()
    if not ship:
        return {"error": f"Ship '{ship_name}' not found."}

    loadouts = db.query(Loadout).filter(Loadout.ship_id == ship.id).all()
    return {"ship": ship_name, "custom_builds": [{"name": l.custom_name, "weapons": l.weapon_id} for l in loadouts]}


def rate_custom_build(db: Session, build_name: str, rating: float):
    """
    Allows users to rate stored builds, improving AI recommendations.
    """
    loadout = db.query(Loadout).filter(Loadout.custom_name == build_name).first()
    if not loadout:
        return {"error": f"Build '{build_name}' not found."}

    loadout.user_rating = rating
    db.commit()
    return {"message": f"Build '{build_name}' rated {rating}/5!"}