"""Convenience runner for the project.

Creates required directories (data/input, data/output, data/archive, logs) and
optionally starts the FastAPI app with Uvicorn.

Usage:
    python scripts/run_app.py --serve    # create directories and start server
    python scripts/run_app.py            # only create directories
"""
from pathlib import Path
import argparse

try:
    import uvicorn
except Exception:
    uvicorn = None


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
ARCHIVE_DIR = DATA_DIR / "archive"
LOG_DIR = BASE_DIR / "logs"


def setup_dirs():
    for p in (INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR, LOG_DIR):
        p.mkdir(parents=True, exist_ok=True)


def main(serve: bool = False, host: str = "0.0.0.0", port: int = 8000):
    setup_dirs()
    print(f"Ensured directories exist under {BASE_DIR}")

    if serve:
        if uvicorn is None:
            raise RuntimeError("uvicorn is not available. Install requirements before using --serve")
        uvicorn.run("app.api:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Start the uvicorn server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(serve=args.serve, host=args.host, port=args.port)
