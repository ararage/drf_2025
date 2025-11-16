"""
Generate Django JSON fixtures for the WatchList model (watchlist_app.watchlist).
This script creates 200 fixtures at:
  watchmate/watchlist_app/fixtures/watchlists_200.json

Run with the workspace Python interpreter. Example:
"C:/Users/Ricardo Perez/drf_2025/env/Scripts/python.exe" scripts/generate_watchlist_fixtures.py
"""
import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))  # repository root
OUT_DIR = os.path.join(ROOT, "watchmate", "watchlist_app", "fixtures")
OUT_FILE = os.path.join(OUT_DIR, "watchlists_200.json")

os.makedirs(OUT_DIR, exist_ok=True)

records = []
NUM = 200
for i in range(1, NUM + 1):
    # Deterministic UUID-like primary keys. These are valid UUID strings.
    pk = "00000000-0000-0000-0000-%012x" % i
    number_rating = i % 10  # 0..9
    if number_rating == 0:
        avg_rating = 0.0
    else:
        avg_rating = float((i % 5) + 1)  # 1.0 .. 5.0

    record = {
        "model": "watchlist_app.watchlist",
        "pk": pk,
        "fields": {
            "title": f"Watchlist Movie {i}",
            "storyline": f"Auto-generated fixture storyline for movie {i}.",
            "platform": "8b4da7bce9184cc3b6c911ce4ec63c83",
            "active": True,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
        }
    }
    records.append(record)

with open(OUT_FILE, "w", encoding="utf-8") as fh:
    json.dump(records, fh, indent=2, ensure_ascii=False)

print(f"Wrote {len(records)} fixtures to: {OUT_FILE}")
