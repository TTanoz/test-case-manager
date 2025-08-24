# tests/conftest.py
import sys
from pathlib import Path

# project root'u sys.path'e ekle
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))