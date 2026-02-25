#!/bin/bash

# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.


# Build a source distribution for the python-apple-fm-sdk package.

# Step 1: Clean previous build artifacts
echo "Cleaning previous build artifacts..."
bash bin/clean-build-files.sh

# Step 2: Build source distribution
echo "Building source distribution..."
python3 -m build --sdist --outdir dist


echo "Source distribution built successfully! Check the dist/ directory for the generated .tar.gz file."