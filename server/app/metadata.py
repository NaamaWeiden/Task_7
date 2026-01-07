import json
from pathlib import Path

METADATA_FILE = Path("metadata.json")
_metadata_cache = {}

def load_from_disk():
    global _metadata_cache
    if METADATA_FILE.exists():
        _metadata_cache = json.loads(METADATA_FILE.read_text())
    else:
        _metadata_cache = {}

def save_to_disk():
    METADATA_FILE.write_text(json.dumps(_metadata_cache, indent=2))

def asset_exists(hash_value):
    return hash_value in _metadata_cache

def add_asset(hash_value, entry):
    _metadata_cache[hash_value] = entry
    save_to_disk()
