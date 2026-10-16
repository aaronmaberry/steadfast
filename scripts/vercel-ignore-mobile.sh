#!/usr/bin/env bash
# Exit 0 to skip the Vercel build. Exit 1 to build the website.
# Commits that only touch mobile/ do not redeploy the site.
set -u

prev="${VERCEL_GIT_PREVIOUS_SHA:-}"
if [ -z "$prev" ]; then
  exit 1
fi
if ! git cat-file -e "${prev}^{commit}" 2>/dev/null; then
  exit 1
fi
if ! names="$(git diff --name-only "$prev" HEAD)"; then
  exit 1
fi
non_mobile="$(printf '%s\n' "$names" | grep -vE '^(mobile/|$)' || true)"
if [ -n "$non_mobile" ]; then
  exit 1
fi
exit 0
