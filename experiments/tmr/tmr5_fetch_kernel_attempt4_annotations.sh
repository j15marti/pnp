#!/usr/bin/env bash
# Read-only diagnostic. Requires GitHub CLI authenticated for j15marti/pnp.
set -euo pipefail
REPO='j15marti/pnp'
RUN='43804269099'
JOB='133266252794'
OUT="${1:-kernel-attempt4-diagnostics}"
if ! command -v gh >/dev/null 2>&1; then
  printf 'GitHub CLI (gh) is required. No credentials or repository settings were changed.\n' >&2
  exit 2
fi
gh auth status >/dev/null
mkdir -p "$OUT"
gh api "repos/$REPO/actions/runs/$RUN/attempts/4/jobs" > "$OUT/jobs.json"
gh api "repos/$REPO/check-runs/$JOB" > "$OUT/check-run.json"
gh api --paginate "repos/$REPO/check-runs/$JOB/annotations" > "$OUT/annotations.json"
printf 'Failure annotations:\n'
gh api --paginate "repos/$REPO/check-runs/$JOB/annotations" \
  --jq '.[] | {title, message, raw_details}'
printf '\nRead-only diagnostics saved to %s\n' "$OUT"
