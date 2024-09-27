// components/CreateLogs.js
import React, { useState } from 'react';
import axios from 'axios';

function CreateLogs() {
  const [maxCount, setMaxCount] = useState('');
  const [timeInterval, setTimeInterval] = useState('');
  const [logs, setLogs] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8080/create_logs', {
        max_count: maxCount,
        time_interval: timeInterval
      });
      setLogs(response.data.data);
    } catch (error) {
      console.error('Error creating logs:', error);
    }
  };

  return (
    <div>
      <h2>Create Logs</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          value={maxCount}
          onChange={(e) => setMaxCount(e.target.value)}
          placeholder="Max Count"
        />
        <input
          type="number"
          value={timeInterval}
          onChange={(e) => setTimeInterval(e.target.value)}
          placeholder="Time Interval"
        />
        <button type="submit">Create Logs</button>
      </form>
      {logs && (
        <div>
          <h3>Generated Logs:</h3>
          <pre>{logs}</pre>
        </div>
      )}
    </div>
  );
}

export default CreateLogs