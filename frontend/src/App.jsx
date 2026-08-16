import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api";
const SERVER_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // =====================================================
  // FILE SELECTION
  // =====================================================

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setResult(null);
    setAnalysis(null);
    setError("");

    if (selectedFile.type.startsWith("image/")) {
      const url = URL.createObjectURL(selectedFile);
      setPreview(url);
    } else {
      setPreview(null);
    }
  };

  // =====================================================
  // IMAGE INSPECTION
  // =====================================================

  const inspectImage = async () => {
    if (!file) {
      setError("Please select an image.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setAnalysis(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${API_URL}/inspect/image`,
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Image inspection failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // VIDEO INSPECTION
  // =====================================================

  const inspectVideo = async () => {
    if (!file) {
      setError("Please select a video.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setAnalysis(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${API_URL}/inspect/video`,
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Video inspection failed."
        );
      }

      console.log(
        "VIDEO INSPECTION RESULT:",
        data
      );

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // AI QUALITY ANALYSIS
  // =====================================================

  const analyzeDefect = async (
    defect,
    confidence
  ) => {
    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const response = await fetch(
        `${API_URL}/agent/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            defect: defect,
            confidence: confidence
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "AI analysis failed."
        );
      }

      console.log(
        "AI ANALYSIS:",
        data
      );

      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // IMAGE DETECTIONS
  // =====================================================

  const imageDetections =
    result?.detections || [];

  // =====================================================
  // VIDEO FRAMES
  // =====================================================

  const videoFrames =
    result?.frames || [];

  // =====================================================
  // SELECT ONLY 2-3 BEST FRAMES PER DEFECT
  //
  // If video contains:
  //   scratch + dent
  //
  // the UI will show:
  //   2-3 scratch frames
  //   2-3 dent frames
  //
  // instead of showing every detected frame.
  // =====================================================

  const getRepresentativeFrames = () => {
    if (!videoFrames.length) {
      return [];
    }

    const framesByDefect = {};

    // -----------------------------------------------------
    // Group frames according to defect
    // -----------------------------------------------------

    videoFrames.forEach((frameData) => {
      if (!frameData.detections) {
        return;
      }

      frameData.detections.forEach((detection) => {
        const defect = detection.defect;

        if (!framesByDefect[defect]) {
          framesByDefect[defect] = [];
        }

        framesByDefect[defect].push({
          ...frameData,
          selectedDetection: detection
        });
      });
    });

    const selectedFrames = [];

    // -----------------------------------------------------
    // Select maximum 3 frames for each defect
    // -----------------------------------------------------

    Object.keys(framesByDefect).forEach((defect) => {
      const frames = framesByDefect[defect];

      // Highest-confidence frames first
      frames.sort(
        (a, b) =>
          b.selectedDetection.confidence -
          a.selectedDetection.confidence
      );

      // Remove duplicate frame numbers
      const uniqueFrames = [];

      const usedFrames = new Set();

      for (const frame of frames) {
        if (!usedFrames.has(frame.frame)) {
          usedFrames.add(frame.frame);
          uniqueFrames.push(frame);
        }
      }

      // Only show top 3 frames for this defect
      selectedFrames.push(
        ...uniqueFrames.slice(0, 3)
      );
    });

    return selectedFrames;
  };

  const representativeFrames =
    getRepresentativeFrames();

  // =====================================================
  // TOTAL DEFECT COUNT
  // =====================================================

  const defectCount =
    result?.defect_count ??
    result?.count ??
    0;

  // =====================================================
  // RENDER
  // =====================================================

  return (
    <div className="app">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div>

          <h1>
            AI Automotive Defect
            Inspection
          </h1>

          <p>
            YOLO11 + RAG + AI
            Quality Analysis
          </p>

        </div>

        <div className="status">
          ● System Ready
        </div>

      </header>

      <main className="container">

        {/* =================================================
            UPLOAD
        ================================================= */}

        <section className="upload-card">

          <h2>
            Vehicle Inspection
          </h2>

          <p className="subtitle">
            Upload an automotive
            image or inspection video.
          </p>

          <label className="file-input">

            <input
              type="file"
              accept="image/*,video/*"
              onChange={handleFileChange}
            />

            <span>
              Choose Image / Video
            </span>

          </label>

          {file && (
            <div className="file-name">

              Selected:

              <strong>
                {file.name}
              </strong>

            </div>
          )}

          <div className="buttons">

            <button
              onClick={inspectImage}
              disabled={
                loading ||
                !file ||
                !file.type.startsWith("image/")
              }
            >
              Inspect Image
            </button>

            <button
              onClick={inspectVideo}
              disabled={
                loading ||
                !file ||
                !file.type.startsWith("video/")
              }
            >
              Analyze Video
            </button>

          </div>

          {loading && (
            <div className="loading">
              Processing inspection...
            </div>
          )}

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>

        {/* =================================================
            INPUT IMAGE PREVIEW
        ================================================= */}

        {preview && !result && (

          <section className="image-card">

            <h2>
              Input Image
            </h2>

            <img
              src={preview}
              alt="Vehicle"
            />

          </section>

        )}

        {/* =================================================
            INSPECTION RESULTS
        ================================================= */}

        {result && (

          <section className="results">

            <div className="section-title">

              <div>

                <h2>
                  Inspection Results
                </h2>

                <p>
                  YOLO11 detection output
                </p>

              </div>

              <div className="defect-count">

                {defectCount} Defects

              </div>

            </div>

           {/* =================================================
    IMAGE RESULT
================================================= */}

{result.image && (

  <div className="image-card">

    <h2>
      Detected Image
    </h2>

    <div
      style={{
        width: "100%",
        maxWidth: "900px",
        margin: "0 auto"
      }}
    >

      <img
        src={
          result.image.startsWith("data:image")
            ? result.image
            : result.image.startsWith("http")
              ? result.image
              : `${SERVER_URL}${result.image}`
        }
        alt="Detected automotive defects"
        style={{
          width: "100%",
          height: "auto",
          display: "block",
          borderRadius: "8px"
        }}
      />

    </div>

  </div>

)}

            {/* =================================================
                VIDEO RESULTS
            ================================================= */}

            {representativeFrames.length > 0 && (

              <div className="video-results">

                <h2>
                  Representative Defect Frames
                </h2>

                <p className="subtitle">
                  Showing the highest-confidence
                  detected frames only.
                </p>

                <div className="detection-grid">

                  {representativeFrames.map(
                    (frameData, frameIndex) => (

                      <div
                        className="image-card"
                        key={`${frameData.frame}-${frameIndex}`}
                      >

                        <h3>
                          Frame {frameData.frame}
                        </h3>

                        <img
                          src={
                            frameData.image.startsWith("http")
                              ? frameData.image
                              : `${SERVER_URL}${frameData.image}`
                          }
                          alt={
                            `Detected ${frameData.selectedDetection.defect}`
                          }
                        />

                        <div className="detection-card">

                          <h3>
                            {
                              frameData.selectedDetection
                                .defect
                            }
                          </h3>

                          <div className="confidence">

                            <span>
                              Confidence
                            </span>

                            <strong>
                              {
                                frameData.selectedDetection
                                  .confidence_percent ??
                                (
                                  frameData.selectedDetection
                                    .confidence * 100
                                ).toFixed(2)
                              }%
                            </strong>

                          </div>

                        </div>

                      </div>

                    )
                  )}

                </div>

              </div>

            )}

            {/* =================================================
                NO VIDEO DETECTIONS
            ================================================= */}

            {result &&
              result.frames &&
              result.frames.length === 0 &&
              !imageDetections.length && (

              <div className="error">
                No defects were detected
                in the processed video frames.
              </div>

            )}

            {/* =================================================
                SUMMARY
            ================================================= */}

            {result.summary &&
              result.summary.length > 0 && (

              <div>

                <h2>
                  Defect Summary
                </h2>

                <p className="subtitle">
                  Overall defect detection summary
                  for the inspection.
                </p>

                <div className="detection-grid">

                  {result.summary.map(
                    (detection, index) => (

                      <div
                        className="detection-card"
                        key={index}
                      >

                        <h3>
                          {detection.defect}
                        </h3>

                        <div className="confidence">

                          <span>
                            Highest Confidence
                          </span>

                          <strong>
                            {
                              detection.confidence_percent ??
                              (
                                detection.highest_confidence *
                                100
                              ).toFixed(2)
                            }%
                          </strong>

                        </div>

                        <p>

                          Detected in{" "}

                          <strong>
                            {detection.detections}
                          </strong>

                          {" "}processed frames.

                        </p>

                        <button
                          onClick={() =>
                            analyzeDefect(
                              detection.defect,
                              detection.highest_confidence
                            )
                          }
                        >
                          AI Analysis
                        </button>

                      </div>

                    )
                  )}

                </div>

              </div>

            )}

          </section>

        )}

        {/* =================================================
            AI QUALITY ANALYSIS
        ================================================= */}

        {analysis && (

          <section className="analysis-card">

            <div className="section-title">

              <div>

                <h2>
                  AI Quality Analysis
                </h2>

                <p>
                  RAG-grounded automotive
                  quality analysis
                </p>

              </div>

              <div className="ai-badge">
                AI AGENT
              </div>

            </div>

            <div className="analysis-content">
              {analysis.analysis}
            </div>

            {/* =================================================
                RAG SOURCES
            ================================================= */}

            {(analysis.sources ||
              analysis.knowledge_sources) && (

              <div className="sources">

                <h3>
                  Retrieved Knowledge
                </h3>

                {(
                  analysis.sources ||
                  analysis.knowledge_sources ||
                  []
                ).map(
                  (source, index) => (

                    <div
                      key={index}
                      className="source"
                    >
                      {source}
                    </div>

                  )
                )}

              </div>

            )}

          </section>

        )}

      </main>

      <footer>

        AI-Powered Automotive
        Defect Inspection &
        Quality Analysis System

      </footer>

    </div>
  );
}

export default App;