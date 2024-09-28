// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import { ArrowUpRight, Upload, MessageSquare, FileText, Brain } from 'lucide-react';
import FileUpload from './components/FileUpload';
import ChatWithLogs from './components/ChatWithLogs';
import CreateLogs from './components/CreateLogs';
import MasterAgent from './components/MasterAgent';
import Home from './components/Home';
import './App.css';
import logo from './result-BJ6Bh87MCu.webp'




function App() {

  const FeatureCard = ({ icon: Icon,to }) => (
    <Link to={to}>
      <Icon className="icon-placeholder" />
    </Link>
  );
  

  return (
    <Router>
      <div className='home'>
        <nav>
          <Link to='/'>
            <div className='logo'>
            </div>
          </Link>
          <ul>
            {/* <li><Link to="/">Home</Link></li>
            <li><Link to="/file-upload">File Upload</Link></li>
            <li><Link to="/chat-with-logs">Chat with Logs</Link></li>
            <li><Link to="/create-logs">Create Logs</Link></li>
            <li><Link to="/master-agent">Master Agent</Link></li> */}
            <li>
            <FeatureCard
                icon={Upload}
                to = "/file-upload"
              />
            </li>

            <li>
            <FeatureCard
              icon={MessageSquare}
              to = "/chat-with-logs"
            />
            </li>
            <li>  
            <FeatureCard
              icon={FileText}
              to = "/create-logs"
            />
            </li>
            <li>
            <FeatureCard
              icon={Brain}
              to = "/master-agent"
            />
            </li>
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