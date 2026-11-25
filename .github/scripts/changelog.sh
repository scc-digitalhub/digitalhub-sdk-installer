#!/usr/bin/env bash
set -euo pipefail

if [ "${2:-false}" = "true" ]; then
    touch CHANGELOG.md
else
    git-cliff --unreleased --tag "$1" -c .github/scripts/cliff.toml -v -o
fi
