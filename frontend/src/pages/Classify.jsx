import React, { useState } from "react";
import FileUpload from "../components/FileUpload";
import MoodResultCard from "../components/MoodResultCard";
import { uploadAudio } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Classify() {
  const [result, setResult] = useState(null);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  async function handleFile(file) {
    setUploading(true);
    try {
      const response = await uploadAudio(file, (evt) => {
        // optional progress
      });
      setResult(response);
    } catch (err) {
      console.error("Upload error", err);
      alert("Error uploading audio.");
    } finally {
      setUploading(false);
    }
  }

  function goToMoodSearch() {
    navigate("/mood-search", {
      state: {
        mood: result?.mood,
        valence: result?.valence,
        arousal: result?.arousal,
        language: result?.language,
      },
    });
  }

  return (
    <div className="classify-page page">
      <h1 className="page-title">Detect Mood from Audio</h1>

      <div className="classify-grid container">
        <div className="classify-left">
          <div className="classify-card glass-card">
            <h2 className="card-title">Upload a track</h2>
            <p className="card-sub">We analyze valence, arousal and mood.</p>
            <FileUpload onFileSelected={handleFile} uploading={uploading} />
          </div>
        </div>

        <div className="classify-right">
          <div className="classify-card glass-card">
            <h2 className="card-title">Result</h2>
            {!result ? (
              <p className="muted">No result yet. Upload a file to see mood.</p>
            ) : (
              <>
                <MoodResultCard
                  mood={result.mood}
                  valence={result.valence}
                  arousal={result.arousal}
                  language={result.language}
                />
                <div style={{ textAlign: "center", marginTop: 12 }}>
                  <button className="btn btn-primary" onClick={goToMoodSearch}>
                    Find songs for this mood
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
