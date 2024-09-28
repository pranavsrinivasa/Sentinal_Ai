// components/ChatWithLogs.js
import React, { useState } from 'react';
import axios from 'axios';

function ChatWithLogs() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleDefaultMessage = () => {
    const temp = 'Analyze the processes of the system in detail and provide insights and a complete audit report about the system in markdown format, The markdown should contain the following sections: Overview, System Information, CPU Usage, Memory Usage, Suspicious Processes, Security Recommendations, Conclusions. Get information about each for each of the sections';

    // Set the input for UI purposes
    setInput(temp);

    // Call handleSubmit directly with the default message
    handleSubmit(temp);
  };

  const handleSubmit = async (message) => {
    const userMessage = message || input; // Use the provided message or fallback to input state
    if (!userMessage) return; // Do nothing if the message is empty
    console.log(userMessage)
    const newMessage = { text: userMessage, sender: 'user' };
    setMessages([...messages, newMessage]);
    setInput(''); // Clear input

    try {
      const response = await axios.post('http://localhost:8080/agent_query', { prompt: userMessage });
      const botMessage = { text: response.data.response, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleSubmit(); // Call handleSubmit with the current input
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
      <button className='default_message' onClick={handleDefaultMessage}>Create Accurate Audit reports</button>
      <form onSubmit={handleFormSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default ChatWithLogs;
