import React from "react";

export default function MoodResultCard({ mood, valence, arousal, language }) {
  return (
    <div className="mood-card glass-card">
      <h2 className="mood-title">{mood || "No mood detected yet"}</h2>

      <div className="mood-stats">
        <p><strong>Valence:</strong> {valence?.toFixed(2)}</p>
        <p><strong>Arousal:</strong> {arousal?.toFixed(2)}</p>
        <p><strong>Language:</strong> {language}</p>
      </div>
    </div>
  );
}
