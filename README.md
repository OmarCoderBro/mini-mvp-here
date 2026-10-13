# Road Image Quality Checker MVP - Omar Shatat

this MVP is a synthetic road image processor / analyzer using React → FastAPI → OpenCV.

You can select up to 20 road images and each is labeled "Usable" or "Review needed" based on simple blur and brightness checks, before it would enter a computer-vision pipeline, using basic blur and brightness processing using OpenCV. Just a quick reminder, these are screening heuristics, not a guarantee that the image that displays "usable" suits a real ML pipeline.


## Quick Architecture Sanity Check

React page --(upload images)--> FastAPI /analyze --> OpenCV scoring --> Usable / Review needed

- **FastAPI** (`POST /analyze`, `GET /health`) validates file type, size, and batch limit, then analyzes each image independently so one bad file doesn't fail the batch.
- **OpenCV** decodes each image and computes two scores: blur (variance of the Laplacian) and brightness (mean grayscale).
- **Thresholds** in `backend/app/config.py` turn the scores into labels with reasons ("likely blurry", "too dark", "too bright").
- **React** is a single page for uploading images and viewing results. Sample photos are in `samples/`.

## Run locally

Requires Python 3 and Node.js.

**1. start API** (one terminal, from `backend/`)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**2. start frontend** (second terminal, from `frontend/`)
```bash
cd frontend
npm install
npm run dev
```

Open the URL React outputs (normally http://localhost:5173), then upload images from `samples/`.

**Stop:** Ctrl+C both terminals.

## Troubleshooting Tips for this MVP
- **If Port 8000 is still in use:**
`kill $(lsof -nP -tiTCP:8000 -sTCP:LISTEN)`.
- **To check if its running on there:**
`lsof -nP -iTCP:5173 -sTCP:LISTEN`.

- **Vite uses a different port (e.g. 5174):** the API only allows `http://localhost:5173` for CORS. Stop whatever holds 5173 and restart the frontend so it takes that port.
- **Page can't reach the API:** confirm http://localhost:8000/health responds.
