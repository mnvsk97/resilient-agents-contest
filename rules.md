# Contest Rules

## Core Rule

Submit a runnable agent, not only a demo video. The evaluator must be able to clone your repo, inject environment variables, run one command, and produce a score.

## Participant Rules

1. Submissions must run with `./contest/run.sh`.
2. Submissions must include a `Dockerfile`.
3. Submissions must not require manual browser clicks, notebook execution, local credentials, or human approval during evaluation.
4. Secrets must come from environment variables only.
5. Dependencies must be pinned through a lockfile or explicit version ranges.
6. The run command must print one valid JSON object to stdout.
7. The agent must handle repeated runs safely. Do not create duplicate irreversible side effects.
8. External network dependencies must be listed in `contest.yaml`.
9. Every external call should have a timeout.
10. The agent must degrade gracefully when the primary model, provider, or tool fails.
11. Public scenarios may be used for testing, but submissions must not hardcode public fixture strings, task IDs, or expected hidden-test answers.
12. Submissions must not inspect hidden evaluator files, modify the evaluator, call private leaderboard APIs, or branch behavior based on evaluator internals.
13. Submissions must emit enough logs, traces, or structured metadata to explain retries, fallbacks, and final decisions.

## Required Files

```text
README.md
contest.yaml
contest/run.sh
contest/healthcheck.sh
Dockerfile
```

## Allowed

- Any programming language
- Any agent framework
- Any model provider
- TrueFoundry AI Gateway for routing, fallback, observability, guardrails, or policy controls
- Local mock services included in the submission

## Not Allowed

- Hardcoded hidden-test answers
- Manual operations during evaluation
- Hardcoded secrets
- Writing outside the submission workspace unless explicitly documented
- Long-running background services that do not shut down cleanly
- Destructive actions against real production systems

## Evaluation

The organizer may run public and hidden scenarios. Prize eligibility depends on verified evaluator runs and judge review.
