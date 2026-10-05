# HERE Road Image Quality Checker (MVP)

A small portfolio demo inspired by the HERE Technologies Software Engineer
Intern posting. It flags road images that may be too blurry or poorly lit
before they'd enter a computer-vision pipeline. This is an independent demo,
not a HERE product and not a claim about any team's real system.

## What it does

Upload up to 20 road images. The backend decodes each one with OpenCV and
computes two heuristic signals:

- **Blur** — variance of the Laplacian (low variance suggests a blurry image).
- **Brightness** — mean grayscale intensity (very low/high suggests
  under/over-exposure).

Each image is labeled `Usable` or `Review needed` with reason tags. These are
screening signals, not a guarantee that an image is suitable for a machine
learning pipeline.

## Run with Docker Compose (recommended)

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (health check at `/health`)

Stop with `docker compose down`.

## Run locally without Docker

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend (in a second terminal):

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173.

## Running tests

```bash
cd backend
source .venv/bin/activate
python -m pytest -v
```

All 11 tests cover: blur/brightness scoring on synthetic images, per-file
error handling for invalid images, batch-size and file-size limits, and the
documented API response fields.

## Limitations

- Blur and brightness thresholds are simple heuristics, tuned for a demo —
  not validated against real-world road imagery or any ML suitability
  criteria.
- No images or results are stored; each request is analyzed and discarded.
- Scoped intentionally: no accounts, no database, no cloud deployment.
