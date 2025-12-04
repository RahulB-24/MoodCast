import React, { useState, useRef } from "react";

export default function FileUpload({ onFileSelected, uploading }) {
  const inputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  function handleFile(file) {
    if (file) onFileSelected(file);
  }

  return (
    <div
      className={`upload-box ${dragOver ? "drag-over" : ""}`}
      onDragEnter={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={(e) => {
        e.preventDefault();
        setDragOver(false);
      }}
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        setDragOver(false);
        if (e.dataTransfer.files.length > 0) {
          handleFile(e.dataTransfer.files[0]);
        }
      }}
    >
      <p>{uploading ? "Uploading..." : "Drag & Drop Audio Here"}</p>
      <p>or</p>

      <button
        className="btn btn-primary"
        onClick={() => inputRef.current?.click()}
        disabled={uploading}
      >
        Choose File
      </button>

      <input
        ref={inputRef}
        type="file"
        accept="audio/*"
        style={{ display: "none" }}
        onChange={(e) => handleFile(e.target.files[0])}
      />
    </div>
  );
}
