import React, { useState } from "react";
import { getAuthUrl } from "../api/api";

export default function ConnectSpotify() {
  const [authUrl, setAuthUrl] = useState("");

  async function fetchUrl() {
    try {
      const res = await getAuthUrl();
      setAuthUrl(res.auth_url);
      window.location.href = res.auth_url;
    } catch (err) {
      console.error(err);
      alert("Error fetching Spotify auth URL");
    }
  }

  return (
    <div className="connect-page">
      <h1 className="page-title">Connect Your Spotify</h1>

      <p className="connect-desc">
        Login with Spotify to enable playlist creation and personalized features.
      </p>

      <button onClick={fetchUrl} className="btn btn-primary">
        Connect Spotify
      </button>

      {authUrl && (
        <p className="auth-url">
          Redirecting… If not redirected, click  
          <a href={authUrl} target="_blank"> here </a>.
        </p>
      )}
    </div>
  );
}
