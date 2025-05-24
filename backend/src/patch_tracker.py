import requests
import json
from sqlalchemy.orm import Session
from database import Patch, Weapon

SC_PATCH_URL = "https://api.star-citizen-updates.com/patches"  # Placeholder for live API

def fetch_latest_patch():
    """Fetches the latest Star Citizen patch data from official/community sources."""
    try:
        response = requests.get(SC_PATCH_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching patch data: {e}")
        return None

def update_weapon_balance(db: Session, patch_data):
    """
    Auto-adjusts weapon stats based on balance changes reported in the latest patch.
    Updates AI recommendations accordingly.
    """
    affected_weapons = patch_data.get("affected_components", {})

    for weapon_name, new_stats in affected_weapons.items():
        weapon = db.query(Weapon).filter(Weapon.name == weapon_name).first()
        if weapon:
            weapon.damage = new_stats["damage"]
            weapon.fire_rate = new_stats["fire_rate"]
            weapon.meta_rating = new_stats.get("meta_rating", weapon.meta_rating)

    db.commit()

def track_patches(db: Session):
    """Main function to monitor patches and auto-sync balance updates."""
    latest_patch = fetch_latest_patch()
    if latest_patch:
        patch_version = latest_patch["patch_version"]
        if not db.query(Patch).filter(Patch.patch_version == patch_version).first():
            new_patch = Patch(
                patch_version=patch_version,
                change_log=json.dumps(latest_patch["change_log"]),
                affected_components=json.dumps(latest_patch["affected_components"])
            )
            db.add(new_patch)
            update_weapon_balance(db, latest_patch)
            db.commit()
            print(f"Patched to version: {patch_version}")