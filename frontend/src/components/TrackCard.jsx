import React from "react";
import { FiPlayCircle } from "react-icons/fi";

export default function TrackCard({ track, onPreview, playing }) {
  const title = track.name || "";
  const artist = track.artist || "";
  const query = encodeURIComponent(`${title} ${artist}`);
  const youtubeUrl = `https://www.youtube.com/results?search_query=${query}`;

  return (
    <a
      className="track-link"
      href={youtubeUrl}
      target="_blank"
      rel="noopener noreferrer"
      onClick={(e) => {
        // if clicking preview button, prevent opening new tab
        const tgt = e.target;
        if (tgt && (tgt.tagName === "BUTTON" || tgt.closest && tgt.closest("button"))) {
          e.preventDefault();
        }
      }}
    >
      <div className="track-card glass-card" role="button" tabIndex={0}>
        <img src={track.image} alt="album" className="track-img" />

        <div className="track-info">
          <h3>{track.name}</h3>
          <p>{track.artist}</p>
        </div>

        <div className="track-actions">
          {track.preview_url ? (
            <button
              className={`preview-btn ${playing ? "playing" : ""}`}
              onClick={(ev) => {
                ev.preventDefault();
                ev.stopPropagation();
                onPreview(track.preview_url, track.id);
              }}
            >
              <FiPlayCircle size={26} />
            </button>
          ) : (
            <p className="no-preview">No preview</p>
          )}

          <p className="score">Score: {track.score?.toFixed(3)}</p>
        </div>
      </div>
    </a>
  );
}
