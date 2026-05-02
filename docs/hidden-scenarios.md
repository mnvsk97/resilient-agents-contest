# Hidden Scenarios

Hidden scenarios are used for finalist verification and prize decisions.

Do not commit hidden scenario files to this public repository. Keep them in a private organizer workspace and pass scenario tasks into submissions at evaluation time.

## What To Keep Hidden

- final task wording
- scenario IDs
- fixture data
- exact injected fault schedule
- expected answer keys
- judge notes

## What Can Be Public

- categories of failures
- scoring rubric
- public practice scenarios
- required input and output contract
- examples of acceptable recovery behavior

## Recommended Hidden Scenario Types

- Rate limit appears after the first successful model call.
- Primary model returns malformed JSON once, then valid JSON.
- Tool call times out during a multi-step workflow.
- Provider route fails and must fall back through TrueFoundry AI Gateway.
- Tool response contains stale or contradictory data.
- Agent must avoid duplicate side effects after retry.

## Handling Hidden Tasks Safely

- Do not mount hidden scenario files into the participant container.
- Pass one task at a time through stdin, HTTP, or a neutral temporary file.
- Use randomized task IDs and names.
- Keep raw evaluator logs for finalist review.
- Restrict network access where possible.
- Re-run finalists in a clean environment.
