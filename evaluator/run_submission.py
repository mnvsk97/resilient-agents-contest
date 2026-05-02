#!/usr/bin/env python3
import json
import subprocess
import sys
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


def fail(message: str) -> int:
    print(json.dumps({"passed": False, "error": message}, indent=2))
    return 1


def main() -> int:
    if len(sys.argv) != 2:
        return fail("Usage: evaluator/run_submission.py <submission_dir>")

    submission_dir = Path(sys.argv[1]).resolve()
    if not submission_dir.exists():
        return fail(f"Submission directory not found: {submission_dir}")

    missing = [path for path in REQUIRED_FILES if not (submission_dir / path).exists()]
    if missing:
        return fail(f"Missing required files: {', '.join(missing)}")

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
            f"{result.returncode}: {result.stderr.strip()}"
        )

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return fail(f"Run command did not emit valid JSON: {exc}")

    missing_fields = sorted(REQUIRED_OUTPUT_FIELDS.difference(payload))
    if missing_fields:
        return fail(f"Output missing required fields: {', '.join(missing_fields)}")

    score = {
        "passed": True,
        "status": payload["status"],
        "score": 60 if payload["status"] == "success" else 30,
        "checks": {
            "required_files": True,
            "valid_json_output": True,
            "required_fields": True,
        },
        "submission_output": payload,
    }
    print(json.dumps(score, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
