import pytest

from app.analyzer import DecodeError, analyze_image


def test_sharp_image_scores_higher_than_blurred(sharp_image_bytes, blurred_image_bytes):
    sharp = analyze_image(sharp_image_bytes)
    blurred = analyze_image(blurred_image_bytes)
    assert sharp["blur_score"] > blurred["blur_score"]


def test_dark_image_flagged(dark_image_bytes):
    result = analyze_image(dark_image_bytes)
    assert result["status"] == "review_needed"
    assert "too dark" in result["reasons"]


def test_bright_image_flagged(bright_image_bytes):
    result = analyze_image(bright_image_bytes)
    assert result["status"] == "review_needed"
    assert "too bright" in result["reasons"]


def test_normal_image_usable(normal_image_bytes):
    result = analyze_image(normal_image_bytes)
    assert result["status"] == "usable"
    assert result["reasons"] == []


def test_invalid_bytes_raise_decode_error():
    with pytest.raises(DecodeError):
        analyze_image(b"not an image")
