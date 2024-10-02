# Sentinal AI - Cybersecurity AI Agent

Sentinal AI is a comprehensive cybersecurity agent designed to monitor your system by generating logs, detecting suspicious activities, and creating audit reports. The AI utilizes LSTM models to detect potential threats and provides a chat-based interface for querying logs or audit reports.
This is a complete set of individual tools along with a master agent that is capable of doing them autonomously

## Table of Contents

- [Sentinal AI - Cybersecurity AI Agent](#sentinal-ai---cybersecurity-ai-agent)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
  - [Data Storage](#data-storage)
  - [LSTM Model for Threat Detection](#lstm-model-for-threat-detection)
  - [Chat-based Interface](#chat-based-interface)
  - [Master Agent](#master-agent)
    
## Features

- **Log Generation**: Automatically generates system logs for security monitoring.
- **Audit Report Creation**: Generates audit reports from the logs. If the user does not have audit reports, Cybertron AI will create them from available logs.
- **Suspicious Activity Detection**: Uses LSTM models trained on cybersecurity data to detect anomalies and threats in the logs.
- **Chat-based Interface**: Allows users to query the logs or audit reports through a user-friendly chatbot.

## Prerequisites

To run Cybertron AI, ensure you have the following installed:

- Python 3.7+
- Node.js 14+
- Required Python libraries (install via `requirements.txt`)
- Required Node.js dependencies (install via `npm`)

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/cybertron_ai.git
   cd cybertron_ai```
2. Install the Python dependencies:
    ```bash
    cd Server
    pip install -r requirements.txt
3. Install Node.js dependencies:
    ```bash
    cd cybertron_ai
    npm install
4. Running the Project
    Start the backend: 
    - In the root directory, run:
        ```bash
        cd Server
        python app.py
    - Start the frontend: 
      - In a separate terminal, navigate to the frontend directory and run:
        ```bash
        cd cybertron_ai
        npm run dev
The system will now be running, and you can interact with it through the chat interface.

## Data Storage
Logs and audit reports are stored locally in the Data folder. The system generates logs continuously and updates them in real-time. Audit reports are either generated on-demand or can be created automatically if missing.

## LSTM Model for Threat Detection
The LSTM model is trained to detect various categories of suspicious activities, including but not limited to:

- Reconnaissance
- DoS attacks
- Backdoor exploits
- Worms and malware
- Generic threats
- You can view detected threats through the chat interface or in the generated audit reports.

## Chat-based Interface
The chat-based interface provides a convenient way to interact with the system. You can ask questions such as:

    "Show me today's logs."
    "Generate an audit report for last week's data."
    "What suspicious activities were detected?"

The chatbot will respond with relevant information or actions.

## Master Agent

Finally, a master agent is a multiagent with all of the above tools, that can autonomously do all the above based on the user query.

License
This project is licensed under the MIT License.



