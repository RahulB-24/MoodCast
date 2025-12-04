import React, { useState, useEffect } from "react";
import { searchByMood, getGenres } from "../api/api";
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
  const [genres, setGenres] = useState([]);
  const [genreOptions, setGenreOptions] = useState([]);
  const [results, setResults] = useState([]);
  const { playPreview, playingId } = useAudioPreview();

  useEffect(() => {
    async function loadGenres() {
      try {
        const res = await getGenres();
        setGenreOptions(res.genres || []);
      } catch (err) {
        console.error(err);
      }
    }
    loadGenres();
  }, []);

  // Helpers to add tag items
  function addItem(setter, value) {
    if (value.trim() !== "") {
      setter(prev => [...prev, value.trim()]);
    }
  }

  async function runSearch() {
    const payload = {
        mood,
        valence: location.state?.valence || 5.0,
        arousal: location.state?.arousal || 5.0,
        language: language === "none" ? "none" : language,
        genres,
        artist_names: artistNames,
        track_names: trackNames,
        keywords,
    };


    try {
      const res = await searchByMood(payload);
      setResults(res.results || []);
    } catch (err) {
      console.error(err);
      alert("Error searching by mood.");
    }
  }

  return (
    <div className="mood-search-page">
      <h1 className="page-title">Find Music by Mood</h1>

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
          className="input"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="none">Auto Detect</option>
          <option value="en">English</option>
          <option value="ta">Tamil</option>
          <option value="hi">Hindi</option>
          <option value="te">Telugu</option>
        </select>

        <label>Keywords</label>
        <input
          className="input"
          onKeyDown={(e) => {
            if (e.key === "Enter") addItem(setKeywords, e.target.value);
          }}
          placeholder="lofi, acoustic (press Enter)"
        />

        <label>Artists</label>
        <input
          className="input"
          onKeyDown={(e) => {
            if (e.key === "Enter") addItem(setArtistNames, e.target.value);
          }}
          placeholder="Arijit Singh (press Enter)"
        />

        <label>Tracks</label>
        <input
          className="input"
          onKeyDown={(e) => {
            if (e.key === "Enter") addItem(setTrackNames, e.target.value);
          }}
          placeholder="Shape of You (press Enter)"
        />

        <label>Genres</label>
        <select
          className="input"
          onChange={(e) => {
            const g = e.target.value;
            if (g && !genres.includes(g)) {
              setGenres(prev => [...prev, g]);
            }
          }}
        >
          <option value="">Choose genre</option>
          {genreOptions.map((g) => (
            <option key={g} value={g}>{g}</option>
          ))}
        </select>

        <button className="btn btn-primary" onClick={runSearch}>
          Search
        </button>
      </div>

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
  );
}
