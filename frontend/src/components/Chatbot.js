import React, { useEffect, useRef } from "react";
import Message from "./Message";
import InputBox from "./InputBox";
import ReactMarkdown from "react-markdown";


const Chatbot = ({ messages, onSendMessage }) => {
  const chatWindowRef = useRef(null);

  // Scroll to the bottom whenever a new message is added
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="chatbot">
      <div
        className="chat-window"
        ref={chatWindowRef}
        style={{ overflowY: "auto", maxHeight: "80vh" }} // Add scrollable window
      >
        {messages.map((msg, idx) => (
          <Message key={idx} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <InputBox onSendMessage={onSendMessage} />
    </div>
  );
};

const ChatMessage = ({ sender, text }) => {
    return (
      <div className={`message ${sender.toLowerCase()}`}>
        <ReactMarkdown>{text}</ReactMarkdown>
      </div>
    );
  };

export default Chatbot;
