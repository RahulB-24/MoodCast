import React, { useState } from "react";
import { searchTracks, searchArtists } from "../api/api";
import TrackCard from "../components/TrackCard";
import useAudioPreview from "../hooks/useAudioPreview";

export default function SpotifySearch() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("tracks");
  const [results, setResults] = useState([]);
  const { playPreview, playingId } = useAudioPreview();

  async function runSearch() {
    if (!query.trim()) return;

    try {
      const data =
        mode === "tracks"
          ? await searchTracks(query)
          : await searchArtists(query);

      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      alert("Error fetching search results.");
    }
  }

  return (
    <div className="spotify-search-page">
      <h1 className="page-title">Explore Spotify</h1>

      <div className="spotify-search-form glass-card">
        <input
          className="input"
          placeholder="Search tracks or artists..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runSearch()}
        />

        <div className="toggle-row">
          <button
            className={`toggle-btn ${mode === "tracks" ? "active" : ""}`}
            onClick={() => setMode("tracks")}
          >
            Tracks
          </button>
          <button
            className={`toggle-btn ${mode === "artists" ? "active" : ""}`}
            onClick={() => setMode("artists")}
          >
            Artists
          </button>
        </div>

        <button className="btn btn-primary" onClick={runSearch}>
          Search
        </button>
      </div>

      <div className="tracks-grid">
        {results.map((track) => (
          <TrackCard
            key={track.id || track.name}
            track={track}
            onPreview={playPreview}
            playing={playingId === track.id}
          />
        ))}
      </div>
    </div>
  );
}
