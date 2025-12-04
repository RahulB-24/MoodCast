import React from "react";
import { FiPlayCircle } from "react-icons/fi";

export default function TrackCard({ track, onPreview, playing }) {
  return (
    <div className="track-card glass-card">
      <img src={track.image} alt="album" className="track-img" />

      <div className="track-info">
        <h3>{track.name}</h3>
        <p>{track.artist}</p>
      </div>

      <div className="track-actions">
        {track.preview_url ? (
          <button
            className={`preview-btn ${playing ? "playing" : ""}`}
            onClick={() => onPreview(track.preview_url, track.id)}
          >
            <FiPlayCircle size={26} />
          </button>
        ) : (
          <p className="no-preview">No preview</p>
        )}

        <p className="score">Score: {track.score?.toFixed(3)}</p>
      </div>
    </div>
  );
}
