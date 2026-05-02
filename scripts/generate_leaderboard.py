#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
LEADERBOARD_MD = ROOT / "leaderboard.md"
LEADERBOARD_JSON = ROOT / "leaderboard.json"


def load_results() -> list[dict]:
    if not RESULTS_DIR.exists():
        return []

    results = []
    for path in sorted(RESULTS_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as file:
            result = json.load(file)
        if result.get("passed") is True:
            result["_source"] = path.name
            results.append(result)
    return results


def rank_results(results: list[dict]) -> list[dict]:
    return sorted(
        results,
        key=lambda item: (
            -item.get("score", 0),
            -item.get("pass_rate", 0),
            -item.get("recovery", 0),
            -item.get("gateway_usage", 0),
            item.get("verified_at", ""),
        ),
    )


def project_cell(result: dict) -> str:
    project = result.get("project") or "Untitled"
    repo = result.get("repo") or ""
    if repo:
        return f"[{project}]({repo})"
    return project


def format_percent(value: float | int | None) -> str:
    if value is None:
        return "0%"
    return f"{float(value) * 100:.0f}%"


def write_markdown(results: list[dict]) -> None:
    lines = [
        "# Leaderboard",
        "",
        "Only organizer-verified evaluator runs are ranked here.",
        "",
    ]

    if not results:
        lines.extend(
            [
                "No verified submissions yet.",
                "",
                "Run an evaluation with `--result-file results/<team>.json`, then run:",
                "",
                "```bash",
                "python3 scripts/generate_leaderboard.py",
                "```",
                "",
            ]
        )
        LEADERBOARD_MD.write_text("\n".join(lines), encoding="utf-8")
        return

    lines.extend(
        [
            "| Rank | Team | Project | Score | Pass Rate | Recovery | Gateway Usage | Last Verified |",
            "|---:|---|---|---:|---:|---:|---:|---|",
        ]
    )

    for index, result in enumerate(results, start=1):
        verified_at = str(result.get("verified_at", ""))[:10]
        lines.append(
            "| "
            f"{index} | "
            f"{result.get('team', 'Unknown')} | "
            f"{project_cell(result)} | "
            f"{result.get('score', 0)} | "
            f"{format_percent(result.get('pass_rate', 0))} | "
            f"{result.get('recovery', 0)} | "
            f"{result.get('gateway_usage', 0)} | "
            f"{verified_at} |"
        )

    lines.append("")
    LEADERBOARD_MD.write_text("\n".join(lines), encoding="utf-8")


def write_json(results: list[dict]) -> None:
    public_results = []
    for index, result in enumerate(results, start=1):
        public_results.append(
            {
                "rank": index,
                "team": result.get("team", "Unknown"),
                "project": result.get("project", "Untitled"),
                "repo": result.get("repo", ""),
                "score": result.get("score", 0),
                "pass_rate": result.get("pass_rate", 0),
                "recovery": result.get("recovery", 0),
                "gateway_usage": result.get("gateway_usage", 0),
                "verified_at": result.get("verified_at", ""),
            }
        )
    LEADERBOARD_JSON.write_text(json.dumps(public_results, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ranked = rank_results(load_results())
    write_markdown(ranked)
    write_json(ranked)
    print(f"Wrote {LEADERBOARD_MD} and {LEADERBOARD_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
