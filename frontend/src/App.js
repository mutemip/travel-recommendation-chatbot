import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import Chatbot from "./components/Chatbot";
import "./styles.css";

const App = () => {
  const [models, setModels] = useState([]);
  const [model, setModel] = useState("");
  const [messages, setMessages] = useState([]);

  // Fetch models from the backend
  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await fetch("http://localhost:5000/models");
        const data = await response.json();
        setModels(data.models);
        if (data.models.length > 0) {
          setModel(data.models[0]); // Set default model
        }
      } catch (error) {
        console.error("Error fetching models:", error);
      }
    };
    fetchModels();
  }, []);

  const sendMessage = async (userMessage) => {
    const newMessages = [...messages, { sender: "User", text: userMessage }];
    setMessages(newMessages);
  
    try {
      const response = await fetch("http://localhost:5000/converse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          model, // Ensure this matches the backend expectation
        }),
      });
      const data = await response.json();
      setMessages((prev) => [...prev, { sender: "Bot", text: data.response }]);
    } catch (error) {
      console.error("Error:", error);
    }
  };
  

  return (
    <div className="app">
      <Sidebar models={models} model={model} setModel={setModel} />
      <Chatbot messages={messages} onSendMessage={sendMessage} />
    </div>
  );
};

export default App;
