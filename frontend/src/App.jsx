import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ParticleBackground from "./components/ParticleBackground";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Classify from "./pages/Classify";
import MoodSearch from "./pages/MoodSearch";
import SpotifySearch from "./pages/SpotifySearch";
import About from "./pages/About";
import "./styles/theme.css";
import "./styles/components.css";

export default function App() {
  return (
    <BrowserRouter>
      <ParticleBackground />
      <div className="app-shell">
        <Navbar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/classify" element={<Classify />} />
            <Route path="/mood-search" element={<MoodSearch />} />
            <Route path="/explore" element={<SpotifySearch />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
