#!/bin/bash
# Script: apply-branch-protection.sh
# Use GitHub CLI (gh) to apply recommended branch protection to main.
# Usage: gh auth login && bash apply-branch-protection.sh <owner> <repo>

OWNER=${1:-garthmoseczo-spec}
REPO=${2:-aegis-treasury}

echo "Applying branch protection to $OWNER/$REPO:main"

gh api --method PUT /repos/$OWNER/$REPO/branches/main/protection -f required_status_checks='{"strict":true,"contexts":["Python tests (Windows)","Java (Maven) build (Windows)","CodeQL analysis"]}' -f enforce_admins=true -f required_pull_request_reviews='{"dismiss_stale_reviews":true,"required_approving_review_count":1}' -f restrictions='null'

if [ $? -eq 0 ]; then
  echo "Branch protection applied."
else
  echo "Branch protection API call failed. Please ensure gh is authenticated and you have admin rights, or apply settings via the web UI." >&2
fi
