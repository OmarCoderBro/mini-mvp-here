import os
from pathlib import Path

# Central place for demo thresholds so they're easy to tune live.

# Defaults to the repo-root samples/ directory; override in docker-compose
# since the container's directory depth differs from local dev.
SAMPLES_DIR = Path(
    os.environ.get("SAMPLES_DIR", str(Path(__file__).resolve().parents[2] / "samples"))
)

MAX_BATCH_SIZE = 20
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB per file
MIN_DIMENSION_PX = 32
MAX_DIMENSION_PX = 8000

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

# Below this Laplacian variance, an image is flagged as likely blurry.
BLUR_THRESHOLD = 100.0

# Outside this mean-intensity range (0-255), an image is flagged as too dark/bright.
BRIGHTNESS_MIN = 50.0
BRIGHTNESS_MAX = 200.0
