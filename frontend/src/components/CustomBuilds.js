import React, { useState, useEffect } from "react";

const CustomBuilds = () => {
  const [builds, setBuilds] = useState([]);
  const [selectedShip, setSelectedShip] = useState("");
  const [newBuildName, setNewBuildName] = useState("");
  const [selectedWeapons, setSelectedWeapons] = useState([]);

  useEffect(() => {
    fetch(`/fetch_custom_builds?ship_name=${selectedShip}`)
      .then((res) => res.json())
      .then((data) => setBuilds(data.custom_builds))
      .catch((err) => console.error("Error fetching builds:", err));
  }, [selectedShip]);

  const saveBuild = () => {
    fetch("/save_custom_build", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ship_name: selectedShip,
        build_name: newBuildName,
        weapon_list: selectedWeapons,
      }),
    })
      .then((res) => res.json())
      .then((data) => alert(data.message))
      .catch((err) => console.error("Error saving build:", err));
  };

  return (
    <div>
      <h2>Custom Loadouts</h2>
      <label>Select Ship:</label>
      <input
        type="text"
        value={selectedShip}
        onChange={(e) => setSelectedShip(e.target.value)}
      />
      <h3>Available Builds</h3>
      <ul>
        {builds.map((build) => (
          <li key={build.name}>{build.name} - Weapons: {build.weapons.join(", ")}</li>
        ))}
      </ul>
      <h3>Create a New Build</h3>
      <input
        type="text"
        placeholder="Enter Build Name"
        value={newBuildName}
        onChange={(e) => setNewBuildName(e.target.value)}
      />
      <button onClick={saveBuild}>Save Loadout</button>
    </div>
  );
};

export default CustomBuilds;