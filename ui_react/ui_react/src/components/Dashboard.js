import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [workflows, setWorkflows] = useState([]);
  const [message, setMessage] = useState("");
  const [feedback, setFeedback] = useState({ workflow: "", score: 5, note: "" });

  useEffect(() => {
    axios.get("/api/workflows").then(res => {
      setWorkflows(res.data.workflows);
    });
  }, []);

  const runWorkflow = (name) => {
    setMessage("⏳ Lancement en cours...");
    axios.post(`/api/run/${name}`).then(res => {
      setMessage(res.data.message);
      setFeedback({ ...feedback, workflow: name });
    });
  };

  const submitFeedback = () => {
    axios.post("/api/feedback", feedback).then(res => {
      setMessage(res.data.message);
    });
  };

  return (
    <div>
      <h2>🚀 Workflows disponibles</h2>
      {workflows.map(w => (
        <button key={w} onClick={() => runWorkflow(w)}>▶ {w}</button>
      ))}
      <h3>📝 Donner un feedback</h3>
      <input placeholder="Note" value={feedback.note}
        onChange={e => setFeedback({ ...feedback, note: e.target.value })} />
      <select value={feedback.score}
        onChange={e => setFeedback({ ...feedback, score: e.target.value })}>
        {[1, 2, 3, 4, 5].map(v => <option key={v}>{v}</option>)}
      </select>
      <button onClick={submitFeedback}>Envoyer</button>

      <p>{message}</p>
    </div>
  );
}

export default Dashboard;
