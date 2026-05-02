# Results

Organizer-verified evaluator outputs go here as JSON files.

Do not accept participant-submitted result files as verified leaderboard entries. Generate these files from organizer-run evaluations.

Example:

```bash
python3 evaluator/run_submission.py examples/sample-agent \
  --team "Sample Team" \
  --project "Sample Agent" \
  --repo "https://github.com/example/sample-agent" \
  --result-file results/sample-team.json

python3 scripts/generate_leaderboard.py
```
