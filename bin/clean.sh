#!/bin/bash

# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.


# Clean script to remove build artifacts and virtual environments
# This script removes:
# - Any .venv folder in the current repository
# - foundation-models-c/.build folder if present

echo "Starting cleanup..."

# Remove .venv folder if it exists
if [ -d ".venv" ]; then
    echo "Removing .venv folder..."
    rm -rf .venv
    echo "✓ .venv folder removed"
else
    echo "✓ No .venv folder found"
fi

# Run build files cleanup script
if [ -f "bin/clean-build-files.sh" ]; then
    echo "Running build files cleanup script..."
    bash bin/clean-build-files.sh
else
    echo "✓ No build files cleanup script found"
fi

echo "Cleanup completed!"
