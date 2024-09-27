// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import FileUpload from './components/FileUpload';
import ChatWithLogs from './components/ChatWithLogs';
import CreateLogs from './components/CreateLogs';
import MasterAgent from './components/MasterAgent';
import Home from './components/Home';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/file-upload">File Upload</Link></li>
            <li><Link to="/chat-with-logs">Chat with Logs</Link></li>
            <li><Link to="/create-logs">Create Logs</Link></li>
            <li><Link to="/master-agent">Master Agent</Link></li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/file-upload" element={<FileUpload />} />
          <Route path="/chat-with-logs" element={<ChatWithLogs />} />
          <Route path="/create-logs" element={<CreateLogs />} />
          <Route path="/master-agent" element={<MasterAgent />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App