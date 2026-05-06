"""Simple file-based data service for input/output/archive operations.

Provides small helpers used by the app to read input JSON documents,
write standardized outputs, and move processed files to an archive folder.
"""

from pathlib import Path
import json
import shutil
from datetime import datetime
from typing import Dict, Any, Optional


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
ARCHIVE_DIR = DATA_DIR / "archive"


class DataService:
	"""Filesystem helpers for reading and writing JSON documents."""

	def __init__(self):
		for d in (INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR):
			d.mkdir(parents=True, exist_ok=True)

	def load_json(self, path: Path) -> Dict[str, Any]:
		path = Path(path)
		if not path.exists():
			raise FileNotFoundError(f"Input file not found: {path}")
		with path.open("r", encoding="utf-8") as fh:
			return json.load(fh)

	def load_input_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
		# Look for a matching file named <document_id>.json or any file containing the id
		candidate = INPUT_DIR / f"{document_id}.json"
		if candidate.exists():
			return self.load_json(candidate)

		# Fallback: search files for matching document_id inside
		for p in INPUT_DIR.glob("*.json"):
			try:
				j = self.load_json(p)
				if j.get("document_id") == document_id:
					return j
			except Exception:
				continue

		return None

	def save_output(self, document_id: str, data: Dict[str, Any]) -> Path:
		out_path = OUTPUT_DIR / f"{document_id}.json"
		with out_path.open("w", encoding="utf-8") as fh:
			json.dump(data, fh, ensure_ascii=False, indent=2, default=str)
		return out_path

	def archive_input(self, path_or_id: str) -> Optional[Path]:
		p = Path(path_or_id)
		if not p.exists():
			# try by id
			candidate = INPUT_DIR / f"{path_or_id}.json"
			if candidate.exists():
				p = candidate
			else:
				return None

		ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
		dest = ARCHIVE_DIR / f"{p.stem}.{ts}{p.suffix}"
		shutil.move(str(p), str(dest))
		return dest


__all__ = ["DataService", "INPUT_DIR", "OUTPUT_DIR", "ARCHIVE_DIR"]
