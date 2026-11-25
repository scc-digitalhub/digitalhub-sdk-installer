#!/usr/bin/env bash
set -euo pipefail

version=$(bumpver show -n --environ | sed -n 's/^CURRENT_VERSION=//p')

if [[ "$version" == *"b"* ]]; then
    has_beta_tag=1
else
    has_beta_tag=0
fi

case "${1:-}" in
    new-beta-major|new-beta-minor|new-beta-patch)
        release_type=${1#new-beta-}
        if [ "$has_beta_tag" -eq 0 ]; then
            bumpver update -n "--${release_type}" --tag=beta
        else
            echo "You can create a new beta from a final version! Current version: $version" >&2
            exit 1
        fi
        ;;
    final)
        if [ "$has_beta_tag" -eq 1 ]; then
            bumpver update -n --tag=final
        else
            echo "You can create a final version from a beta version! Current version: $version" >&2
            exit 1
        fi
        ;;
    upgrade-beta)
        if [ "$has_beta_tag" -eq 1 ]; then
            bumpver update -n --tag-num
        else
            echo "You can upgrade a beta from a beta version! Current version: $version" >&2
            exit 1
        fi
        ;;
    major|minor|patch)
        bumpver update -n "--${1}" --tag=final
        ;;
    *)
        echo "Unsupported release type: ${1:-}" >&2
        exit 1
        ;;
esac

version=$(bumpver show -n --environ | sed -n 's/^CURRENT_VERSION=//p')
python .github/scripts/sync_dependency_bounds.py "$version"
