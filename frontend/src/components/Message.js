import React from "react";

const Message = ({ sender, text }) => {
  const isUser = sender === "User";

  return (
    <div className={`message ${isUser ? "user-message" : "bot-message"}`}>
      {isUser ? (
        <p>{text}</p>
      ) : (
        // Render bot response, handling long content
        <div style={{ whiteSpace: "pre-wrap", overflowWrap: "break-word" }} dangerouslySetInnerHTML={{ __html: text }} />
      )}
    </div>
  );
};

export default Message;
