import React, { useState, useRef } from "react";

export default function FileUpload({ onFileSelected, uploading }) {
  const inputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  function handleFile(file) {
    if (file) onFileSelected(file);
  }

  return (
    <div className="upload-area">
      <div
        className={`upload-box ${dragOver ? "drag-over" : ""}`}
        onDragEnter={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={(e) => { e.preventDefault(); setDragOver(false); }}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
          }
        }}
      >
        {!uploading ? (
          <>
            <p className="upload-title">Drag & Drop Audio Here</p>
            <p className="upload-sub">or</p>
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
          </>
        ) : (
          <div className="uploading-state">
            <div className="upload-row">
              <div className="folder left-folder">📁</div>

              <div className="notes-rail" aria-hidden>
                <span className="note n1">♪</span>
                <span className="note n2">♫</span>
                <span className="note n3">♬</span>
                <span className="note n4">♪</span>
              </div>

              <div className="folder right-folder">📂</div>
            </div>

            <p className="uploading-text">Uploading... Converting & detecting mood</p>
          </div>
        )}
      </div>
    </div>
  );
}
