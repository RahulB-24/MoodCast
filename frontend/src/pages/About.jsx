import React from "react";
import { motion } from "framer-motion";
import { FaGithub, FaLinkedin, FaEnvelope } from "react-icons/fa";

export default function About() {
  return (
    <div className="about-page">
      {/* PAGE TITLE */}
      <motion.h1
        className="about-title"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <span className="highlight-warm">About</span>{" "}
        <span className="highlight-cool">MoodCast</span>
      </motion.h1>

      <div className="about-container">

        {/* ABOUT PROJECT */}
        <motion.section
          className="about-section"
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <h2 className="section-header">About the Project</h2>

          <p>
            <strong>MoodCast</strong> is an intelligent music exploration system that combines
            machine learning, audio analysis, and Spotify search pipelines to create
            personalized music discovery results.
          </p>

          <p>
            The system uses a custom-trained valence–arousal regression model built using
            the DEAM dataset and Librosa features, along with Faster-Whisper language
            detection. Based on the detected mood and language cues, MoodCast generates
            optimized search queries to retrieve high-quality Spotify tracks.
          </p>

          <p>
            The platform seamlessly integrates a FastAPI backend, ML pipeline, and a modern
            React-based UI with animations, smooth transitions, and an intuitive music-themed
            experience.
          </p>
          <div className="repo-source-wrapper">
          <a 
            href="https://github.com/RahulB-24/MoodCast"
            target="_blank"
            rel="noreferrer"
            className="repo-source-link"
          >
            <FaGithub size={32} className="repo-github-icon" />
            <span>Source Code</span>
          </a>
        </div>



        </motion.section>

        {/* ABOUT ME */}
        <motion.section
          className="about-section"
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h2 className="section-header">About Me</h2>

          <p>
            I’m <strong>Rahul Balachandar</strong>, a 3rd-year Computer Science and Engineering
            student (AI/ML specialization) at VIT Chennai. I’m passionate about applied machine
            learning, full-stack engineering, and building impactful real-world AI systems. I have built multiple projects
            involving deep learning, NLP, computer vision, and web development. Check them out on my GitHub!
          </p>

        </motion.section>

        {/* LINKS */}
        <motion.section
          className="about-section contact-section"
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <h2 className="section-header">Connect With Me</h2>

          <div className="contact-links">
            <a href="https://github.com/" target="_blank" rel="noreferrer">
              <FaGithub size={28} /> GitHub
            </a>

            <a href="https://linkedin.com/in/" target="_blank" rel="noreferrer">
              <FaLinkedin size={28} /> LinkedIn
            </a>
          </div>
        </motion.section>
      </div>
    </div>
  );
}
