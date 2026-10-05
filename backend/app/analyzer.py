import cv2
import numpy as np

from . import config


class DecodeError(Exception):
    pass


def decode_image(data: bytes) -> np.ndarray:
    array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise DecodeError("Could not decode image")
    return image


def blur_score(gray: np.ndarray) -> float:
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def brightness_score(gray: np.ndarray) -> float:
    return float(gray.mean())


def classify(blur: float, brightness: float) -> tuple[str, list[str]]:
    reasons = []
    if blur < config.BLUR_THRESHOLD:
        reasons.append("likely blurry")
    if brightness < config.BRIGHTNESS_MIN:
        reasons.append("too dark")
    elif brightness > config.BRIGHTNESS_MAX:
        reasons.append("too bright")

    status = "review_needed" if reasons else "usable"
    return status, reasons


def analyze_image(data: bytes) -> dict:
    image = decode_image(data)
    height, width = image.shape[:2]

    if width < config.MIN_DIMENSION_PX or height < config.MIN_DIMENSION_PX:
        raise DecodeError("Image dimensions too small")
    if width > config.MAX_DIMENSION_PX or height > config.MAX_DIMENSION_PX:
        raise DecodeError("Image dimensions too large")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = blur_score(gray)
    brightness = brightness_score(gray)
    status, reasons = classify(blur, brightness)

    return {
        "width": width,
        "height": height,
        "blur_score": round(blur, 2),
        "brightness_score": round(brightness, 2),
        "status": status,
        "reasons": reasons,
    }
