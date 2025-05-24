from sqlalchemy.orm import Session
from database import Weapon, Ship
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def suggest_loadout(ship_type: str, db: Session) -> dict:
    """
    AI-driven loadout recommendation based on ship type & available weapons.
    Uses clustering algorithms to find best weapon combos for the selected ship.
    """
    weapons = db.query(Weapon).all()
    ship = db.query(Ship).filter(Ship.name == ship_type).first()

    if not ship:
        return {"error": f"Ship '{ship_type}' not found in the database."}

    # Extract weapon stats for clustering analysis
    data_matrix = np.array([[w.damage, w.fire_rate, w.power_draw, w.heat_generation] for w in weapons])
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_matrix)

    # Apply K-Means clustering (grouping similar weapons)
    num_clusters = min(len(weapons) // 3, 5)  # Ensure reasonable clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(scaled_data)

    best_weapons = []
    for cluster_idx in range(num_clusters):
        cluster_members = [weapons[i] for i, label in enumerate(kmeans.labels_) if label == cluster_idx]
        best_weapon = max(cluster_members, key=lambda w: w.dps)  # Select highest DPS weapon per cluster
        best_weapons.append(best_weapon)

    # Format AI recommendations
    recommendations = {
        "ship": ship.name,
        "optimized_loadout": [{"weapon": w.name, "DPS": w.dps, "Efficiency Score": round((w.damage * w.fire_rate) / (w.power_draw + w.heat_generation), 2)} for w in best_weapons]
    }

    return recommendations