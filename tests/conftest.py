import sys
from pathlib import Path


# Ensure `src` is on sys.path so tests can import `orf_finder` package.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
