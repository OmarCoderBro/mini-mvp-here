# HERE Road Image Quality Checker MVP

## Purpose

Build a small recruiter-facing demo inspired by the HERE Technologies Software Engineer Intern posting. The role describes full-stack development, automation, continuous delivery, and work with computer-vision and machine-learning engineers.

This MVP demonstrates one supporting workflow: flag road images that may be blurry or poorly lit before they enter a computer-vision pipeline. It is an independent portfolio project, not a HERE product and not a claim about the team's exact current work.

## MVP outcome

A user selects or uploads a small batch of road images. The application measures blur and brightness, marks each image as Usable or Review needed, and explains the result.

Keep the MVP narrow: one page, two image-quality measurements, clear results, and a local demo. The thresholds are simple heuristics and must be described as screening signals, not objective proof that an image is suitable for machine learning.

## Technology stack

- Python for image analysis.
- OpenCV for decoding images and calculating blur and brightness measures.
- FastAPI for the small analysis API.
- React and TypeScript with Vite for the user interface.
- Docker Compose for a repeatable local run.
- Linux container environment for consistent runtime behavior.

Use Python because it is explicitly named in the internship posting and suits this compact computer-vision workflow. OpenCV, FastAPI, React, and TypeScript are implementation choices for the demo. Do not add C++, Java, Scala, Kubernetes, AWS, a database, or model-training libraries unless the user asks.

## User workflow

1. The user selects up to 20 sample road images.
2. The React page sends the images to the FastAPI endpoint.
3. The Python service decodes each image with OpenCV.
4. The analyzer calculates image dimensions, blur score, and average brightness.
5. Simple configurable thresholds mark the image Usable or Review needed and attach reason labels.
6. The API returns JSON results and the UI displays a preview, status, and measurements for each image.

Use openly licensed sample images or images the user has permission to use. Keep samples in a small local directory and include attribution when required.

## Analysis rules

Implement two easy-to-explain checks:

- Blur: use variance of the Laplacian as a basic sharpness indicator. A low score can flag a likely blurry image.
- Brightness: use the mean intensity of a grayscale image. Very low or very high values can flag a dark or washed-out image.

Put thresholds in one clearly named configuration location. Make them easy to adjust during a demo. Return the numeric scores and reason labels so the user can understand why an image was flagged.

Handle unreadable or unsupported images as per-file errors. One bad file must not prevent valid images in the same batch from being analyzed. Do not claim that these two checks assess focus, exposure, road visibility, or ML suitability perfectly.

## API scope

Implement only endpoints required by the demo:

- GET /health returns a small status response.
- POST /analyze accepts a bounded batch of image uploads and returns one result per file.

Each successful image result should include:

- filename
- width and height
- blur_score
- brightness_score
- status
- reasons

Each failed image result should include a safe, readable error message. Validate the maximum batch count, file size, file type, and decoded image dimensions. Do not store uploaded images or analysis results after the request completes.

## User interface

Build one responsive page containing:

- A file picker supporting multiple images.
- A clear limit of 20 images per batch.
- An Analyze images button.
- A results list with thumbnail, filename, dimensions, blur score, brightness, status, and reason labels.
- Loading, empty, partial-failure, and API-error states.
- A short explanation that the checks are heuristic screening signals.

Avoid accounts, navigation, charts, elaborate styling, image editing, or a multi-page dashboard.

## Docker and Linux use

Use Docker Compose to run the FastAPI service in a container with its Python and OpenCV dependencies, and optionally run the Vite frontend in a second development container. This makes the setup reproducible and avoids relying on packages installed directly on the user's machine.

The containers run in a Linux environment. That demonstrates basic Linux and Docker familiarity relevant to the posting while keeping this project local. Provide simple start and stop commands in README.md. Do not deploy to cloud or add Kubernetes.

## Security and reliability

- Accept only image formats supported by the application.
- Enforce upload count and byte-size limits before processing.
- Decode files with OpenCV and report invalid files safely.
- Use generated filenames for temporary files if temporary storage is needed; delete them after processing.
- Do not log image bytes or expose local filesystem paths in API responses.
- Do not include credentials or personal data in sample images.
- Configure CORS only for the local frontend during development.
- Keep errors useful but do not return stack traces.
- Do not claim production readiness, clinical safety, road-safety certification, or validated model performance.

## Tests

Add focused tests for behavior that matters:

- A sharp synthetic image produces a higher blur score than a blurred version of the same image.
- Dark and bright synthetic images trigger the expected brightness flags.
- Invalid image bytes return a per-file error without crashing the batch.
- Batch and file-size limits are enforced.
- API results include the documented fields and statuses.

Use pytest. Create images in tests with OpenCV or NumPy instead of relying on large test assets. Run the relevant tests after changes and report the exact commands and results. Do not say tests pass unless they were run.

## Suggested project structure

Adapt this to the repository if it already has a structure:

- frontend/ for the React and TypeScript UI.
- backend/app/main.py for FastAPI setup.
- backend/app/analyzer.py for blur and brightness calculations.
- backend/app/schemas.py for response models.
- backend/tests/ for focused pytest tests.
- samples/ for a small set of attributed example images.
- Dockerfile and docker-compose.yml for the local demo.
- .env.example only if configuration requires environment variables.
- .gitignore for local caches, virtual environments, node_modules, build output, and secrets.
- README.md for setup, analysis limitations, and the demo flow.

Keep the structure compact. Avoid empty files or abstractions with no current use.

## How Claude Code should work

- Read this file and inspect the repository before proposing changes.
- Start with a short plan and wait for user approval before broad implementation.
- Build one slice at a time: analysis functions and tests, API, UI, then Docker run.
- Explain changes in plain language and tell the user what to run or try.
- Run relevant checks and report actual results.
- Ask before adding dependencies, expanding scope, using cloud services, or changing the chosen stack.
- Preserve existing working code and avoid unrelated refactors.
- Keep the user updated at each milestone with changed files, test results, blockers, and the next step.
- If a decision is unclear, choose the smallest option consistent with this document and state the assumption.

## Suggested milestones

1. Inspect the repository and agree on a small plan.
2. Implement blur and brightness analysis with focused tests.
3. Add the bounded batch-analysis API.
4. Build the single-page results interface.
5. Add Docker Compose and verify the complete local workflow.
6. Document startup commands, sample-image attribution, and heuristic limitations in README.md.

The finished demo should clearly show a compact computer-vision support workflow, practical automation, and a reproducible Linux-based development setup.
