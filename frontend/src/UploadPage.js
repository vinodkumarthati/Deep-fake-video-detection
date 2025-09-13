import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [option, setOption] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file || !option) return;
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("model_name", option); // send selected model

      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (res.ok) {
        // Navigate with backend results
        navigate("/result", {
          state: {
            fileName: data.filename,
            isReal: data.aggregate.mean < 0.5, // mean score threshold
            option,
            analysis: {
              face: Math.round(data.aggregate.mean * 100),
              temporal: Math.round(data.aggregate.median * 100),
              artifact: Math.round(data.aggregate.majority_ratio * 100),
              lipsync: Math.round(data.aggregate.mean * 100), // example reuse
            },
            thumbnails: data.thumbnails.slice(0, 10), // first 10 frames
          },
        });
      } else {
        alert("Error: " + (data.error || "Something went wrong"));
      }
    } catch (err) {
      console.error(err);
      alert("Failed to analyze video.");
    } finally {
      setLoading(false);
    }
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
            <option value="efficientnet_ffpp">efficientnet_ffpp model</option>
            
          </select>
        </div>
        <button
          onClick={handleAnalyze}
          disabled={!file || !option || loading}
          className="btn"
        >
          {loading ? "Analyzing..." : "Analyze Video"}
        </button>
      </div>
    </div>
  );
}

export default UploadPage;
