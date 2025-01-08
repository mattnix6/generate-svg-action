#!/bin/bash

set -e  # Exit immediately on error

# Set defaults for the repository and branch
REPOSITORY=${INPUT_REPOSITORY:-.}
BRANCH=${INPUT_BRANCH:-commit-dashboard}

# Export PYTHONPATH
export PYTHONPATH=/app

# If repository is specified, clone it
if [ "$REPOSITORY" != "." ]; then
  echo "Cloning repository: $REPOSITORY"
  git clone https://github.com/$REPOSITORY.git
  cd $(basename "$REPOSITORY" .git)  # Move into the cloned repo
else
  echo "Using current repository."
  cd $(pwd)  # Stay in the current repository
fi

# Mark the repository as a safe directory to avoid ownership errors
git config --global --add safe.directory /github/workspace

# Install dependencies
pip install --upgrade pip
pip install -r /app/requirements.txt

# Run the Python script to generate the SVG
python -m generate_svg.svg_generator

# Create and checkout to the specified branch
git checkout -b $BRANCH

# Commit and push the SVG to the specified branch
git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"

# Set up authentication using GITHUB_TOKEN
git remote set-url origin https://github-actions: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@github.com/$REPOSITORY.git

git add output/commit_percentage.svg
git commit -m "Update commit percentage dashboard SVG"
git push --set-upstream origin $BRANCH
