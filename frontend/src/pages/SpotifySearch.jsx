import React, { useState } from "react";
import { searchTracks, searchArtists } from "../api/api";
import TrackCard from "../components/TrackCard";
import useAudioPreview from "../hooks/useAudioPreview";

export default function SpotifySearch() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("tracks");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const { playPreview, playingId } = useAudioPreview();

  async function runSearch() {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = mode === "tracks" ? await searchTracks(query) : await searchArtists(query);
      setResults(data.results || data);
    } catch (err) {
      console.error(err);
      alert("Error fetching search results.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="spotify-search-page page">
      <h1 className="page-title">Explore Music</h1>


      <div className="spotify-search-wrapper">
        <div className="spotify-search-form glass-card">
          <input
            className="input"
            placeholder="Search tracks or artists..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && runSearch()}
          />

          <div className="toggle-row">
            <button className={`toggle-btn ${mode === "tracks" ? "active" : ""}`} onClick={() => setMode("tracks")}>Tracks</button>
            <button className={`toggle-btn ${mode === "artists" ? "active" : ""}`} onClick={() => setMode("artists")}>Artists</button>
          </div>

          <div className="search-button-row">
            <button className="btn btn-primary" onClick={runSearch} disabled={loading}>
              {loading ? <span className="vinyl-spinner" aria-hidden /> : "Search"}
            </button>
          </div>
        </div>

        <div className="tracks-results">
          <div className="tracks-grid">
            {results.map((track) => (
              <TrackCard key={track.id || track.name} track={track} onPreview={playPreview} playing={playingId === track.id} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
