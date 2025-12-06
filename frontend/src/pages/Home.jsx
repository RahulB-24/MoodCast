import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="home-page page">
      <div className="home-inner container">
        <h1 className="home-title">
          <span className="logo-mood">Mood</span>
          <span className="logo-cast">Cast</span>
        </h1>

        <p className="home-subtitle">
          Discover music that fits your mood. Upload a track to detect mood or search by mood.
        </p>

        <div className="home-cta">
          <Link to="/classify" className="btn btn-primary">Detect Mood</Link>
          <Link to="/mood-search" className="btn btn-secondary">Mood Search</Link>
        </div>
      </div>
    </div>
  );
}
