from fastapi.testclient import TestClient

from app import config
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_returns_documented_fields(normal_image_bytes):
    response = client.post(
        "/analyze",
        files={"files": ("normal.png", normal_image_bytes, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["results"]) == 1
    result = body["results"][0]
    for field in ("filename", "width", "height", "blur_score", "brightness_score", "status", "reasons"):
        assert field in result


def test_analyze_invalid_file_is_per_file_error(normal_image_bytes):
    response = client.post(
        "/analyze",
        files=[
            ("files", ("good.png", normal_image_bytes, "image/png")),
            ("files", ("bad.png", b"garbage", "image/png")),
        ],
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["results"]) == 1
    assert len(body["errors"]) == 1
    assert body["errors"][0]["filename"] == "bad.png"


def test_batch_limit_enforced(normal_image_bytes):
    files = [
        ("files", (f"img{i}.png", normal_image_bytes, "image/png"))
        for i in range(config.MAX_BATCH_SIZE + 1)
    ]
    response = client.post("/analyze", files=files)
    assert response.status_code == 400


def test_file_too_large_rejected():
    oversized = b"0" * (config.MAX_FILE_SIZE_BYTES + 1)
    response = client.post(
        "/analyze",
        files={"files": ("big.png", oversized, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["errors"][0]["error"] == "File too large"


def test_unsupported_content_type_rejected(normal_image_bytes):
    response = client.post(
        "/analyze",
        files={"files": ("file.gif", normal_image_bytes, "image/gif")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["errors"][0]["error"] == "Unsupported file type"
