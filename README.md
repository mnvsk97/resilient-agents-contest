# Resilient Agents Contest

Build an AI agent that keeps working when real-world infrastructure fails.

This contest is measured with automated scenarios. Your submission must be runnable without manual steps, survive injected failures, and produce structured output that the evaluator can score.

## What You Build

Build an agent for a real workflow. The agent should complete the task while handling failures such as:

- model rate limits
- provider outages
- tool timeouts
- malformed tool responses
- latency spikes
- partial or stale data

Projects should use TrueFoundry AI Gateway meaningfully for routing, fallback, observability, policy, budgets, or guardrails.

## Submission Contract

Every submission must include:

```text
.
├── README.md
├── contest.yaml
├── contest/
│   ├── run.sh
│   └── healthcheck.sh
├── Dockerfile
└── src/
```

The evaluator will run:

```bash
docker build -t resilient-agent-submission .
docker run --rm --env-file .env.evaluator resilient-agent-submission ./contest/run.sh
```

The run command must print one JSON object to stdout.

## Output Format

```json
{
  "status": "success",
  "answer": "Final user-facing result",
  "actions_taken": ["retried_model", "used_fallback_provider"],
  "errors_recovered": 2,
  "trace_id": "optional-trace-id"
}
```

## Scoring

- 35% resilience under injected failures
- 20% task completion correctness
- 15% safe recovery behavior
- 15% meaningful TrueFoundry AI Gateway usage
- 10% product usefulness
- 5% README and demo clarity

See [rules.md](rules.md) for participant rules.

See [docs/contest-operations.md](docs/contest-operations.md) for the organizer runbook, leaderboard plan, and anti-gaming model.

See [leaderboard.md](leaderboard.md) for verified results.

Submissions should go through a private form so teams cannot inspect each other's projects before judging. See [docs/private-submission-intake.md](docs/private-submission-intake.md).

## Local Smoke Test

Run the sample agent:

```bash
python3 evaluator/run_submission.py examples/sample-agent
```

Generate a local leaderboard:

```bash
python3 evaluator/run_submission.py examples/sample-agent \
  --team "Sample Team" \
  --project "Sample Agent" \
  --result-file results/sample-team.json
python3 scripts/generate_leaderboard.py
```
