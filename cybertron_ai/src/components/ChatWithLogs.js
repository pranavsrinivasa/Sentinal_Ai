// components/ChatWithLogs.js
import React, { useState } from 'react';
import axios from 'axios';

function ChatWithLogs() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newMessage = { text: input, sender: 'user' };
    setMessages([...messages, newMessage]);
    setInput('');

    try {
      const response = await axios.post('http://localhost:8080/agent_query', { prompt: input });
      const botMessage = { text: response.data.response, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleDefaultMessage = () => {
    setInput('Create Accurate Audit reports');
    handleSubmit({ preventDefault: () => {} });
  };

  return (
    <div>
      <h2>Chat with Logs</h2>
      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
      <button onClick={handleDefaultMessage}>Create Accurate Audit reports</button>
    </div>
  );
}

export default ChatWithLogs