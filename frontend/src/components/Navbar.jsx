import React from "react";
import { Link, useLocation } from "react-router-dom";
import { FiMusic } from "react-icons/fi";

export default function Navbar() {
  const { pathname } = useLocation();

  return (
    <nav className="navbar glass-nav">
      <div className="navbar-inner">
        <Link to="/" className="navbar-logo">
          <FiMusic size={22} />
          <span>MoodCast</span>
        </Link>

        <div className="navbar-links">
          <Link className={pathname === "/" ? "active" : ""} to="/">Home</Link>
          <Link className={pathname === "/classify" ? "active" : ""} to="/classify">Detect Mood</Link>
          <Link className={pathname === "/mood-search" ? "active" : ""} to="/mood-search">Mood Search</Link>
          <Link className={pathname === "/explore" ? "active" : ""} to="/explore">Explore</Link>
          <Link className={pathname === "/connect" ? "active" : ""} to="/connect">Connect</Link>
        </div>
      </div>
    </nav>
  );
}
