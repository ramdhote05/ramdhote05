import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "ramdhote05"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_contributions():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    return response.text


def parse_contrib_data(html):
    soup = BeautifulSoup(html, "html.parser")
    cells = []
    for day in soup.select("rect.day"):
        date = day.get("data-date")
        count = int(day.get("data-count", "0"))
        level = day.get("data-level", "0")
        cells.append({"date": date, "count": count, "level": level})

    valid = [c for c in cells if c["count"] > 0]
    if valid:
        current_streak = 0
        for item in sorted(cells, key=lambda x: x["date"], reverse=True):
            if item["count"] > 0:
                current_streak += 1
            else:
                break

        longest = 0
        streak = 0
        for item in sorted(cells, key=lambda x: x["date"]):
            if item["count"] > 0:
                streak += 1
                longest = max(longest, streak)
            else:
                streak = 0

        best_day = max(cells, key=lambda x: x["count"]) if cells else {"date": None, "count": 0}
        total = sum(c["count"] for c in cells)
        monthly = {}
        for item in cells:
            if not item["date"]:
                continue
            month = item["date"][:7]
            monthly[month] = monthly.get(month, 0) + item["count"]
    else:
        current_streak = 0
        longest = 0
        best_day = {"date": None, "count": 0}
        total = 0
        monthly = {}

    return {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "cells": cells,
        "summary": {
            "total": total,
            "current_streak": current_streak,
            "longest_streak": longest,
            "best_day": best_day,
            "monthly_totals": monthly,
        },
    }


def main():
    html = fetch_contributions()
    data = parse_contrib_data(html)
    out_dir = Path(__file__).resolve().parents[1] / "data"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "contributions.json").open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
