from fastapi import FastAPI, HTTPException
from database import setup_database
from dps_calculator import calculate_dps
from ai_recommender import suggest_loadout

app = FastAPI()

@app.get("/")
def root():
    return {"message": "QuantumForge API is running"}

@app.get("/calculate_dps")
def get_dps(weapon_name: str, fire_rate: float, damage: float):
    """Computes DPS dynamically based on input stats."""
    dps_result = calculate_dps(weapon_name, fire_rate, damage)
    return {"weapon": weapon_name, "DPS": dps_result}

@app.get("/recommend_loadout")
def loadout_suggestions(ship_type: str):
    """AI-based loadout recommendations."""
    recommendations = suggest_loadout(ship_type)
    return {"ship": ship_type, "recommended_loadout": recommendations}

# Initialize database
setup_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)