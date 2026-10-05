export interface ImageResult {
  filename: string;
  width: number;
  height: number;
  blur_score: number;
  brightness_score: number;
  status: "usable" | "review_needed";
  reasons: string[];
}

export interface ImageError {
  filename: string;
  error: string;
}

export interface AnalyzeResponse {
  results: ImageResult[];
  errors: ImageError[];
}
