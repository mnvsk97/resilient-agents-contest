# Contest Operations

This document explains how to run the Resilient Agents Contest end to end.

The contest is designed to be simple to operate:

- GitHub is the source of truth for rules, sample code, scenarios, evaluator, and leaderboard data.
- Luma or a form can collect registrations.
- Discord can handle announcements and support.
- Automated evaluator runs decide the leaderboard.
- Judges review finalists for usefulness, clarity, and meaningful TrueFoundry AI Gateway usage.

## Operating Principles

- Make the rules clear before submissions open.
- Give participants a public local evaluator so they can self-test.
- Keep final prize verification separate from public practice scenarios.
- Publish leaderboard results from verified evaluator runs, not from self-reported scores.
- Use hidden scenarios to reduce hardcoding and leaderboard gaming.
- Keep the first version lightweight; avoid building a full contest platform until needed.

## Contest Phases

### 1. Prep

Organizer tasks:

- Finalize `README.md`, `rules.md`, and scoring weights.
- Publish public scenarios under `scenarios/public/`.
- Keep hidden scenarios outside the public repo.
- Confirm registration page.
- Confirm Discord support channel.
- Confirm prize terms and eligibility.
- Confirm judge panel and finalist review process.
- Decide how submissions are collected: GitHub issue form, Google Form, or manual repo list.
- Decide how the leaderboard is published: `leaderboard.md`, GitHub Pages, or both.
- Keep final hidden scenarios in a private organizer workspace. See `docs/hidden-scenarios.md`.

Output:

- Public contest repo ready.
- Registration link live.
- Submission intake method live.
- Public support channel live.

### 2. Launch

Organizer tasks:

- Announce the contest.
- Point participants to this repo.
- Explain the required submission structure.
- Explain the automated evaluation flow.
- Explain what is public practice versus hidden final evaluation.
- Pin the rules and FAQ in Discord.

Participant tasks:

- Register.
- Join Discord.
- Fork or copy the sample agent structure.
- Build their agent.
- Test locally against public scenarios.

### 3. Build Window

Organizer tasks:

- Answer clarifying questions publicly when possible.
- Update FAQ for repeated questions.
- Avoid changing rules in ways that disadvantage teams already building.
- If a rule must change, record the change in the repo.
- Periodically run smoke tests on sample submissions.

Participant tasks:

- Build a runnable agent.
- Keep dependencies pinned.
- Use environment variables for secrets.
- Produce the required JSON output.
- Add enough logs or trace IDs to debug evaluator results.

### 4. Submission

Minimum submission fields:

- Team name
- Participant names
- Contact email
- GitHub repo URL
- Short project description
- Demo video URL, optional for leaderboard but useful for judging
- Notes on TrueFoundry AI Gateway usage
- Any required environment variables, without secret values

For the GitHub-first flow, use the issue form in `.github/ISSUE_TEMPLATE/submission.yml`.

Submission requirements:

- Repo must be accessible to organizers.
- Repo must include required files listed in `rules.md`.
- `./contest/run.sh` must run non-interactively.
- The project must not depend on manual approvals during evaluation.

### 5. Automated Evaluation

For each submission, the organizer runs:

```bash
docker build -t resilient-agent-submission .
docker run --rm --env-file .env.evaluator resilient-agent-submission ./contest/run.sh
```

The evaluator should:

- validate required files
- run health checks
- inject public and hidden failure scenarios
- enforce runtime and cost limits
- parse one JSON result from stdout
- collect logs and traces
- write one result JSON per team
- update the leaderboard from verified results

For v1, write verified outputs to `results/*.json` and regenerate the public leaderboard:

```bash
python3 scripts/generate_leaderboard.py
```

Recommended result file shape:

```json
{
  "team": "Example Team",
  "project": "Reliable Support Agent",
  "repo": "https://github.com/example/reliable-support-agent",
  "verified_at": "2026-05-15T18:30:00Z",
  "score": 84,
  "pass_rate": 0.9,
  "resilience": 31,
  "correctness": 18,
  "recovery": 13,
  "gateway_usage": 14,
  "product_usefulness": 6,
  "readme_demo": 2,
  "notes": "Recovered from rate limits and malformed tool output."
}
```

