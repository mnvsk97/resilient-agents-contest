# Private Submission Intake

Use private submission intake when teams should not see each other's projects before judging.

Do not use public GitHub issues for contest submissions. Public issues expose team names, repo URLs, project ideas, demo links, and implementation details to other participants.

## Recommended V1 Flow

- Registration: Luma
- Submission intake: private Google Form, Tally form, Airtable form, or Typeform
- Submission storage: private spreadsheet
- Evaluation: organizer-run scripts
- Public output: leaderboard only

## Submission Form Fields

Required fields:

- Team name
- Participant names
- Contact email
- GitHub repo URL
- Project name
- Short project description
- TrueFoundry AI Gateway usage notes
- Required environment variable names, without secret values
- Demo video URL, optional but recommended
- Confirmation that the repo follows `rules.md`

Optional fields:

- Discord handle
- Preferred public display name
- Whether the repo can be made public after judging
- Any setup notes for organizers

## Privacy Rules

- Keep raw submissions private to organizers and judges.
- Do not publish repo URLs before winners are announced unless the team explicitly agrees.
- Publish only leaderboard fields that are safe to disclose.
- Let teams choose a public display name for the leaderboard.
- Store secrets outside the submission form.

## Organizer Tracking Columns

Use these columns in the private submission spreadsheet:

| Column | Purpose |
|---|---|
| submitted_at | Timestamp from the form |
| team | Public or internal team name |
| display_name | Name shown on leaderboard |
| contact_email | Organizer contact |
| repo_url | Private evaluation input |
| project | Project name |
| demo_url | Judge review |
| gateway_notes | Judge review |
| env_vars | Setup checklist, names only |
| status | submitted, needs-info, evaluated, finalist, winner |
| result_file | `results/<team>.json` path |
| score | Verified evaluator score |
| notes | Internal organizer notes |

## Public Leaderboard Fields

Keep the public leaderboard narrow:

- rank
- display name
- project name
- score
- pass rate
- recovery score
- gateway usage score
- last verified date

Avoid publishing private repo URLs until teams opt in.
