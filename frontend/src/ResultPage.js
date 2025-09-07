import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

function ResultPage() {
  const { state } = useLocation();
  const navigate = useNavigate();

  if (!state) {
    return (
      <div className="container">
        <p>No analysis data found.</p>
        <button className="btn" onClick={() => navigate("/")}>
          Go Back
        </button>
      </div>
    );
  }

  const { fileName, isReal, option, analysis } = state;

  return (
    <div className="container">
      <h1 className="title">Analysis Result</h1>

      <div className="result-box">
        <p><strong>Video:</strong> {fileName}</p>
        <p><strong>Analysis Type:</strong> {option}</p>
        <p>
          Status:{" "}
          <span style={{ color: isReal ? "limegreen" : "red" }}>
            {isReal ? "Likely Authentic" : "Likely Fake"}
          </span>
        </p>

        <h2>Detailed Analysis</h2>
        <div className="bar">
          <label>Face Analysis</label>
          <progress value={analysis.face} max="100"></progress>
          <span>{analysis.face}%</span>
        </div>
        <div className="bar">
          <label>Temporal Consistency</label>
          <progress value={analysis.temporal} max="100"></progress>
          <span>{analysis.temporal}%</span>
        </div>
        <div className="bar">
          <label>Artifact Detection</label>
          <progress value={analysis.artifact} max="100"></progress>
          <span>{analysis.artifact}%</span>
        </div>
        <div className="bar">
          <label>Lip Sync Analysis</label>
          <progress value={analysis.lipsync} max="100"></progress>
          <span>{analysis.lipsync}%</span>
        </div>

        <button className="btn" onClick={() => navigate("/")}>
          Analyze Another
        </button>
      </div>
    </div>
  );
}

export default ResultPage;
