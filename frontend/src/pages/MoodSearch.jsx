import React, { useState } from "react";
import { searchByMood } from "../api/api";
import TrackCard from "../components/TrackCard";
import useAudioPreview from "../hooks/useAudioPreview";
import { useLocation } from "react-router-dom";

export default function MoodSearch() {
  const location = useLocation();
  const [mood, setMood] = useState(location.state?.mood || "");
  const [language, setLanguage] = useState(location.state?.language || "none");
  const [keywords, setKeywords] = useState([]);
  const [artistNames, setArtistNames] = useState([]);
  const [trackNames, setTrackNames] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const { playPreview, playingId } = useAudioPreview();

  function addItem(setter, value) {
    if (value.trim() !== "") setter((prev) => [...prev, value.trim()]);
  }

  async function runSearch() {
    setLoading(true);
    setResults([]);
    const payload = {
      mood,
      valence: location.state?.valence || 5.0,
      arousal: location.state?.arousal || 5.0,
      language: language === "none" ? "none" : language,
      genres: [],
      artist_names: artistNames,
      track_names: trackNames,
      keywords,
    };

    try {
      const res = await searchByMood(payload);
      const out = res.results || res;
      setResults(out);
    } catch (err) {
      console.error(err);
      alert("Error searching by mood.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mood-search-page page">
      <h1 className="page-title">Find Music by Mood</h1>

      <div className="mood-search-wrapper">
        <div className="mood-search-form glass-card">
          <label>Mood</label>
          <input
            className="input"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            placeholder="happy energetic, sad calm..."
          />

          <label>Language</label>
          <select
            className="input language-select"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            <option value="none">Auto Detect</option>
            <option value="en">English</option>
            <option value="ta">Tamil</option>
            <option value="hi">Hindi</option>
            <option value="te">Telugu</option>
          </select>

          <label>Keywords (press Enter)</label>
          <input
            className="input"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                addItem(setKeywords, e.target.value);
                e.target.value = "";
              }
            }}
            placeholder="lofi, acoustic (press Enter)"
          />

          <label>Artists (press Enter)</label>
          <input
            className="input"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                addItem(setArtistNames, e.target.value);
                e.target.value = "";
              }
            }}
            placeholder="Arijit Singh (press Enter)"
          />

          <label>Tracks (press Enter)</label>
          <input
            className="input"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                addItem(setTrackNames, e.target.value);
                e.target.value = "";
              }
            }}
            placeholder="Shape of You (press Enter)"
          />

          <div className="chip-row">
            {keywords.map((k, i) => <span key={i} className="chip">{k}</span>)}
            {artistNames.map((k, i) => <span key={i} className="chip">{k}</span>)}
            {trackNames.map((k, i) => <span key={i} className="chip">{k}</span>)}
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
              <TrackCard
                key={track.id}
                track={track}
                onPreview={playPreview}
                playing={playingId === track.id}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
