import { useMemo, useState } from "react";
import type { AnalyzeResponse } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";
const MAX_IMAGES = 20;

export default function App() {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<AnalyzeResponse | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  const previews = useMemo(
    () => files.map((file) => ({ file, url: URL.createObjectURL(file) })),
    [files]
  );

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const selected = Array.from(event.target.files ?? []).slice(0, MAX_IMAGES);
    setFiles(selected);
    setResponse(null);
    setApiError(null);
  }

  async function handleAnalyze() {
    setLoading(true);
    setApiError(null);
    setResponse(null);

    try {
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));

      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail ?? `Request failed (${res.status})`);
      }

      const data: AnalyzeResponse = await res.json();
      setResponse(data);
    } catch (err) {
      setApiError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  }

  const previewUrlByName = useMemo(() => {
    const map = new Map<string, string>();
    previews.forEach(({ file, url }) => map.set(file.name, url));
    return map;
  }, [previews]);

  return (
    <div className="app">
      <h1>HERE Road Image Quality Checker</h1>
      <p className="subtitle">
        Upload a batch of road images to screen for blur and lighting issues.
      </p>

      <div className="disclaimer">
        These checks are heuristic screening signals (Laplacian blur variance and
        mean brightness), not proof that an image is suitable for a machine
        learning pipeline. This is an independent demo, not a HERE product.
      </div>

      <div className="controls">
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          onChange={handleFileChange}
        />
        <button onClick={handleAnalyze} disabled={files.length === 0 || loading}>
          {loading ? "Analyzing..." : "Analyze images"}
        </button>
        <span className="count-note">
          {files.length} / {MAX_IMAGES} selected
        </span>
      </div>

      {apiError && <div className="error-banner">Error: {apiError}</div>}

      {!response && !loading && files.length === 0 && (
        <div className="empty-state">Select up to {MAX_IMAGES} images to get started.</div>
      )}

      {response && (
        <div className="results">
          {response.results.map((result) => (
            <div className="card" key={result.filename}>
              {previewUrlByName.get(result.filename) && (
                <img src={previewUrlByName.get(result.filename)} alt={result.filename} />
              )}
              <div className="card-body">
                <div className="filename">{result.filename}</div>
                <span className={`status ${result.status}`}>
                  {result.status === "usable" ? "Usable" : "Review needed"}
                </span>
                <p className="metrics">
                  {result.width}x{result.height} · blur {result.blur_score} · brightness{" "}
                  {result.brightness_score}
                </p>
                {result.reasons.length > 0 && (
                  <p className="reasons">{result.reasons.join(", ")}</p>
                )}
              </div>
            </div>
          ))}

          {response.errors.map((err) => (
            <div className="card error" key={err.filename}>
              <div className="card-body">
                <div className="filename">{err.filename}</div>
                <p className="reasons">{err.error}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
