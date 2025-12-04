import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <div className="home-page">
      <motion.h1
        className="home-title neon-text"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        MoodCast
      </motion.h1>

      <motion.p
        className="home-subtitle"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        Discover music that matches your mood.
      </motion.p>

      <motion.div
        className="home-buttons"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        <Link to="/classify" className="btn btn-primary">
          Detect Mood
        </Link>

        <Link to="/mood-search" className="btn btn-secondary">
          Mood Search
        </Link>
      </motion.div>
    </div>
  );
}
