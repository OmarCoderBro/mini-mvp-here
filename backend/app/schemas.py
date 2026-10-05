from typing import Literal

from pydantic import BaseModel


class ImageResult(BaseModel):
    filename: str
    width: int
    height: int
    blur_score: float
    brightness_score: float
    status: Literal["usable", "review_needed"]
    reasons: list[str]


class ImageError(BaseModel):
    filename: str
    error: str


class AnalyzeResponse(BaseModel):
    results: list[ImageResult]
    errors: list[ImageError]


class HealthResponse(BaseModel):
    status: Literal["ok"]


class SampleImage(BaseModel):
    filename: str
    url: str


class SamplesResponse(BaseModel):
    samples: list[SampleImage]
