// components/Home.js
import React from 'react';

function Home() {
  return (
    <div>
      <h1>Welcome to the Cybersecurity Application</h1>
      <p>This application allows you to upload files, chat with logs, create logs, and interact with a master agent.</p>
      <ul>
        <li>Use the File Upload page to upload your documents.</li>
        <li>Chat with Logs allows you to interact with the main agent and analyze your logs.</li>
        <li>Create Logs helps you generate new log data for analysis.</li>
        <li>The Master Agent provides advanced insights and recommendations.</li>
      </ul>
    </div>
  );
}

export default Home