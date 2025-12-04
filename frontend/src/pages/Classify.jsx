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
      const response = await uploadAudio(file);
      setResult(response);
    } catch (err) {
      console.error(err);
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
            language: result?.language, // backend returns "language"
        },
    });
  }

  return (
    <div className="classify-page">
      <h1 className="page-title">Detect Mood from Audio</h1>

      <FileUpload onFileSelected={handleFile} uploading={uploading} />

      {result && (
        <div className="classify-result-section">
          <MoodResultCard
            mood={result.mood}
            valence={result.valence}
            arousal={result.arousal}
            language={result.detected_language}
          />

          <button onClick={goToMoodSearch} className="btn btn-primary">
            Search Music for this Mood
          </button>
        </div>
      )}
    </div>
  );
}