### 6. Leaderboard

For v1, use a simple leaderboard.

Minimum columns:

| Rank | Team | Project | Score | Pass Rate | Recovery | Gateway Usage | Last Verified |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | Example Team | Reliable Support Agent | 84 | 90% | 13 | 14 | 2026-05-15 |

Leaderboard rules:

- Only organizer-verified runs count.
- Failed runs can be shown as unranked or omitted.
- Ties should be broken by hidden-scenario pass rate, then lower cost, then earlier verified submission time.
- The public leaderboard is provisional until final judging is complete.

### 7. Final Judging

Automated scores should select finalists, not replace judgment.

Judges should review:

- Does the project solve a real workflow?
- Is resilience designed into the agent, or did it only pass fixtures?
- Is TrueFoundry AI Gateway used meaningfully?
- Are logs, traces, retries, and fallbacks understandable?
- Is the demo clear and reproducible?

Recommended final process:

- Select top 5 to 10 verified submissions from the leaderboard.
- Review demos and READMEs.
- Run hidden final scenarios once more.
- Choose winners using both evaluator score and judge review.

## Anti-Gaming Model

AgentBreak and the public evaluator can be open source. That is acceptable if the contest separates practice from verification.

The goal is not to hide the existence of failures. The goal is to prevent participants from hardcoding exact hidden tasks or exploiting evaluator internals.

### Exploit Risks

| Risk | Example | Mitigation |
|---|---|---|
| Hardcoded public scenarios | Agent checks for `public-rate-limit` and returns a canned answer | Hidden scenarios with different IDs, wording, and timing |
| Fixture memorization | Agent matches exact prompt strings from public YAML | Paraphrased hidden tasks and randomized inputs |
| Evaluator detection | Code branches when it sees evaluator-specific env vars or file paths | Minimal exposed evaluator metadata; inspect suspicious submissions |
| Score spoofing | Agent prints high `errors_recovered` without actually recovering | Score from evaluator-observed behavior, not self-reported fields |
| Retry spam | Agent retries endlessly until one call works | Strict timeout, retry, token, and cost limits |
| No-op fallbacks | Agent claims fallback but returns low-quality output | Correctness checks and judge review |
| Hidden file probing | Submission scans filesystem for hidden scenarios | Run in a sandbox with hidden scenarios outside mounted workspace |
| Network exfiltration | Submission sends hidden prompts to an external server | Restrict network where possible; require declared services; inspect finalists |
| Dependency drift | Submission works only because latest package behavior changed | Require pinned dependencies or lockfiles |
| Manual intervention | Team fixes state during judging | Non-interactive evaluation only |
| Production side effects | Agent sends real emails or creates real tickets | Test-mode services, dry-run destinations, idempotency checks |
| Leaderboard overfitting | Teams optimize only for visible public score | Keep public leaderboard provisional and use hidden final verification |

### Practical Guardrails

- Keep hidden scenarios private and outside the public repo.
- Follow `docs/hidden-scenarios.md` when preparing finalist verification tasks.
- Do not mount hidden scenario files into the participant container.
- Pass tasks over stdin, HTTP, or temporary files with neutral names.
- Randomize task IDs, names, timing, and injected fault schedules.
- Score behavior observed by the evaluator, not claims in participant output.
- Keep raw evaluator logs for finalists.
- Run finalist submissions in a clean environment.
- Cap runtime, retries, tokens, and spend.
- Require declared network services in `contest.yaml`.
- Reserve the right to disqualify submissions that tamper with evaluation.

## Recommended V1 Stack

- Registration: Luma
- Support: Discord
- Submission intake: GitHub issue form or Google Form
- Evaluation: organizer-run script plus hidden scenarios
- Results storage: `results/*.json`
- Leaderboard: generated `leaderboard.md`
- Final review: judge panel

## Open Questions

- Will submissions be public during the contest or only after judging?
- Will teams submit through GitHub issues, a form, or email?
- Will participants get multiple official leaderboard attempts?
- What are the exact runtime and cost budgets?
- Which TrueFoundry AI Gateway features are required versus optional?
- What hidden scenarios should decide finalist verification?
