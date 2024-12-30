import React from "react";
import { Select, MenuItem } from "@mui/material";

const Sidebar = ({ models, model, setModel }) => {
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
    </div>
  );
};

export default Sidebar;
