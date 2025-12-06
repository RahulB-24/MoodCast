import React from "react";
import { Link, useLocation } from "react-router-dom";
import { FiMusic } from "react-icons/fi";

export default function Navbar() {
  const { pathname } = useLocation();

  return (
    <nav className="navbar glass-nav">
      <div className="nav-container">
        <Link to="/" className="navbar-logo logo-anim" aria-label="MoodCast home">
          <FiMusic size={22} className="logo-icon" />
          <span className="logo-text">
            <span className="logo-mood">Mood</span>
            <span className="logo-cast">Cast</span>
          </span>
        </Link>

        <div className="navbar-links">
          <Link className={pathname === "/" ? "active" : ""} to="/">Home</Link>
          <Link className={pathname === "/classify" ? "active" : ""} to="/classify">Detect Mood</Link>
          <Link className={pathname === "/mood-search" ? "active" : ""} to="/mood-search">Mood Search</Link>
          <Link className={pathname === "/explore" ? "active" : ""} to="/explore">Explore</Link>
          <Link className={pathname === "/about" ? "active" : ""} to="/about">About</Link>
        </div>
      </div>
    </nav>
  );
}
