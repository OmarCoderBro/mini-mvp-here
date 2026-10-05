import cv2
import numpy as np
import pytest


def _encode(image: np.ndarray) -> bytes:
    ok, buf = cv2.imencode(".png", image)
    assert ok
    return buf.tobytes()


@pytest.fixture
def sharp_image_bytes() -> bytes:
    rng = np.random.default_rng(42)
    image = rng.integers(0, 255, size=(200, 200, 3), dtype=np.uint8)
    return _encode(image)


@pytest.fixture
def blurred_image_bytes(sharp_image_bytes: bytes) -> bytes:
    array = np.frombuffer(sharp_image_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    blurred = cv2.GaussianBlur(image, (25, 25), 0)
    return _encode(blurred)


@pytest.fixture
def dark_image_bytes() -> bytes:
    image = np.full((200, 200, 3), 10, dtype=np.uint8)
    return _encode(image)


@pytest.fixture
def bright_image_bytes() -> bytes:
    image = np.full((200, 200, 3), 245, dtype=np.uint8)
    return _encode(image)


@pytest.fixture
def normal_image_bytes() -> bytes:
    image = np.full((200, 200, 3), 128, dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (180, 180), (200, 50, 50), 3)
    cv2.rectangle(image, (60, 60), (140, 140), (50, 200, 50), 3)
    return _encode(image)
