#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "contest.yaml",
    "contest/run.sh",
    "contest/healthcheck.sh",
    "Dockerfile",
]

REQUIRED_OUTPUT_FIELDS = {
    "status",
    "answer",
    "actions_taken",
    "errors_recovered",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fail(message: str, result_file: Path | None = None) -> int:
    payload = {"passed": False, "verified_at": utc_now(), "error": message}
    if result_file:
        result_file.parent.mkdir(parents=True, exist_ok=True)
        result_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a contest submission smoke evaluation.")
    parser.add_argument("submission_dir", help="Path to the submission directory")
    parser.add_argument("--team", default="Unverified Team", help="Team name for result output")
    parser.add_argument("--project", default="Untitled Project", help="Project name for result output")
    parser.add_argument("--repo", default="", help="Submission repository URL")
    parser.add_argument("--result-file", help="Optional path to write a verified result JSON")
    args = parser.parse_args()

    result_file = Path(args.result_file).resolve() if args.result_file else None
    submission_dir = Path(args.submission_dir).resolve()
    if not submission_dir.exists():
        return fail(f"Submission directory not found: {submission_dir}", result_file)

    missing = [path for path in REQUIRED_FILES if not (submission_dir / path).exists()]
    if missing:
        return fail(f"Missing required files: {', '.join(missing)}", result_file)

    healthcheck = subprocess.run(
        [str(submission_dir / "contest" / "healthcheck.sh")],
        cwd=submission_dir,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )

    if healthcheck.returncode != 0:
        return fail(
            "Healthcheck failed with exit code "
            f"{healthcheck.returncode}: {healthcheck.stderr.strip()}",
            result_file,
        )

    run_script = submission_dir / "contest" / "run.sh"
    result = subprocess.run(
        [str(run_script)],
        cwd=submission_dir,
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )

    if result.returncode != 0:
        return fail(
            "Run command failed with exit code "
            f"{result.returncode}: {result.stderr.strip()}",
            result_file,
        )

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return fail(f"Run command did not emit valid JSON: {exc}", result_file)

    missing_fields = sorted(REQUIRED_OUTPUT_FIELDS.difference(payload))
    if missing_fields:
        return fail(f"Output missing required fields: {', '.join(missing_fields)}", result_file)

    if payload["status"] not in {"success", "partial", "failed"}:
        return fail("Output field `status` must be one of: success, partial, failed", result_file)

    if not isinstance(payload["answer"], str):
        return fail("Output field `answer` must be a string", result_file)

    if not isinstance(payload["actions_taken"], list):
        return fail("Output field `actions_taken` must be a list", result_file)

    if not isinstance(payload["errors_recovered"], int):
        return fail("Output field `errors_recovered` must be an integer", result_file)

    status_score = {"success": 60, "partial": 35, "failed": 10}[payload["status"]]

    score = {
        "passed": True,
        "team": args.team,
        "project": args.project,
        "repo": args.repo,
        "verified_at": utc_now(),
        "status": payload["status"],
        "score": status_score,
        "pass_rate": 1.0 if payload["status"] == "success" else 0.5 if payload["status"] == "partial" else 0.0,
        "resilience": 20 if payload["status"] == "success" else 8,
        "correctness": 20 if payload["status"] == "success" else 10 if payload["status"] == "partial" else 0,
        "recovery": 5,
        "gateway_usage": 0,
        "product_usefulness": 10 if payload["status"] == "success" else 5,
        "readme_demo": 5,
        "checks": {
            "required_files": True,
            "healthcheck": True,
            "valid_json_output": True,
            "required_fields": True,
        },
        "self_reported": {
            "actions_taken": payload["actions_taken"],
            "errors_recovered": payload["errors_recovered"],
            "trace_id": payload.get("trace_id"),
        },
        "submission_output": payload,
    }
    if result_file:
        result_file.parent.mkdir(parents=True, exist_ok=True)
        result_file.write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(score, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
