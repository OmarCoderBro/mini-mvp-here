from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .analyzer import DecodeError, analyze_image
from .schemas import AnalyzeResponse, HealthResponse, ImageError, ImageResult

app = FastAPI(title="HERE Road Image Quality Checker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(files: list[UploadFile] = File(...)) -> AnalyzeResponse:
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No files provided")
    if len(files) > config.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch exceeds limit of {config.MAX_BATCH_SIZE} images",
        )

    results: list[ImageResult] = []
    errors: list[ImageError] = []

    for upload in files:
        filename = upload.filename or "unnamed"

        if upload.content_type not in config.ALLOWED_CONTENT_TYPES:
            errors.append(ImageError(filename=filename, error="Unsupported file type"))
            continue

        data = await upload.read()
        if len(data) > config.MAX_FILE_SIZE_BYTES:
            errors.append(ImageError(filename=filename, error="File too large"))
            continue

        try:
            analysis = analyze_image(data)
        except DecodeError as exc:
            errors.append(ImageError(filename=filename, error=str(exc)))
            continue
        except Exception:
            errors.append(ImageError(filename=filename, error="Could not process image"))
            continue

        results.append(ImageResult(filename=filename, **analysis))

    return AnalyzeResponse(results=results, errors=errors)
