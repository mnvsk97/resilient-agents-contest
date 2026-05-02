# Evaluator

This folder contains organizer-owned evaluation tools.

The first evaluator goal is intentionally simple:

1. Validate that a submission has required files.
2. Run its `contest/run.sh` command.
3. Parse stdout as JSON.
4. Check required output fields.
5. Produce a score payload that can later feed a leaderboard.

Hidden scenarios should not be committed to this public folder.
