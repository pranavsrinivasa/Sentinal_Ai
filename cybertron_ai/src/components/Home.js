import React from 'react';
import './Home.css';
import { ArrowUpRight, Upload, MessageSquare, FileText, Brain } from 'lucide-react';
import { Link } from 'react-router-dom';

const FeatureCard = ({ icon: Icon, title, description, to }) => (
  <div className="feature-card">
    <Link to={to}>
      <Icon className="icon-placeholder" />
    </Link>
    <h3>{title}</h3>
    <p>{description}</p>
  </div>
);

const Home = () => {
  return (
    <div className="home">

      <main>
        <div className="container">
          <div className="hero">
              <div className='intro_title'>
              <div className='logo2'>
              </div>
              
              <h2>The Sentinel Welcomes You</h2>
            </div>
            <p>Your all-in-one solution for file management, log analysis, and AI-powered insights</p>
            <button className="explore-button">Explore Features</button>
          </div>

          <div className="features">
              <FeatureCard
                icon={Upload}
                title="File Upload"
                description="Easily upload and manage your documents securely."
                to = "/file-upload"
              />

            <FeatureCard
              icon={MessageSquare}
              title="Chat with Logs"
              description="Interact with our AI to analyze and understand your logs."
              to = "/chat-with-logs"
            />
            <FeatureCard
              icon={FileText}
              title="Create Logs"
              description="Generate new log data for comprehensive analysis."
              to = "/create-logs"
            />
            <FeatureCard
              icon={Brain}
              title="Master Agent"
              description="Get advanced insights and recommendations from our AI."
              to = "/master-agent"
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;