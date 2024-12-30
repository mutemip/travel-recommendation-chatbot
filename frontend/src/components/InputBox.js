import React, { useState } from "react";
import { TextField, Button } from "@mui/material";

const InputBox = ({ onSendMessage }) => {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  return (
    <div className="input-box">
      <TextField
        fullWidth
        label="Type a message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <Button onClick={handleSend} variant="contained" style={{ marginLeft: "10px" }}>
        Send
      </Button>
    </div>
  );
};

export default InputBox;
