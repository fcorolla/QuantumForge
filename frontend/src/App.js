import React from "react";
import CustomBuilds from "./components/CustomBuilds";

function App() {
  return (
    <div className="p-6 bg-gray-800 min-h-screen text-white">
      <h1 className="text-3xl font-bold">QuantumForge Loadout Optimizer</h1>
      <CustomBuilds />
    </div>
  );
}

export default App;