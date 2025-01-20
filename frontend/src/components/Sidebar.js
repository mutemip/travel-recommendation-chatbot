import React from "react";
import { Select, MenuItem } from "@mui/material";

const Sidebar = ({ models, model, setModel, language, setLanguage }) => {
  return (
    <div className="sidebar">
      <h2>Settings</h2>
      <Select
        label="Model"
        value={model}
        onChange={(e) => setModel(e.target.value)}
        fullWidth
        style={{ marginTop: "20px" }}
      >
        {models.map((m) => (
          <MenuItem key={m} value={m}>
            {m}
          </MenuItem>
        ))}
      </Select>
      <Select
        label="Language"
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        fullWidth
        style={{ marginTop: "20px" }}
      >
        <MenuItem value="en">English</MenuItem>
        <MenuItem value="es">Spanish</MenuItem>
        <MenuItem value="fr">French</MenuItem>
        <MenuItem value="de">German</MenuItem>
        <MenuItem value="zh-cn">Chinese</MenuItem>
      </Select>
    </div>
  );
};

export default Sidebar;