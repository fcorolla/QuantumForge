const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

app.get("/fetch_custom_builds", (req, res) => {
  res.json({ custom_builds: ["Build Alpha", "Build Bravo"] });
});

app.listen(4000, () => {
  console.log("QuantumForge Backend running on port 4000");
});