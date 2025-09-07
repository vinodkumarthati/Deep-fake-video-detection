import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [option, setOption] = useState("");
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleAnalyze = () => {
    const isReal = Math.random() > 0.5;

    // Fake analysis data
    const analysis = {
      face: 89,
      temporal: 82,
      artifact: 80,
      lipsync: 80,
    };

    navigate("/result", {
      state: { fileName: file?.name, isReal, option, analysis },
    });
  };

  return (
    <div className="container">
      <h1 className="title">Deep Fake Video Detection</h1>
      <p className="subtitle">
        AI-powered analysis to detect manipulated video content with precision
        and reliability
      </p>

      <div className="upload-box">
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <div className="dropdown">
          <label>Select Analysis Type:</label>
          <select
            value={option}
            onChange={(e) => setOption(e.target.value)}
          >
            <option value="">-- Choose an option --</option>
            <option value="basic">Basic Analysis</option>
            <option value="advanced">Advanced Analysis</option>
            <option value="frame">Frame-by-Frame Analysis</option>
          </select>
        </div>
        <button
          onClick={handleAnalyze}
          disabled={!file || !option}
          className="btn"
        >
          Analyze Video
        </button>
      </div>
    </div>
  );
}

export default UploadPage;
