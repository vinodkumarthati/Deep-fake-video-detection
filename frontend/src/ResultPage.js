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

  const { fileName, isReal, option, analysis, thumbnails } = state;

  return (
    <div className="container">
      <h1 className="title">Analysis Result</h1>

      <div className="result-box">
        <p>
          <strong>Video:</strong> {fileName}
        </p>
        <p>
          <strong>Model Used:</strong> {option}
        </p>
        <p>
          <strong>Status:</strong>{" "}
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

        <h2>Frame Samples</h2>
        <div className="frame-grid">
          {thumbnails?.map((thumb, idx) => (
            <div key={idx} className="frame-card">
              <img
                src={`data:image/jpeg;base64,${thumb.img_b64}`}
                alt={`frame-${idx}`}
              />
              <p>Frame {thumb.index}</p>
              <p>Score: {(thumb.score * 100).toFixed(2)}%</p>
            </div>
          ))}
        </div>

        <button className="btn" onClick={() => navigate("/")}>
          Analyze Another
        </button>
      </div>
    </div>
  );
}

export default ResultPage;
