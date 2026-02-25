#!/bin/bash

# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

# Alternative publishing method for gh-page that doesn't rely on Github actions.
# 1. build the doc sphinx webiste using: 
#   - cd docs
#   - uv sync --group docs
#   - make clean
#   - make html
# 2. Copy the contents of /docs/build/html to a temporary location
# 3. Go to the gh-pages branch
# 4. Delete all files in the gh-pages branch
# 5. Copy the contents from the temporary location to the gh-pages branch
# 6. Commit and push the changes to the gh-pages branch

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting documentation publishing process...${NC}"

# Get the root directory of the repository
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Warning: You have uncommitted changes. Please commit or stash them first.${NC}"
    read -p "Do you want to continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Build the documentation
echo -e "${GREEN}Step 1: Building Sphinx documentation...${NC}"
cd "$REPO_ROOT/docs"

echo "Installing documentation dependencies..."
uv sync --group docs

echo "Cleaning previous builds..."
make clean

echo "Building HTML documentation..."
make html

if [ ! -d "build/html" ]; then
    echo -e "${RED}Error: Documentation build failed - build/html directory not found${NC}"
    exit 1
fi

# Step 2: Copy the contents to a temporary location (dereference symlinks with -L)
echo -e "${GREEN}Step 2: Copying built documentation to temporary location...${NC}"
TEMP_DIR=$(mktemp -d)
echo "Temporary directory: $TEMP_DIR"

# Use -L to dereference symlinks, ensuring all files are actual files not symlinks
cp -rL "$REPO_ROOT/docs/build/html/"* "$TEMP_DIR/" 2>/dev/null || true
cp -rL "$REPO_ROOT/docs/build/html/".* "$TEMP_DIR/" 2>/dev/null || true

# Create .nojekyll file to disable Jekyll processing on GitHub Pages
touch "$TEMP_DIR/.nojekyll"

# Step 3: Switch to gh-pages branch
echo -e "${GREEN}Step 3: Switching to gh-pages branch...${NC}"
cd "$REPO_ROOT"

# Save current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"

# Check if gh-pages branch exists
if git show-ref --verify --quiet refs/heads/gh-pages; then
    echo "Checking out existing gh-pages branch..."
    git checkout gh-pages
else
    echo "Creating new gh-pages branch..."
    git checkout --orphan gh-pages
fi

# Step 4: Delete all files in the gh-pages branch (except .git)
echo -e "${GREEN}Step 4: Cleaning gh-pages branch...${NC}"
git rm -rf . 2>/dev/null || true
# Remove any remaining files and directories, but preserve .git
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} + 2>/dev/null || true

# Step 5: Copy the contents from the temporary location
echo -e "${GREEN}Step 5: Copying documentation to gh-pages branch...${NC}"
cp -r "$TEMP_DIR/"* . 2>/dev/null || true
cp "$TEMP_DIR/.nojekyll" . 2>/dev/null || true

# Verify no symlinks exist in the current directory (don't exit on error)
echo "Checking for symlinks..."
SYMLINKS=$(find . -type l ! -path './.git/*' 2>/dev/null || true)
if [ -n "$SYMLINKS" ]; then
    echo -e "${RED}Warning: Symlinks detected in gh-pages branch:${NC}"
    echo "$SYMLINKS"
    echo -e "${YELLOW}These symlinks may cause issues with GitHub Pages.${NC}"
else
    echo "No symlinks found - good!"
fi

# Clean up temporary directory
rm -rf "$TEMP_DIR"

# Step 6: Commit and push the changes
echo -e "${GREEN}Step 6: Committing and pushing changes...${NC}"

# Add all files
git add -A

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo -e "${YELLOW}No changes to commit. Documentation is already up to date.${NC}"
else
    # Commit with timestamp
    COMMIT_MSG="Update documentation - $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$COMMIT_MSG"
    
    echo "Pushing to gh-pages branch..."
    git push origin gh-pages
    
    echo -e "${GREEN}Documentation successfully published!${NC}"
fi

# Return to original branch
echo "Returning to $CURRENT_BRANCH branch..."
git checkout "$CURRENT_BRANCH"

echo -e "${GREEN}Done! Documentation has been published to gh-pages branch.${NC}"
