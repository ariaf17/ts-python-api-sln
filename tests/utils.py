import json
from pathlib import Path
from datetime import datetime

# Returns the root directory of the repository, assumes this file is located at <repo_root>/tests/utils.py
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]

# Loads a JSON file from the relative path, the path is relative to the repository root
def load_json(rel_path: str) -> dict:
    path = repo_root() / rel_path
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)
    
# Parses a datetime string in ISO format, handling the 'Z' timezone for UTC
def parse_iso8601(s: str) -> datetime:
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

