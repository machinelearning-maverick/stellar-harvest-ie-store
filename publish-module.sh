#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# deployment/scripts/publish-module.sh
# ------------------------------------------------------------
# Usage:
#   ./publish-module.sh [--version <version>] [<path-to-your-project>]
#
# Examples:
#   ./publish-module.sh                   # build & upload all dist/*
#   ./publish-module.sh --version 0.2.1   # upload only dist/*0.2.1*
#
# Prereqs:
#   pip install build twine
#   .env (in this script’s dir) containing:
#     TWINE_REPOSITORY_URL=https://example.com/devpi/team/pypi/
#     TWINE_USERNAME=team
#     TWINE_PASSWORD=YourSecretHere
# ------------------------------------------------------------

# load .env
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/.env" ]]; then
  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/.env"
else
  echo "❗  No .env found in $SCRIPT_DIR; please create it with TWINE_REPOSITORY_URL, TWINE_USERNAME, TWINE_PASSWORD"
  exit 1
fi

# ensure required vars
: "${TWINE_REPOSITORY_URL:?Need TWINE_REPOSITORY_URL in .env}"
: "${TWINE_USERNAME:?Need TWINE_USERNAME in .env}"
: "${TWINE_PASSWORD:?Need TWINE_PASSWORD in .env}"

# parse args
VERSION=""
PROJECT_DIR=""
while [[ $# -gt 0 ]]; do
  case $1 in
    -v|--version)
      shift
      VERSION="$1"
      ;;
    -*)
      echo "Unknown option $1" >&2
      exit 1
      ;;
    *)
      PROJECT_DIR="$1"
      ;;
  esac
  shift
done

# default project dir
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR"

echo "▶️  Publishing project in $PROJECT_DIR"
[[ -n $VERSION ]] && echo "   – filtering for version: $VERSION"

source .venv/bin/activate

# build wheel + sdist
echo "📦 Installing locally and building artifacts..."
pip install -r requirements.txt --upgrade
pip install --quiet --upgrade -e . build twine
python3 -m build

# prepare list of files to upload
if [[ -n $VERSION ]]; then
  FILES=(dist/*"$VERSION"*)
else
  FILES=(dist/*)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "❌ No files found to upload in dist/ matching version '$VERSION'"
  exit 1
fi

echo "🚀 Uploading ${#FILES[@]} file(s):"
printf "   %s\n" "${FILES[@]}"

# upload with twine
TWINE_REPOSITORY_URL="$TWINE_REPOSITORY_URL" \
TWINE_USERNAME="$TWINE_USERNAME" \
TWINE_PASSWORD="$TWINE_PASSWORD" \
twine upload -r "" \
  --repository-url "$TWINE_REPOSITORY_URL" \
  "${FILES[@]}"

echo "✅ Publish complete!"
