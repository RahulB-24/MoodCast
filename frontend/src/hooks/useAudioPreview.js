import { useRef, useState } from "react";

export default function useAudioPreview() {
  const audioRef = useRef(null);
  const [playingId, setPlayingId] = useState(null);

  function playPreview(url, id) {
    // Create audio element on first use
    if (!audioRef.current) {
      audioRef.current = new Audio();
    }

    const audio = audioRef.current;

    // If clicking the same track → pause it
    if (playingId === id) {
      audio.pause();
      setPlayingId(null);
      return;
    }

    // If switching tracks → stop previous, play new
    audio.pause();
    audio.src = url;
    audio.currentTime = 0;

    audio
      .play()
      .then(() => {
        setPlayingId(id);
      })
      .catch((err) => {
        console.warn("Preview playback failed:", err);
      });

    // When audio ends
    audio.onended = () => {
      setPlayingId(null);
    };
  }

  return {
    playPreview,
    playingId,
  };
}
