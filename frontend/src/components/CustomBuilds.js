import React, { useState, useEffect } from "react";
import axios from "axios";

const CustomBuilds = () => {
  const [builds, setBuilds] = useState([]);
  const [selectedShip, setSelectedShip] = useState("");
  const [newBuildName, setNewBuildName] = useState("");
  const [selectedWeapons, setSelectedWeapons] = useState([]);

  useEffect(() => {
    axios.get(`/fetch_custom_builds?ship_name=${selectedShip}`)
      .then(response => setBuilds(response.data.custom_builds))
      .catch(error => console.error("Error fetching builds:", error));
  }, [selectedShip]);

  const saveBuild = () => {
    axios.post("/save_custom_build", {
      ship_name: selectedShip,
      build_name: newBuildName,
      weapon_list: selectedWeapons,
    }).then(response => alert(response.data.message))
      .catch(error => console.error("Error saving build:", error));
  };

  return (
    <div className="p-4 bg-gray-900 text-white">
      <h2 className="text-xl font-bold">Custom Loadouts</h2>

      <label>Select Ship:</label>
      <input
        type="text"
        value={selectedShip}
        onChange={(e) => setSelectedShip(e.target.value)}
        className="p-2 border rounded"
      />

      <h3 className="mt-4">Available Builds</h3>
      <ul>
        {builds.map((build, index) => (
          <li key={index}>{build.name} - Weapons: {build.weapons.join(", ")}</li>
        ))}
      </ul>

      <h3 className="mt-4">Create a New Build</h3>
      <input
        type="text"
        placeholder="Enter Build Name"
        value={newBuildName}
        onChange={(e) => setNewBuildName(e.target.value)}
        className="p-2 border rounded"
      />
      <button onClick={saveBuild} className="mt-2 p-2 bg-blue-500">Save Loadout</button>
    </div>
  );
};

export default CustomBuilds;